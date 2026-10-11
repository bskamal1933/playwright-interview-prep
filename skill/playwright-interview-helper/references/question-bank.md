# Question Bank: Python + Playwright (Senior SDET default)

Each entry lists what a strong answer covers. Write the full answer at the target level when producing output. Don't paste these notes verbatim.

## Contents
1. Core architecture
2. Locators
3. Waiting and auto-wait
4. Assertions
5. Browser, context, page
6. pytest-playwright and fixtures
7. Network: mocking, interception, API testing
8. Auth and state
9. Frames, popups, downloads, uploads
10. Debugging and tracing
11. Parallelism and performance
12. Playwright vs Selenium
13. Scenario / debugging questions

---

## 1. Core architecture

**How does Playwright talk to the browser, and how is that different from Selenium WebDriver?**
- Playwright drives browsers over a persistent connection (CDP for Chromium, patched protocols for Firefox/WebKit) through a driver process. Selenium uses the W3C WebDriver HTTP protocol, one request per command.
- Result: lower latency, event-driven waiting, network-level control, and multiple contexts in one browser.
- Ships its own browser builds (`playwright install`). Trade-off: you test Playwright's builds, not necessarily the user's installed browser. Branded Chrome/Edge are available via `channel`.

**Sync vs async API in Python: when would you use each?**
- Sync (`playwright.sync_api`) is simpler and is what `pytest-playwright` gives you by default; it fits most test suites.
- Async fits when you're already in an asyncio app, need concurrency within one test, or use scraping/tooling.
- Don't mix them in one thread. The sync API can't run inside a running event loop.

## 2. Locators

**What's the difference between a Locator and an ElementHandle?**
- A Locator is a lazy, re-resolvable query. It re-finds the element on every action and auto-waits, so it survives re-renders.
- An ElementHandle points to one specific DOM node and goes stale. It's discouraged for tests.
- Locators are strict: an action fails if the query matches more than one element. That catches ambiguous selectors early.

**What is your locator priority, and why?**
- `get_by_role` (with name), then `get_by_label` / `get_by_placeholder` / `get_by_text`, then `get_by_test_id`, with CSS/XPath as a last resort.
- Reasoning: role/label locators mirror how users and assistive tech see the page, so they're resilient to markup changes and double as an accessibility check. Test IDs are stable contracts with developers.
- Mention `set_test_id_attribute` for teams that use `data-qa` and similar.

**How do you handle a list where you need "the Delete button in the row that contains 'Invoice 42'"?**
- Use chaining and filtering: `page.get_by_role("row").filter(has_text="Invoice 42").get_by_role("button", name="Delete")`.
- Know `filter(has=...)`, `has_not`, `nth()`, `first`/`last`, and why `nth()` is brittle.

## 3. Waiting and auto-wait

**Explain auto-waiting. What does Playwright check before a click?**
- Actionability checks: attached, visible, stable (not animating), receives events (not covered), and enabled. For fills, also editable.
- It retries until the timeout. That's why explicit sleeps are unnecessary and harmful.

**When do you still need an explicit wait?**
- When waiting on something that isn't an element action: a network response (`expect_response`), a navigation/URL (`wait_for_url`), a load state, or a custom condition (`wait_for_function`).
- Prefer an `expect(...)` assertion as the wait. Never `wait_for_timeout` except while debugging.

**What's wrong with `wait_for_load_state("networkidle")` as a default?**
- It's flaky on apps with polling, websockets, or analytics, and it's slow. The docs discourage it. Wait for the specific UI state or response that matters instead.

## 4. Assertions

**Difference between `expect(locator).to_have_text("x")` and `assert locator.inner_text() == "x"`?**
- `expect` is web-first: it retries until it passes or times out. `inner_text()` reads once, so the plain assert races the UI.
- Mention soft-assertion options, `expect.configure(timeout=...)` / per-assertion `timeout`, and `to_have_screenshot` (in Python via plugins rather than built in, so be careful here).

## 5. Browser, context, page

**What is a BrowserContext and why does it matter for test design?**
- An isolated, incognito-like session: its own cookies, storage, and cache. Cheap to create, unlike launching a browser.
- `pytest-playwright` gives each test a fresh context, which provides isolation without the cost of a browser launch.
- Use multiple contexts in one test for multi-user scenarios, such as admin approves what a user submitted.

## 6. pytest-playwright and fixtures

**Which fixtures does pytest-playwright provide, and how do you customize them?**
- Function scope: `page`, `context`. Session scope: `browser`, `browser_type`, `playwright`.
- Override `browser_context_args` (session-scoped) to set `base_url`, viewport, locale, `storage_state`, `ignore_https_errors`. Override `browser_type_launch_args` for launch options.
- CLI flags: `--browser chromium --browser firefox`, `--headed`, `--slowmo`, `--base-url`, `--tracing retain-on-failure`, `--video retain-on-failure`, `--screenshot only-on-failure`, `--device "iPhone 13"`.

**How do you structure a Page Object Model with Playwright?**
- Class per page/component, taking `page` in `__init__`, exposing locators as attributes and intent-level methods (`login(user)`).
- Keep assertions in tests, or provide explicit `expect_*` helpers. Senior answers mention component objects for shared widgets and avoiding god-classes.
- Wire page objects through fixtures so tests just request `login_page`.

## 7. Network

**How do you mock an API response?**
- `page.route("**/api/orders*", lambda route: route.fulfill(json=[...]))`. Also `route.continue_()` with modified headers, `route.abort()` to simulate failures, and `route.fetch()` to patch a real response.
- Use cases: deterministic UI tests, error-state testing, decoupling from slow or unstable backends. Trade-off: mocks drift from the real contract, so pair them with contract or API tests.

**How do you do API testing with Playwright?**
- `APIRequestContext`, via `playwright.request.new_context(base_url=...)`, or `page.request` / `context.request`, which share cookies with the browser.
- Common pattern: seed data via API, verify via UI, or log in via API and reuse the storage state. It's faster and less flaky than driving setup through the UI.

## 8. Auth and state

**How do you avoid logging in through the UI in every test?**
- Log in once (UI or API), save `context.storage_state(path="auth.json")`, then load it via `browser_context_args` or `browser.new_context(storage_state=...)`.
- Mention per-role state files, expiry handling, keeping secrets out of the repo, and that parallel workers needing separate accounts may need per-worker state.

## 9. Frames, popups, downloads, uploads

- Frames: `page.frame_locator("#payment").get_by_label("Card number")`. No switching like in Selenium.
- New tab/popup: `with page.expect_popup() as info: ...` then `info.value`.
- Download: `with page.expect_download() as d: ...`, then `d.value.save_as(path)`.
- Upload: `locator.set_input_files(path)`. For hidden inputs or file choosers, use `page.expect_file_chooser()`.
- Dialogs: `page.on("dialog", lambda d: d.accept())`. Register the handler before triggering, and know that unhandled dialogs are auto-dismissed.

## 10. Debugging and tracing

**A test fails only in CI. Walk me through debugging it.**
- Use `--tracing retain-on-failure`, download the artifact, open it with `playwright show-trace trace.zip`. You get a timeline of actions, DOM snapshots before and after each step, network, console, and source.
- Then: check environment differences (viewport, timezone/locale, headless vs headed, CPU slowness, data state, parallelism collisions). Reproduce with the same browser and headless locally, then use `PWDEBUG=1` / `page.pause()` for the Inspector.
- Strong answers fix root causes rather than adding retries.

**What tools speed up writing tests?**
- `playwright codegen <url>` to record and pick locators. Senior answers note codegen output needs refactoring into the POM and better locators.

## 11. Parallelism and performance

**How do you run tests in parallel, and what breaks when you do?**
- `pytest-xdist`: `pytest -n auto`. Each worker gets its own browser; contexts keep tests isolated.
- What breaks: shared test data (two tests editing one record), order-dependent tests, shared accounts with session limits, and global state in fixtures.
- Fixes: unique data per test (factory and uuid), per-worker accounts via `worker_id`, API-based setup and teardown.

## 12. Playwright vs Selenium

**Your team has 2,000 Selenium tests. Would you migrate, and how?**
- Don't big-bang. Measure the pain first (flakiness rate, runtime, maintenance hours). Pilot on the flakiest or most valuable suite. New tests go to Playwright, and old ones migrate when touched or when they flake.
- Show the gains in numbers: runtime, flake rate, debugging time via traces. Mention the costs: retraining, no Grid-style vendor matrix by default, and loss of real branded browsers unless `channel` is used.
- Keep both running in CI during the transition with shared reporting (Allure works with both).

## 13. Scenario questions

- "A test passes locally, fails 1 in 10 runs in CI. What do you do?" Cover trace evidence, root cause categories (timing, data, environment, order), quarantining with a ticket rather than ignoring, and tracking the flake rate.
- "The login page has a CAPTCHA. How do you automate past it?" Don't automate the CAPTCHA. Use a test-environment bypass flag, an allowlisted test account, or API/storage-state login.
- "The app uses shadow DOM." Playwright CSS and role locators pierce open shadow roots by default; XPath does not.
- "How do you test a feature behind a third-party payment iframe?" Use `frame_locator`, vendor sandbox test cards, and mock at the network layer for UI-only tests.
- "How do you handle test data in a finance app?" Cover isolated, seeded data via API or DB fixtures; idempotent cleanup; no production data; masked or synthetic PII; and date and currency edge cases.
