# Framework Design, CI/CD and Leadership Questions

For each question: the dimensions a strong answer covers, and the trade-offs interviewers push on. At Senior SDET level, expect concrete design. At Lead/Manager level, also expect process, metrics, and people.

---

## 1. "Design a Playwright + Pytest framework from scratch for a web app with a REST backend."

**Strong answer covers:**
- **Layout:** `pages/` (page and component objects), `api/` (API clients), `tests/ui`, `tests/api`, `fixtures/` or `conftest.py` layering, `data/` (factories), `config/` (per-environment settings).
- **Config:** environment selection via CLI option or env var; `base_url` and credentials from the environment or a secrets manager, never the repo; `pytest.ini`/`pyproject.toml` for markers and default flags.
- **Data:** factories that create unique data through the API; teardown in fixtures; no shared mutable fixtures.
- **Auth:** storage state per role, generated once per session (or per worker).
- **Reporting:** Allure or pytest-html; traces, video and screenshots attached on failure.
- **Execution:** markers (`smoke`, `regression`), `pytest-xdist`, multi-browser matrix, retries only via `pytest-rerunfailures` with the flake logged.
- **Quality gates:** linting (ruff), type hints, PR review of tests like production code.

**Pushback questions:** Why POM and not the Screenplay pattern? How do you stop page objects bloating? Where do assertions live? How does a new joiner add a test in 10 minutes?

---

## 2. "Integrate the suite into CI/CD."

**Strong answer covers:**
- Use the official Playwright Docker image (browsers and OS dependencies pinned to the Playwright version) or `playwright install --with-deps`.
- Pipeline stages: lint, then API tests, then UI smoke on every PR, with full regression nightly or pre-release.
- Shard across machines (split by file; xdist within each machine).
- Upload traces, videos and reports as artifacts. Post a summary to the PR or chat.
- Fail fast on smoke; keep the regression signal visible (trend dashboard).
- Run against ephemeral or preview environments where possible.

**Pushback:** PR time budget (e.g. under 10 min)? What runs where? How do you stop a red nightly being ignored?

---

## 3. "Your suite has a 7% flake rate. Fix it."

**Strong answer covers:**
- **Measure first:** tag and track each test's pass/fail history; identify the top offenders (it's usually a long tail with a few heavy hitters).
- **Classify root causes:** sync issues (sleeps, non-web-first asserts), test data collisions, environment instability, order dependence, real product bugs (race conditions in the app are bugs, not flakes).
- **Policy:** quarantine with an owner and ticket, a time-boxed fix, and no silent retries. Retries hide product bugs.
- **Prevention:** lint rules banning `wait_for_timeout`/`time.sleep`; PR review checklist; stress-run new tests (run N times) before merge.
- **Target and report:** flake rate trending down, e.g. under 1%.

---

## 4. "How do you decide what to automate?"

- Risk × frequency × stability of the feature; ROI of automation vs manual cost.
- Test pyramid: most coverage at unit/API, with UI for critical user journeys only.
- Don't automate unstable UIs under heavy redesign, one-off checks, or things better covered by visual or exploratory testing.
- In finance domains: calculations, rounding, currency, period-end and date logic, permissions, and audit trails are high-value.

---

## 5. Selenium to Playwright migration plan

See the question bank, section 12. At lead level, add: a business case in numbers, a pilot with success criteria, training plan, a coexistence period, and a decommission milestone.

---

## 6. Lead / Manager level (use when the user asks for lead-level, or as stretch questions for seniors)

- **"How do you keep code quality high across 15–20 automation engineers?"** Coding standards doc, shared fixtures and libraries owned by a core group, mandatory PR review with a checklist, linters in CI, pairing for new joiners, periodic suite health reviews.
- **"How do you use AI in automation?"** AI-assisted test generation and PR review, with guardrails: human review, locator and assert standards enforced, no secrets in prompts, measuring time saved vs defects introduced. Strong candidates speak from real experience and name failure modes.
- **"What metrics do you report to stakeholders?"** Automation coverage of critical journeys (not raw test count), pass rate excluding flakes, flake rate, pipeline duration, escaped defects, and time to feedback. Avoid vanity metrics.
- **"A developer says your tests slow down their PRs. Respond."** Acknowledge the cost, show data, then offer a fast smoke tier on PRs, parallelism and sharding, and run the rest post-merge. Turn it into a shared SLA.
- **"Tell me about a time automation missed a critical bug."** Look for ownership, a root cause (gap in coverage, wrong layer, mocked away), and the systemic fix.

---

## 7. Behavioral (any level)

- Conflict with a developer over a bug's severity.
- Pushing back on an unrealistic release date.
- Mentoring a struggling engineer.
- A decision you made that turned out wrong.

Coach STAR (Situation, Task, Action, Result) with a quantified result, and keep the "I" vs "we" clear. Interviewers want to know what *you* did.
