# Playwright Interview Prep

Free mock-interview practice for **SDET / QA automation** roles built on **Python, Playwright and API testing**.

**Live site:** https://bskamal1933.github.io/playwright-interview-prep/

## What it does

- **10-question sessions** with a fixed mix: 5 Python, 3 Playwright, 2 API testing, interleaved so no topic repeats back to back. Shorter sessions keep the same ratio.
- **Live Python editor** for coding tasks: write a solution, click **Run tests**, and see which hidden tests pass, the actual value on failures, stdout and tracebacks. Infinite loops are stopped after 10 seconds.
- **Model answers** for every question, written at Senior SDET level: a direct answer, the reasoning, and a real-project detail.
- **Self-scoring** on a 1–4 hiring scale, with a summary of scores by skill at the end.
- **Three levels:** Mid-level, Senior SDET, Lead / Manager. Optional Framework, CI & flakiness and Behavioral modules can be added to any session.
- Runs entirely in your browser. No sign-up, no backend, nothing is sent anywhere. Progress is saved in your browser only.

## Question bank

**675 questions** across six modules. Questions are drawn from topics commonly reported in real SDET, QA automation and QA lead interviews, and every model answer is written for this project. Sessions pick at random and show questions you haven't seen yet first.

| Module | Questions | What's covered |
|---|---|---|
| Python | 145 | 84 concept + 61 live-coding tasks with hidden tests (strings, lists, dicts, classic algorithms, log/JSON parsing, money with Decimal, dates, OOP, decorators, generators) |
| Playwright | 120 | architecture, locators, auto-wait, assertions, contexts, auth reuse, network mocking, frames and dialogs, tracing, pytest-playwright, parallel runs, Selenium migration, real-world scenarios |
| API testing | 103 | HTTP and REST semantics, status codes, auth (OAuth, JWT, cookies), schema and contract testing, test design, async and webhooks, resilience, security (OWASP API), finance scenarios |
| Pytest & framework design | 103 | fixtures and scopes, parametrisation, hooks and plugins, xdist, reporting, framework architecture, POM vs Screenplay, test data, config and secrets, scaling across teams |
| CI, debugging & flakiness | 102 | pipeline design, GitHub Actions and Jenkins, Docker and Kubernetes basics, deployments, flaky-test root causes and quarantine, debugging CI-only failures, triage and post-mortems |
| Behavioral | 102 | career and motivation, conflict and influence, ownership, prioritisation, QA leadership and people management, situational questions, project and framework walkthroughs |

Behavioral answers explain what the interviewer is assessing and give a strong structure (usually STAR) to fill with your own experience, rather than a script to memorise.

Every coding task's reference solution is checked against its tests, and its starter code is checked to fail them, by `tools/validate_bank.py`, which also runs in GitHub Actions on every change to `data/`.

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
py-worker.js               runs Python in a Web Worker so long-running code can be stopped
pyodide/                   Pyodide 0.26.4 runtime (CPython compiled to WebAssembly)
tools/validate_bank.py     checks the bank and runs every coding task's tests
skill/                     a Claude skill version of the interview helper
```

## Contributing questions

Add entries to the right `data/<module>.json` file. Each question has:

| Field | Required | Notes |
|---|---|---|
| `id` | yes | unique, e.g. `py-146` |
| `topic` | yes | one of the six module names |
| `difficulty` | yes | `warm-up`, `core` or `deep` |
| `kind` | yes | `concept` or `python_code` |
| `question`, `what_tested`, `model` | yes | `model` is Markdown |
| `hint`, `tags` | no | |
| `starter_code`, `tests`, `solution` | coding tasks | `tests` are single-line or short multi-line `assert` snippets |

Run `python tools/validate_bank.py` before opening a pull request.

## Credits

- Built by [Kamal Bharadwaj](https://github.com/bskamal1933).
- Python runtime: [Pyodide](https://pyodide.org) (MPL-2.0). `pyodide/python_stdlib.wasm` is Pyodide's `python_stdlib.zip`, renamed so more hosts serve it.

## License

MIT for this project's own code and content. Pyodide is distributed under its own license (MPL-2.0).
