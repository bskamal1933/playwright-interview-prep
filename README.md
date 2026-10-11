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

40 questions, chosen at random per session:

| Track | Questions |
|---|---|
| Python | 9 concept + 8 live-coding tasks with hidden tests |
| Playwright | 8 |
| API testing | 8 |
| Pytest & framework design | 3 |
| CI, debugging & flakiness | 2 |
| Behavioral | 2 |

Every coding task's reference solution is checked against its tests, and the starter code is checked to fail them.

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
index.html        the whole app (HTML, CSS, JS and the question bank)
py-worker.js      runs Python in a Web Worker so long-running code can be stopped
pyodide/          Pyodide 0.26.4 runtime (CPython compiled to WebAssembly)
skill/            a Claude skill version of the interview helper (question bank, coding
                  exercises, framework/leadership questions and an interviewer rubric)
```

## Contributing questions

Questions live in the `BANK` array in `index.html`. Each entry has `topic`, `difficulty` (`warm-up` / `core` / `deep`), `kind` (`concept` or `python_code`), `question`, `what_tested`, `hint` and `model`. Coding tasks also need `starter_code` and `tests` (single-line `assert` statements). Pull requests welcome.

## Credits

- Built by [Kamal Bharadwaj](https://github.com/bskamal1933).
- Python runtime: [Pyodide](https://pyodide.org) (MPL-2.0). `pyodide/python_stdlib.wasm` is Pyodide's `python_stdlib.zip`, renamed so more hosts serve it.

## License

MIT for this project's own code and content. Pyodide is distributed under its own license (MPL-2.0).
