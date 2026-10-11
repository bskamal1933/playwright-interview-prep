# Playwright Interview Prep

Free mock-interview practice for **SDET / QA automation** roles built on **Python, Playwright and API testing**.

**Live site:** https://bskamal1933.github.io/playwright-interview-prep/

## What it does

- **10-question sessions** with a fixed mix: 5 Python, 3 Playwright, 2 API testing, interleaved so no topic repeats back to back. Shorter sessions keep the same ratio.
- **Live Python editor** for coding tasks: write a solution, click **Run tests**, and see which hidden tests pass, the actual value on failures, stdout and tracebacks. Infinite loops are stopped after 10 seconds.
- **Model answers** for every question, written at Senior SDET level: a direct answer, the reasoning, and a real-project detail.
- **Self-scoring** on a 1–4 hiring scale, with a summary of scores by skill at the end.
- **Three levels:** Mid-level, Senior SDET, Lead / Manager. Optional Framework, CI & flakiness and Behavioral tracks.
- Runs entirely in your browser. No sign-up, no backend, nothing is sent anywhere. Progress is saved in your browser only.

## Question bank

Questions are compiled from topics commonly reported in real SDET, QA automation and QA lead interviews (public interview reports, interview-prep write-ups and hiring discussions), and every model answer is written for this project. Sessions pick at random and show questions you haven't seen yet first.

| Module | Questions | Notes |
|---|---|---|
| Python | 145 | 84 concept + 61 live-coding tasks with hidden tests |
| Playwright | 120 | locators, waits, assertions, contexts, network, auth, tracing, CI, scenarios |
| API testing | 103 | HTTP/REST, auth, validation, contracts, resilience, security, scenarios |
| Pytest & framework design | 3 | expanding to 100+ |
| CI, debugging & flakiness | 2 | expanding to 100+ |
| Behavioral | 2 | expanding to 100+ |

Every coding task's reference solution is checked against its tests, and its starter code is checked to fail them, by `tools/validate_bank.py`, which also runs in GitHub Actions on every change to `data/`.

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
