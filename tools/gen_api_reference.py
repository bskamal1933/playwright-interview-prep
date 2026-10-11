"""Add a `reference` field to every API coding task in data/api.json.

Runs each task's reference solution against the recorded APIs, logs the requests it makes, and stores the
method, URL, the headers and payload that matter, and a trimmed sample response. The app shows this as
"Reference data" so candidates don't have to guess field names, headers or payload shapes.

Run:  pip install requests && python tools/gen_api_reference.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pyharness"))
import apisim  # noqa: E402

DEFAULT_HEADERS = {"user-agent", "accept-encoding", "accept", "connection", "content-length"}
MAX_CALLS = 3


def trim(body):
    if isinstance(body, list):
        head = [trim(x) for x in body[:2]]
        if len(body) > 2:
            head.append(f"… {len(body) - 2} more")
        return head
    if isinstance(body, dict):
        return {k: trim(v) for k, v in body.items()}
    if isinstance(body, str) and len(body) > 120:
        return body[:117] + "…"
    return body


def payload(request):
    raw = request.body
    if not raw:
        return None, None
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    ctype = request.headers.get("Content-Type", "")
    if "json" in ctype:
        try:
            return "json", json.loads(raw)
        except ValueError:
            pass
    if "x-www-form-urlencoded" in ctype:
        from urllib.parse import parse_qsl
        return "form", dict(parse_qsl(raw))
    return "text", raw


def reference_for(q):
    ns = {}
    exec(q["solution"], ns)
    apisim.LOG = []
    apisim.install()
    try:
        for t in q.get("tests", []):
            try:
                exec(t, dict(ns))
            except Exception:  # noqa: BLE001 - we only want the traffic
                pass
    finally:
        apisim.uninstall()
    log, apisim.LOG = apisim.LOG, None
    calls, seen = [], set()
    for req, resp in log:
        key = (req.method, req.url)
        if key in seen:
            continue
        seen.add(key)
        kind, body = payload(req)
        try:
            rbody = resp.json()
        except ValueError:
            rbody = resp.text
        call = {"method": req.method, "url": req.url,
                "headers": {k: v for k, v in req.headers.items() if k.lower() not in DEFAULT_HEADERS},
                "status": resp.status_code, "reason": resp.reason, "response": trim(rbody)}
        if kind:
            call["body_kind"], call["body"] = kind, body
        calls.append(call)
        if len(calls) >= MAX_CALLS:
            break
    return calls


def main():
    apisim.load_jsonplaceholder(str(ROOT / "pyharness" / "jsonplaceholder.json"))
    path = ROOT / "data" / "api.json"
    bank = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for q in bank:
        if q.get("kind") == "api_code" and q.get("solution"):
            q["reference"] = reference_for(q)
            n += 1
    path.write_text(json.dumps(bank, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"reference data written for {n} API tasks")


if __name__ == "__main__":
    main()
