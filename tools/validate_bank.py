"""Validate the question bank in data/*.json.

Checks every question has the required fields and valid values, ids are unique,
questions aren't duplicated, and every Python coding task's reference solution
passes all of its tests while the starter code does not.

Run:  python tools/validate_bank.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TOPICS = {"Python", "Playwright", "API testing", "Pytest & framework design",
          "CI, debugging & flakiness", "Behavioral"}
DIFFICULTIES = {"warm-up", "core", "deep"}
KINDS = {"concept", "python_code"}
REQUIRED = ["id", "topic", "difficulty", "kind", "question", "what_tested", "model"]


def run_tests(code, tests):
    ns = {}
    exec(code, ns)
    results = []
    for t in tests:
        try:
            exec(t, dict(ns))
            results.append(True)
        except Exception as e:  # noqa: BLE001 - we report any failure
            results.append(f"{type(e).__name__}: {e}")
    return results


def main():
    problems = []
    ids, questions = set(), set()
    total = coding = 0
    for path in sorted(DATA.glob("*.json")):
        items = json.loads(path.read_text(encoding="utf-8"))
        for q in items:
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

            if q.get("kind") == "python_code":
                coding += 1
                tests = q.get("tests") or []
                if len(tests) < 3:
                    problems.append(f"{where}: coding task needs at least 3 tests")
                if not q.get("starter_code") or not q.get("solution"):
                    problems.append(f"{where}: coding task needs starter_code and solution")
                    continue
                for test, ok in zip(tests, run_tests(q["solution"], tests)):
                    if ok is not True:
                        problems.append(f"{where}: solution fails `{test}` ({ok})")
                if all(r is True for r in run_tests(q["starter_code"], tests)):
                    problems.append(f"{where}: starter code passes every test")

    print(f"{total} questions checked ({coding} coding tasks)")
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        print(f"{len(problems)} problem(s) found")
        sys.exit(1)
    print("All good.")


if __name__ == "__main__":
    main()
