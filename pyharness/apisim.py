"""Recorded copies of JSONPlaceholder and httpbin for API coding tasks.

Used in two ways:
  * grading "mutants": your test runs against deliberately broken responses and must fail;
  * a fallback (and the CI validator) when the live API can't be reached.

The JSONPlaceholder data is the project's published dataset, so responses match the live API.
"""
import copy
import json
import re
import urllib.parse

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response
from requests.structures import CaseInsensitiveDict

JP = {}            # filled by load_jsonplaceholder()
_ORIGINAL_SEND = HTTPAdapter.send
REASONS = {200: "OK", 201: "Created", 204: "No Content", 400: "Bad Request", 401: "Unauthorized",
           403: "Forbidden", 404: "Not Found", 418: "I'm a teapot", 429: "Too Many Requests",
           500: "Internal Server Error", 503: "Service Unavailable"}


def load_jsonplaceholder(path):
    global JP
    with open(path, encoding="utf-8") as f:
        JP = json.load(f)


# ---------------------------------------------------------------- helpers
def _body_json(request):
    if not request.body:
        return {}
    body = request.body.decode() if isinstance(request.body, bytes) else request.body
    ctype = request.headers.get("Content-Type", "")
    if "json" in ctype:
        try:
            return json.loads(body)
        except ValueError:
            return {}
    return dict(urllib.parse.parse_qsl(body))


def _filter(items, query):
    out = items
    for key, values in query.items():
        if key.startswith("_"):
            continue
        out = [i for i in out if str(i.get(key)) in values]
    if "_sort" in query:
        k = query["_sort"][0]
        out = sorted(out, key=lambda i: i.get(k), reverse=query.get("_order", ["asc"])[0] == "desc")
    if "_page" in query:
        limit = int(query.get("_limit", ["10"])[0])
        page = int(query["_page"][0])
        out = out[(page - 1) * limit: page * limit]
    elif "_limit" in query:
        out = out[: int(query["_limit"][0])]
    return out


# ---------------------------------------------------------------- JSONPlaceholder
CHILDREN = {"posts": {"comments": "postId"}, "users": {"posts": "userId", "todos": "userId", "albums": "userId"},
            "albums": {}}


def jsonplaceholder(request, timeout):
    url = urllib.parse.urlparse(request.url)
    query = urllib.parse.parse_qs(url.query)
    parts = [p for p in url.path.split("/") if p]
    method = request.method.upper()
    if not parts or parts[0] not in JP:
        return 404, {}, {}
    resource = parts[0]
    items = JP[resource]
    if len(parts) == 1:
        if method == "GET":
            return 200, _filter(items, query), {}
        if method == "POST":
            data = _body_json(request)
            return 201, {**data, "id": len(items) + 1}, {}
        return 404, {}, {}
    try:
        rid = int(parts[1])
    except ValueError:
        return 404, {}, {}
    item = next((i for i in items if i["id"] == rid), None)
    if len(parts) == 3:
        child = parts[2]
        fk = CHILDREN.get(resource, {}).get(child)
        if method != "GET" or fk is None or child not in JP:
            return 404, {}, {}
        return 200, _filter([c for c in JP[child] if c.get(fk) == rid], query), {}
    if method == "GET":
        return (200, item, {}) if item else (404, {}, {})
    if method == "PUT":
        return (200, {**_body_json(request), "id": rid}, {}) if item else (500, {}, {})
    if method == "PATCH":
        return (200, {**(item or {}), **_body_json(request)}, {}) if item else (200, _body_json(request), {})
    if method == "DELETE":
        return 200, {}, {}
    return 404, {}, {}


# ---------------------------------------------------------------- httpbin
def httpbin(request, timeout):
    url = urllib.parse.urlparse(request.url)
    parts = [p for p in url.path.split("/") if p]
    # httpbin echoes header names in Title-Case (X-Request-ID -> X-Request-Id)
    headers = {"-".join(w.capitalize() for w in k.split("-")): v for k, v in request.headers.items()}
    args = {k: v[0] if len(v) == 1 else v for k, v in urllib.parse.parse_qs(url.query).items()}
    echo = {"args": args, "headers": headers, "url": request.url}
    method = request.method.upper()
    if not parts:
        return 404, {}, {}
    head = parts[0]
    if head in ("get", "post", "put", "patch", "delete") and head.upper() == method:
        if method != "GET":
            raw = request.body.decode() if isinstance(request.body, bytes) else (request.body or "")
            try:
                parsed = json.loads(raw) if raw else None
            except ValueError:
                parsed = None
            echo.update(data=raw, json=parsed, form=dict(urllib.parse.parse_qsl(raw)) if parsed is None else {})
        return 200, echo, {}
    if head in ("get", "post", "put", "patch", "delete"):
        return 405, "", {"Content-Type": "text/html"}
    if head == "status" and len(parts) > 1:
        return int(parts[1]), "", {"Content-Type": "text/html"}
    if head == "headers":
        return 200, {"headers": headers}, {}
    if head == "basic-auth" and len(parts) == 3:
        import base64
        expected = "Basic " + base64.b64encode(f"{parts[1]}:{parts[2]}".encode()).decode()
        if headers.get("Authorization") == expected:
            return 200, {"authenticated": True, "user": parts[1]}, {}
        return 401, "", {"WWW-Authenticate": 'Basic realm="Fake Realm"'}
    if head == "bearer":
        auth = headers.get("Authorization", "")
        if auth.startswith("Bearer ") and len(auth) > 7:
            return 200, {"authenticated": True, "token": auth[7:]}, {}
        return 401, "", {"WWW-Authenticate": "Bearer"}
    if head == "delay" and len(parts) > 1:
        seconds = float(parts[1])
        read_timeout = timeout[1] if isinstance(timeout, tuple) else timeout
        if read_timeout is not None and read_timeout < seconds:
            raise requests.exceptions.ReadTimeout(f"Read timed out. (read timeout={read_timeout})")
        return 200, echo, {}
    if head == "json":
        return 200, {"slideshow": {"author": "Yours Truly", "date": "date of publication",
                                   "slides": [{"title": "Wake up to WonderWidgets!", "type": "all"},
                                              {"items": ["Why <em>WonderWidgets</em> are great",
                                                         "Who <em>buys</em> WonderWidgets"],
                                               "title": "Overview", "type": "all"}],
                                   "title": "Sample Slide Show"}}, {}
    if head == "uuid":
        return 200, {"uuid": "6f1c1d4e-2b8a-4c1e-9d6a-0c5b7f3a9e21"}, {}
    if head == "response-headers":
        return 200, args, {k: str(v) for k, v in args.items()}
    return 404, "", {"Content-Type": "text/html"}


HOSTS = {"jsonplaceholder.typicode.com": jsonplaceholder, "httpbin.org": httpbin}


# ---------------------------------------------------------------- mutants
def _walk(body, path):
    parts = path.split(".")
    target = body
    for p in parts[:-1]:
        target = target[int(p)] if isinstance(target, list) else target[p]
    last = parts[-1]
    return target, (int(last) if isinstance(target, list) else last)


def apply_mutant(mutant, request, status, body, headers):
    if not mutant:
        return status, body, headers
    only = mutant.get("only")
    if only and only not in f"{request.method} {request.url}":
        return status, body, headers
    body = copy.deepcopy(body)
    if "status" in mutant:
        status = mutant["status"]
        body = mutant.get("body", {"error": REASONS.get(status, "error")})
    if "body" in mutant and "status" not in mutant:
        body = mutant["body"]
    for path, value in mutant.get("set", {}).items():
        try:
            target, key = _walk(body, path)
            target[key] = value
        except (KeyError, IndexError, TypeError, ValueError):
            pass
    for path in mutant.get("delete", []):
        try:
            target, key = _walk(body, path)
            del target[key]
        except (KeyError, IndexError, TypeError, ValueError):
            pass
    if "truncate" in mutant and isinstance(body, list):
        body = body[: mutant["truncate"]]
    if "headers" in mutant:
        headers = {**headers, **mutant["headers"]}
    return status, body, headers


# ---------------------------------------------------------------- adapter patch
def _make_response(request, status, body, headers):
    r = Response()
    r.status_code = status
    if isinstance(body, (dict, list)):
        content = json.dumps(body).encode()
        base = {"Content-Type": "application/json; charset=utf-8"}
    else:
        content = (body or "").encode()
        base = {"Content-Type": "text/plain; charset=utf-8"}
    r._content = content
    r.headers = CaseInsensitiveDict({**base, **headers, "Content-Length": str(len(content))})
    r.encoding = "utf-8"
    r.url = request.url
    r.request = request
    r.reason = REASONS.get(status, "")
    return r


NETWORK_ERRORS = (requests.exceptions.ConnectionError, requests.exceptions.SSLError)
LOG = None          # set to a list to record (request, response) pairs, e.g. for reference data
FELL_BACK = False   # set by install_fallback() when a live call was served from the recorded copy
CALLS = 0           # requests made since install_fallback()


def _log(request, response):
    if LOG is not None:
        LOG.append((request, response))
    return response


def _recorded(request, timeout, mutant=None):
    host = urllib.parse.urlparse(request.url).hostname
    handler = HOSTS.get(host)
    if handler is None:
        raise requests.exceptions.ConnectionError(f"No recorded copy of {host}; use the URLs given in the task.")
    status, body, headers = handler(request, timeout)
    status, body, headers = apply_mutant(mutant, request, status, body, headers)
    return _make_response(request, status, body, headers)


def install(mutant=None):
    """Route requests to the recorded APIs (optionally with a mutant applied)."""
    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        return _log(request, _recorded(request, timeout, mutant))
    HTTPAdapter.send = send


def install_fallback():
    """Call the real APIs; if one is unreachable, answer that request from the recorded copy instead."""
    global FELL_BACK, CALLS
    FELL_BACK, CALLS = False, 0

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        global FELL_BACK, CALLS
        CALLS += 1
        try:
            return _log(request, _ORIGINAL_SEND(self, request, stream=stream, timeout=timeout, verify=verify,
                                                cert=cert, proxies=proxies))
        except NETWORK_ERRORS:
            if urllib.parse.urlparse(request.url).hostname not in HOSTS:
                raise
            FELL_BACK = True
            return _log(request, _recorded(request, timeout))
    HTTPAdapter.send = send


def uninstall():
    HTTPAdapter.send = _ORIGINAL_SEND


# ---------------------------------------------------------------- task runner


def _run_snippets(snippets, ns):
    results = []
    for t in snippets:
        try:
            exec(compile(t, "<test>", "exec"), dict(ns))
            results.append({"test": t, "ok": True})
        except AssertionError as e:
            results.append({"test": t, "ok": False, "err": str(e) or "assertion failed"})
        except NETWORK_ERRORS as e:
            results.append({"test": t, "ok": False, "network": True, "err": f"{type(e).__name__}: {e}"})
        except Exception as e:  # noqa: BLE001
            results.append({"test": t, "ok": False, "err": f"{type(e).__name__}: {e}"})
    return results


def run_api_task(ns, tests, entry, mutants, live):
    """Returns {"mode": "live"|"recorded", "results": [...]}."""
    mode = "recorded"
    results = None
    if live:
        uninstall()
        results = _run_snippets(tests, ns)
        if any(r.get("network") for r in results):
            results = None          # live API unreachable here: fall back to the recorded copy
        else:
            mode = "live"
    if results is None:
        install()
        try:
            results = _run_snippets(tests, ns)
        finally:
            uninstall()
    for r in results:
        r["label"] = ("Passes against the live API: " if mode == "live" else "Passes against the API: ") + r["test"]
    if entry and mutants:
        for m in mutants:
            install(m)
            try:
                exec(compile(entry, "<entry>", "exec"), dict(ns))
                caught, err = False, None
            except Exception as e:  # noqa: BLE001 - any failure means the test noticed the broken response
                caught, err = True, f"{type(e).__name__}: {e}"
            finally:
                uninstall()
            results.append({"test": f"mutant: {m['label']}", "label": f"Catches a broken response: {m['label']}",
                            "ok": caught, "err": None if caught else "your test still passed with this broken response",
                            "got": None})
    return {"mode": mode, "results": results}
