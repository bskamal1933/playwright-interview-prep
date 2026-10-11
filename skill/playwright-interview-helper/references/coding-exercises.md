# Coding Exercises (pytest-playwright, sync API)

Each exercise includes the prompt, a reference solution, what to look for, and follow-ups. Adapt names and URLs to the user's context. Public practice sites that work well: `https://www.saucedemo.com`, `https://demo.playwright.dev/todomvc`, `https://the-internet.herokuapp.com`.

---

## 1. Login with a page object (warm-up, ~15 min)

**Prompt:** Automate a valid login and an invalid login on saucedemo.com using a page object. No hard waits.

```python
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.submit = page.get_by_role("button", name="Login")
        self.error = page.get_by_test_id("error")

    def open(self):
        self.page.goto("/")

    def login(self, user: str, pwd: str):
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()
```

```python
# conftest.py
import pytest
from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": "https://www.saucedemo.com"}

@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open()
    return lp
```

```python
# tests/test_login.py
import pytest
from playwright.sync_api import expect

def test_valid_login(login_page, page):
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("/inventory.html")

@pytest.mark.parametrize("user,pwd,msg", [
    ("locked_out_user", "secret_sauce", "locked out"),
    ("standard_user", "wrong", "do not match"),
])
def test_invalid_login(login_page, user, pwd, msg):
    login_page.login(user, pwd)
    expect(login_page.error).to_contain_text(msg)
```

Saucedemo's error element uses `data-test`, so set `playwright.selectors.set_test_id_attribute("data-test")` once (for example in a session fixture), or fall back to `page.locator("[data-test='error']")`. A strong candidate notices this instead of guessing.

**Look for:** user-facing locators; assertions in tests; `parametrize` for negative cases; `base_url` via fixture; `to_have_url` (web-first) rather than `assert page.url ==`.

**Follow-ups:** run on Firefox and WebKit (`--browser` flags); make the password come from an environment variable; reuse the login via `storage_state` for other tests.

---

## 2. Mock the API and test the empty and error states (~20 min)

**Prompt:** The orders page calls `GET /api/orders`. Write tests for: (a) the empty list shows "No orders yet"; (b) a 500 shows an error banner. Don't depend on the real backend.

```python
from playwright.sync_api import Page, expect

def test_empty_orders(page: Page):
    page.route("**/api/orders*", lambda route: route.fulfill(json=[]))
    page.goto("/orders")
    expect(page.get_by_text("No orders yet")).to_be_visible()

def test_orders_server_error(page: Page):
    page.route("**/api/orders*", lambda route: route.fulfill(status=500, body="boom"))
    page.goto("/orders")
    expect(page.get_by_role("alert")).to_contain_text("Something went wrong")
```

**Look for:** route registered **before** `goto`; glob patterns; `fulfill(json=...)`; asserting on user-visible outcomes.

**Follow-ups:** assert the request was sent with the right query params (`with page.expect_request(...) as r:`); modify a real response with `route.fetch()`; how they'd stop mocks drifting from the real API (contract tests, schema validation).

---

## 3. API setup, UI verification (~20 min)

**Prompt:** Create an order via the API, then verify it appears in the UI. Clean up afterwards.

```python
import uuid
import pytest
from playwright.sync_api import Playwright, Page, expect

@pytest.fixture
def api(playwright: Playwright):
    ctx = playwright.request.new_context(
        base_url="https://app.example.com",
        extra_http_headers={"Authorization": "Bearer TOKEN_FROM_ENV"},
    )
    yield ctx
    ctx.dispose()

@pytest.fixture
def order(api):
    ref = f"PW-{uuid.uuid4().hex[:8]}"
    resp = api.post("/api/orders", data={"reference": ref, "amount": 125.50})
    assert resp.ok, resp.text()
    body = resp.json()
    yield body
    api.delete(f"/api/orders/{body['id']}")

def test_order_visible(page: Page, order):
    page.goto("/orders")
    row = page.get_by_role("row").filter(has_text=order["reference"])
    expect(row).to_contain_text("125.50")
```

**Look for:** unique data (parallel-safe); fixture teardown with `yield`; `dispose()`; the token not hardcoded (it should come from the environment); filtering rows by text.

**Follow-ups:** what if cleanup fails (idempotent cleanup, sweeper jobs); share auth between `page` and API via `context.request`; schema-validate the API response.

---

## 4. Debug this flaky test (~10 min, great for seniors)

**Prompt:** "This passes locally but fails intermittently in CI. Fix it and explain."

```python
def test_add_to_cart(page):
    page.goto("/inventory.html")
    page.click("#add-to-cart-sauce-labs-backpack")
    page.wait_for_timeout(2000)
    count = page.locator(".shopping_cart_badge").inner_text()
    assert count == "1"
```

**Issues to find:** fixed sleep (too short on slow CI, wasteful locally); one-shot `inner_text` read racing the UI; brittle ID/CSS; no login state, so it depends on test order or shared session.

**Fix:**
```python
def test_add_to_cart(logged_in_page):
    page = logged_in_page
    page.goto("/inventory.html")
    page.get_by_role("button", name="Add to cart").first.click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
```
(Better still: scope to the product card by name instead of `.first`.)

**Follow-ups:** how you'd confirm it's actually fixed (run 50x with `pytest --count` from pytest-repeat, or `-n` stress); how you track flakiness across the suite.

---

## 5. Multi-user flow with two contexts (~20 min)

**Prompt:** A user submits an expense; a manager approves it; the user sees "Approved". Test this in one test.

```python
from playwright.sync_api import Browser, expect

def test_expense_approval(browser: Browser):
    user_ctx = browser.new_context(storage_state="auth/user.json", base_url=BASE)
    mgr_ctx = browser.new_context(storage_state="auth/manager.json", base_url=BASE)
    try:
        user = user_ctx.new_page()
        user.goto("/expenses/new")
        user.get_by_label("Amount").fill("250")
        user.get_by_role("button", name="Submit").click()
        expense_id = user.get_by_test_id("expense-id").inner_text()

        mgr = mgr_ctx.new_page()
        mgr.goto(f"/approvals/{expense_id}")
        mgr.get_by_role("button", name="Approve").click()

        user.reload()
        expect(user.get_by_test_id("status")).to_have_text("Approved")
    finally:
        user_ctx.close()
        mgr_ctx.close()
```

**Look for:** separate contexts (not separate browsers); storage state per role; cleanup in `finally` or fixtures; reading the ID once is fine here because the element is already asserted present by the submit flow (a sharp candidate may add an `expect` first).

**Follow-ups:** convert to fixtures; do the approval via API to speed it up; what if the status updates via websocket (no reload, so rely on `expect` timeout).

---

## 6. Iframe, new tab, download (~15 min, rapid-fire)

```python
def test_iframe(page):
    card = page.frame_locator("iframe[title='Secure payment']")
    card.get_by_label("Card number").fill("4242424242424242")

def test_new_tab(page):
    with page.expect_popup() as info:
        page.get_by_role("link", name="Terms").click()
    terms = info.value
    expect(terms).to_have_title("Terms of Service")

def test_download(page, tmp_path):
    with page.expect_download() as d:
        page.get_by_role("button", name="Export CSV").click()
    path = tmp_path / d.value.suggested_filename
    d.value.save_as(path)
    assert path.read_text().startswith("id,")
```

**Look for:** the `expect_*` context-manager pattern set up **before** the triggering action; `tmp_path`; validating the file content, not just its existence.
