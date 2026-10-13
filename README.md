# Playwright Interview Prep

Free mock-interview practice for **SDET / QA automation** roles built on **Python, Playwright and API testing**.

**Live site:** https://bskamal1933.github.io/playwright-interview-prep/

## What it does

- **Three question formats, all scored automatically:**
  - **Multiple choice** for theory questions: four options, instant right/wrong, then the full explanation.
  - **Python coding** tasks with example input and output, a live editor, and hidden tests. `▶ Run code` runs your code as a script and shows its output; `Run tests` shows which hidden checks pass, the actual value on failures, stdout and tracebacks. The editor scrolls both ways, resizes, and has a full-screen mode.
  - **Real-time API coding**: write tests with the `requests` library against live public APIs ([JSONPlaceholder](https://jsonplaceholder.typicode.com) and [httpbin](https://httpbin.org)). Your test must pass against the real API **and** fail against deliberately broken responses (a 500, a missing field, a wrong value), which proves your assertions actually catch bugs. Each task shows **reference data** for every call it needs (method, URL, headers, JSON payload and a sample response) with copy buttons, so you spend your time on the test rather than guessing field names.
  - **Playwright, framework and CI coding**: page objects, locator strategy, polling waits and network mocking are graded with a recording stand-in for Playwright's page (`pyharness/fakepw.py`, same method names as the sync API), alongside pure-Python tasks on conftest resolution, fixture scopes, pytest.ini, marker expressions, JUnit XML reports, sharding and CI matrices.
- **Pick the format when you start**: *Mixed* (default), *Only multiple choice* or *Only coding*. Coding-only sessions turn off Behavioral, which has no coding tasks.
- **Preparation guide**: a separate page with the answer to every question, grouped by section and topic (e.g. Python → Overloading & overriding, DSA, Decorators; Framework → conftest.py, pytest.ini, Fixtures, Markers), with search, a type filter and reference links to the official docs that open in a new tab.
- **Python Preparation** (`python-preparation.html`): 189 Python interview questions in 19 chapters, basics to advanced, then coding-round programs and output-prediction questions. Each answer opens with a line you can say out loud, followed by code. It has a chapter side menu, full-text search, jump to any question number, a random question picker (all chapters, this chapter, or not yet known), a quiz mode that hides answers until you reveal them, "mark as known" progress saved in the browser, copy buttons on code, and light/dark themes.
- **10-question sessions** with a 5 Python / 3 Playwright / 2 API mix. Topic order and questions are picked at random, unseen questions first. Shorter sessions keep the same ratio, and Framework, CI & flakiness and Behavioral sections can be added.
- **A colourful report**: pie charts for the overall result (correct, partly correct, incorrect, skipped) and for questions by section, plus per-section accuracy, coaching notes and a question log.
- Runs entirely in your browser: no sign-up and no backend. Progress is saved in your browser only. API tasks call the public test APIs directly; if they're unreachable, a recorded copy of the API is used so you can still practise.

## Question bank

**802 questions** across six modules: 662 multiple choice, 110 coding tasks run in the browser (87 Python, 8 Playwright, 8 framework, 7 CI) and 30 real-time API coding tasks. Questions are drawn from topics commonly reported in real SDET, QA automation and QA lead interviews, and every model answer is written for this project.

| Module | Questions | What's covered |
|---|---|---|
| Python | 200 | 113 multiple choice + 87 coding tasks: OOP in depth (inheritance, MRO, super(), mixins, abstract classes, properties), method overloading (singledispatch, typing.overload) and overriding, operator overloading and dunder methods, decorators, generators, context managers, exceptions, concurrency, DSA (binary search, two pointers, prefix sums, heaps, BFS/DFS, DP, topological sort, linked lists, trees), strings, collections, JSON, Decimal and dates |
| Playwright | 129 | 8 coding tasks (page objects, inheritance in POMs, locator priority, polling waits, route mocking, storage state, tables, filtered locators) + multiple choice on architecture, locators, auto-wait, assertions, contexts, auth reuse, network mocking, frames and dialogs, tracing, pytest-playwright, parallel runs, Selenium migration, real-world scenarios |
| API testing | 133 | 30 `requests` coding tasks (GET/POST/PUT/PATCH/DELETE, query params, pagination, schema checks, headers, auth, timeouts, retries) + 103 multiple choice on HTTP, auth, contracts, resilience and security |
| Pytest & framework design | 121 | 8 coding tasks (pytest.ini parsing, `-m` marker expressions, yield-fixture teardown, scope caching, conftest.py resolution, parametrize ids, --strict-markers, environment config) + multiple choice on fixtures and scopes, conftest.py overriding, fixture order, pytest.ini precedence and addopts, parametrisation, hooks and plugins, xdist, reporting, framework architecture, POM vs Screenplay, test data, config and secrets, scaling across teams |
| CI, debugging & flakiness | 117 | 7 coding tasks (JUnit XML summaries and rerun lists, flaky-test detection, duration-based sharding, CI matrices, pass-rate trends, pytest exit codes) + multiple choice on reports (Allure, pytest-html, JUnit), artifacts, caching, secrets, job dependencies, pipeline design, GitHub Actions and Jenkins, Docker and Kubernetes basics, deployments, flaky-test root causes and quarantine, debugging CI-only failures, triage and post-mortems |
| Behavioral | 102 | career and motivation, conflict and influence, ownership, prioritisation, QA leadership and people management, situational questions, project and framework walkthroughs |

Behavioral questions ask you to pick the strongest approach; the explanation then gives a structure (usually STAR) to fill with your own experience, rather than a script to memorise.

`tools/validate_bank.py` checks every question on each change (GitHub Actions): multiple-choice options and answers are valid, every Python task's reference solution passes its tests while the starter fails, and every API task's solution passes against the recorded API and catches every broken response. A weekly job also runs the API solutions against the live APIs.

Topic research drew on public interview reports and prep write-ups, including [Glassdoor SDET interview reports](https://www.glassdoor.com/Interview/sdet-interview-questions-SRCH_KO0,4.htm), [TestDino](https://testdino.com/blog/playwright-interview-questions-answers-2026), [InterviewBit](https://www.interviewbit.com/playwright-interview-questions-answers/), [Software Test Pilot](https://softwaretestpilot.com/api-testing-interview-senior-level) and [The Test Lead](https://thetestlead.medium.com/top-qa-qe-manager-interview-questions-and-how-to-answer-them-ff8deff53f96). No answers were copied from these sources.

## Run locally

Browsers block the Python runner on `file://` URLs, so serve the folder:

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Deploy your own copy

Fork the repo, then in **Settings → Pages** choose **Deploy from a branch**, branch `main`, folder `/ (root)`.

## Repo layout

```
index.html                 the app (HTML, CSS and JS)
data/<module>.json         the question bank, one file per module
python-preparation.html    the Python Preparation page
guide/python/*.md          Python Preparation content, one chapter per "##" heading, one question per "###"
guide/python.json          built from the Markdown by tools/build_python_guide.py (pip install markdown)
py-worker.js               runs Python in a Web Worker so long-running code can be stopped
pyodide/                   Pyodide 0.26.4 runtime (CPython compiled to WebAssembly)
pywheels/                  requests and its dependencies (pure-Python wheels, renamed .whl.wasm)
pyharness/apisim.py        grading harness for API tasks + recorded copies of JSONPlaceholder and httpbin
pyharness/jsonplaceholder.json   JSONPlaceholder's published dataset
pyharness/fakepw.py        recording stand-in for Playwright's Page/Locator/Route used by Playwright coding tasks
data/prep.json             Preparation guide layout: sections, subsections (by tag) and official reference links
tools/validate_bank.py     checks the bank and runs every coding and API task
tools/gen_api_reference.py records the reference data shown for API tasks (rerun after editing one)
skill/                     a Claude skill version of the interview helper
```

## Contributing questions

Add entries to the right `data/<module>.json` file. Common fields: `id` (unique, e.g. `py-146`), `topic` (one of the six module names), `difficulty` (`warm-up`, `core`, `deep`), `kind`, `question`, `what_tested`, `model` (Markdown explanation), and optional `hint` and `tags`.

| `kind` | Extra fields |
|---|---|
| `concept` (multiple choice) | `options` (2-6 strings, similar length so the answer isn't obvious), `answer` (index of the correct option) |
| `python_code` | `examples` (`[{"input", "output"}]`), `starter_code`, `tests` (assert snippets; Playwright tasks can `from fakepw import FakePage`), `solution`. Works for any `topic`, not just Python |
| `api_code` | `endpoint`, `examples`, `starter_code`, `tests` (e.g. `["test_get_post()"]`), `entry` (the call that runs the candidate's test), `reference` (generated: run `python tools/gen_api_reference.py`), `mutants` (broken responses, e.g. `{"label": "server returns 500", "status": 500}`, `{"label": "title empty", "set": {"title": ""}}`, `{"label": "id missing", "delete": ["id"]}`, `{"label": "only 9 items", "truncate": 9}`), `solution` |

Tags decide where a question appears in the Preparation guide: it goes into the first subsection in `data/prep.json` that shares one of its tags.

Run `pip install requests && python tools/validate_bank.py` before opening a pull request.

## Credits

- Built by [Kamal Bharadwaj](https://github.com/bskamal1933).
- Python runtime: [Pyodide](https://pyodide.org) (MPL-2.0). `pyodide/python_stdlib.wasm` is Pyodide's `python_stdlib.zip`, renamed so more hosts serve it.
- HTTP: [requests](https://requests.readthedocs.io) (Apache-2.0) with urllib3 (MIT), idna (BSD), certifi (MPL-2.0) and charset-normalizer (MIT).
- Practice APIs: [JSONPlaceholder](https://jsonplaceholder.typicode.com) (dataset MIT) and [httpbin](https://httpbin.org).

## License

MIT for this project's own code and content. Pyodide is distributed under its own license (MPL-2.0).
