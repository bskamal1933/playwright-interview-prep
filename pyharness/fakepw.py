"""A small stand-in for Playwright's sync Page/Locator/Route API, used to grade Playwright coding tasks
in the browser without launching a real browser.

It mirrors the method names you use with pytest-playwright (page.goto, page.get_by_role(...).click(),
locator.fill, route.fulfill, ...) and records every action in `page.actions`, so a test can assert that
your page object did the right things in the right order.

Locators are described with short strings that match Playwright's own selector syntax:
    page.get_by_role("button", name="Sign in")  -> 'role=button[name="Sign in"]'
    page.get_by_label("Email")                  -> 'label=Email'
    page.get_by_placeholder("Search")           -> 'placeholder=Search'
    page.get_by_test_id("submit")               -> 'testid=submit'
    page.get_by_text("Welcome")                 -> 'text=Welcome'
    page.locator("#cart .item")                 -> '#cart .item'
"""


class FakeLocator:
    def __init__(self, page, desc):
        self.page = page
        self.desc = desc

    # --- chaining -------------------------------------------------------------
    def locator(self, selector):
        return FakeLocator(self.page, f"{self.desc} >> {selector}")

    def get_by_role(self, role, name=None, exact=None):
        return FakeLocator(self.page, f"{self.desc} >> {_role(role, name)}")

    def get_by_text(self, text, exact=None):
        return FakeLocator(self.page, f"{self.desc} >> text={text}")

    def get_by_test_id(self, test_id):
        return FakeLocator(self.page, f"{self.desc} >> testid={test_id}")

    def filter(self, has_text=None):
        return FakeLocator(self.page, f"{self.desc} >> filter(has_text={has_text})")

    def nth(self, index):
        return FakeLocator(self.page, f"{self.desc} >> nth={index}")

    @property
    def first(self):
        return self.nth(0)

    @property
    def last(self):
        return self.nth(-1)

    # --- actions --------------------------------------------------------------
    def _act(self, name, *args):
        self.page.actions.append((name, self.desc, *args))
        handler = self.page.on_action.get((name, self.desc))
        if handler:
            handler(self.page)

    def click(self, timeout=None, **kwargs):
        self._act("click")

    def dblclick(self, **kwargs):
        self._act("dblclick")

    def fill(self, value, timeout=None, **kwargs):
        if not isinstance(value, str):
            raise TypeError(f"fill() expects a string, got {type(value).__name__}")
        self.page.values[self.desc] = value
        self._act("fill", value)

    def clear(self, **kwargs):
        self.page.values[self.desc] = ""
        self._act("clear")

    def type(self, text, **kwargs):
        self.page.values[self.desc] = self.page.values.get(self.desc, "") + text
        self._act("type", text)

    def press(self, key, **kwargs):
        self._act("press", key)

    def check(self, **kwargs):
        self.page.values[self.desc] = True
        self._act("check")

    def uncheck(self, **kwargs):
        self.page.values[self.desc] = False
        self._act("uncheck")

    def select_option(self, value=None, label=None, **kwargs):
        chosen = value if value is not None else label
        self.page.values[self.desc] = chosen
        self._act("select_option", chosen)

    def hover(self, **kwargs):
        self._act("hover")

    def set_input_files(self, files, **kwargs):
        self._act("set_input_files", files)

    def wait_for(self, state="visible", timeout=None):
        self._act("wait_for", state)

    # --- queries --------------------------------------------------------------
    def input_value(self, **kwargs):
        return self.page.values.get(self.desc, "")

    def inner_text(self, **kwargs):
        return self.page.texts.get(self.desc, "")

    def text_content(self, **kwargs):
        return self.page.texts.get(self.desc)

    def all_inner_texts(self):
        return list(self.page.lists.get(self.desc, []))

    def all_text_contents(self):
        return list(self.page.lists.get(self.desc, []))

    def count(self):
        if self.desc in self.page.lists:
            return len(self.page.lists[self.desc])
        return self.page.counts.get(self.desc, 1 if self.desc in self.page.visible else 0)

    def is_visible(self, **kwargs):
        return self.desc in self.page.visible

    def is_checked(self, **kwargs):
        return bool(self.page.values.get(self.desc))

    def get_attribute(self, name, **kwargs):
        return self.page.attrs.get((self.desc, name))

    def __repr__(self):
        return f"<Locator {self.desc}>"


def _role(role, name=None):
    return f'role={role}[name="{name}"]' if name is not None else f"role={role}"


class FakeRequest:
    def __init__(self, url, method="GET", post_data=None, headers=None):
        self.url = url
        self.method = method
        self.post_data = post_data
        self.headers = headers or {}


class FakeRoute:
    """Stand-in for playwright.sync_api.Route: records how the handler resolved the request."""

    def __init__(self, url, method="GET", post_data=None, headers=None):
        self.request = FakeRequest(url, method, post_data, headers)
        self.outcome = None

    def _done(self, outcome):
        if self.outcome is not None:
            raise RuntimeError("Route is already handled")
        self.outcome = outcome

    def fulfill(self, status=200, json=None, body=None, headers=None, content_type=None, **kwargs):
        self._done({"action": "fulfill", "status": status, "json": json, "body": body, "headers": headers or {},
                    "content_type": content_type})

    def continue_(self, **overrides):
        self._done({"action": "continue", **overrides})

    def abort(self, error_code=None):
        self._done({"action": "abort", "error_code": error_code})

    def fallback(self, **kwargs):
        self._done({"action": "fallback"})


class FakePage:
    def __init__(self, base_url="", url="about:blank", title=""):
        self.base_url = base_url
        self.url = url
        self._title = title
        self.actions = []        # ("goto", url) / ("click", desc) / ("fill", desc, value) ...
        self.values = {}         # desc -> current input value
        self.texts = {}          # desc -> text shown (set by the test)
        self.lists = {}          # desc -> list of texts for multi-element locators
        self.counts = {}         # desc -> element count
        self.visible = set()     # descs that are visible
        self.attrs = {}          # (desc, attr) -> value
        self.on_action = {}      # (action, desc) -> callback(page), e.g. to "navigate" after a click
        self.routes = []         # (pattern, handler)

    def goto(self, url, **kwargs):
        if url.startswith("/") and self.base_url:
            url = self.base_url.rstrip("/") + url
        self.url = url
        self.actions.append(("goto", url))

    def reload(self, **kwargs):
        self.actions.append(("reload", self.url))

    def title(self):
        return self._title

    def locator(self, selector):
        return FakeLocator(self, selector)

    def get_by_role(self, role, name=None, exact=None):
        return FakeLocator(self, _role(role, name))

    def get_by_label(self, text, exact=None):
        return FakeLocator(self, f"label={text}")

    def get_by_placeholder(self, text, exact=None):
        return FakeLocator(self, f"placeholder={text}")

    def get_by_test_id(self, test_id):
        return FakeLocator(self, f"testid={test_id}")

    def get_by_text(self, text, exact=None):
        return FakeLocator(self, f"text={text}")

    def get_by_alt_text(self, text, exact=None):
        return FakeLocator(self, f"alt={text}")

    def get_by_title(self, text, exact=None):
        return FakeLocator(self, f"title={text}")

    def route(self, pattern, handler):
        self.routes.append((pattern, handler))
        self.actions.append(("route", pattern))

    def wait_for_url(self, url, **kwargs):
        self.actions.append(("wait_for_url", url))

    def wait_for_load_state(self, state="load", **kwargs):
        self.actions.append(("wait_for_load_state", state))

    def screenshot(self, path=None, full_page=False, **kwargs):
        self.actions.append(("screenshot", path, full_page))
        return b""

    # helpers for tests
    def did(self, *action):
        return tuple(action) in self.actions
