"""Validate the question bank in data/*.json.

Checks:
  * every question has the required fields and valid values; ids and question text are unique;
  * multiple-choice questions have 2-6 distinct options and a valid answer index;
  * every Python coding task's reference solution passes all of its tests, and its starter code doesn't;
  * every API coding task's reference solution passes against the recorded APIs and catches every
    "mutant" (deliberately broken response), and its starter code doesn't pass everything.

Run:  pip install requests && python tools/validate_bank.py
Add --live to also run API task solutions against the real public APIs.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "pyharness"))

TOPICS = {"Python", "Playwright", "API testing", "Pytest & framework design",
          "CI, debugging & flakiness", "Behavioral"}
DIFFICULTIES = {"warm-up", "core", "deep"}
KINDS = {"concept", "python_code", "api_code"}
REQUIRED = ["id", "topic", "difficulty", "kind", "question", "what_tested", "model"]


def run_tests(code, tests):
    ns = {}
    exec(code, ns)
    results = []
    for t in tests:
        try:
            exec(t, dict(ns))
            results.append(True)
        except Exception as e:  # noqa: BLE001 - report any failure
            results.append(f"{type(e).__name__}: {e}")
    return results


def run_api(apisim, q, code, live):
    ns = {}
    exec(code, ns)
    return apisim.run_api_task(ns, q.get("tests", []), q.get("entry"), q.get("mutants") or [], live=live)


def main():
    live = "--live" in sys.argv
    apisim = None
    problems = []
    ids, questions = set(), set()
    total = coding = api = mcq = 0
    for path in sorted(DATA.glob("*.json")):
        for q in json.loads(path.read_text(encoding="utf-8")):
            total += 1
            where = f"{path.name}:{q.get('id', '?')}"
            for field in REQUIRED:
                if not q.get(field):
                    problems.append(f"{where}: missing {field}")
            if q.get("topic") not in TOPICS:
                problems.append(f"{where}: unknown topic {q.get('topic')!r}")
            if q.get("difficulty") not in DIFFICULTIES:
                problems.append(f"{where}: bad difficulty {q.get('difficulty')!r}")
            if q.get("kind") not in KINDS:
                problems.append(f"{where}: bad kind {q.get('kind')!r}")
            if q.get("id") in ids:
                problems.append(f"{where}: duplicate id")
            ids.add(q.get("id"))
            key = q.get("question", "").strip().lower()
            if key in questions:
                problems.append(f"{where}: duplicate question text")
            questions.add(key)

            kind = q.get("kind")
            if kind == "concept":
                mcq += 1
                opts = q.get("options") or []
                if not (2 <= len(opts) <= 6) or len(set(opts)) != len(opts) or not all(isinstance(o, str) and o.strip() for o in opts):
                    problems.append(f"{where}: needs 2-6 distinct non-empty options")
                if not isinstance(q.get("answer"), int) or not (0 <= q["answer"] < len(opts)):
                    problems.append(f"{where}: answer must be a valid option index")

            elif kind == "python_code":
                coding += 1
                tests = q.get("tests") or []
                if len(tests) < 3:
                    problems.append(f"{where}: coding task needs at least 3 tests")
                if not q.get("starter_code") or not q.get("solution"):
                    problems.append(f"{where}: coding task needs starter_code and solution")
                    continue
                if not q.get("examples"):
                    problems.append(f"{where}: coding task needs input/output examples")
                for test, ok in zip(tests, run_tests(q["solution"], tests)):
                    if ok is not True:
                        problems.append(f"{where}: solution fails `{test}` ({ok})")
                if all(r is True for r in run_tests(q["starter_code"], tests)):
                    problems.append(f"{where}: starter code passes every test")

            elif kind == "api_code":
                api += 1
                if apisim is None:
                    import apisim as _apisim
                    _apisim.load_jsonplaceholder(str(ROOT / "pyharness" / "jsonplaceholder.json"))
                    apisim = _apisim
                if not q.get("endpoint") or not q.get("examples") or not q.get("tests"):
                    problems.append(f"{where}: API task needs endpoint, examples and tests")
                if not q.get("reference"):
                    problems.append(f"{where}: API task needs reference data (run tools/gen_api_reference.py)")
                if not q.get("starter_code") or not q.get("solution"):
                    problems.append(f"{where}: API task needs starter_code and solution")
                    continue
                res = run_api(apisim, q, q["solution"], live=False)
                for r in res["results"]:
                    if not r["ok"]:
                        problems.append(f"{where}: solution fails '{r['label']}' ({r.get('err')})")
                if live:
                    live_res = run_api(apisim, q, q["solution"], live=True)
                    if live_res["mode"] != "live":
                        problems.append(f"{where}: live API unreachable")
                    for r in live_res["results"]:
                        if not r["ok"] and not r["test"].startswith("mutant:"):
                            problems.append(f"{where}: solution fails live '{r['label']}' ({r.get('err')})")
                if all(r["ok"] for r in run_api(apisim, q, q["starter_code"], live=False)["results"]):
                    problems.append(f"{where}: starter code passes every check")

    print(f"{total} questions checked: {mcq} multiple choice, {coding} Python coding, {api} API coding"
          + (" (API tasks also run live)" if live else ""))
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        print(f"{len(problems)} problem(s) found")
        sys.exit(1)
    print("All good.")


if __name__ == "__main__":
    main()
