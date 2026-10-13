## Exception Handling

### How are exceptions handled in Python?

With `try` / `except` / `else` / `finally`:

- `try` — code that may fail
- `except` — runs if a matching exception occurs
- `else` — runs only if **no** exception occurred
- `finally` — **always** runs; used for cleanup (close browser, DB connection)

```python
try:
    result = 10 / int("0")
except ZeroDivisionError as e:
    print("Cannot divide by zero:", e)
except (ValueError, TypeError):
    print("Bad input")
else:
    print("Success:", result)
finally:
    print("Cleanup always runs")
```

Catch **specific exceptions first**; avoid bare `except:` because it hides real bugs (and even catches `KeyboardInterrupt`).

### How do you raise and re-raise exceptions?

```python
def withdraw(amount, balance):
    if amount > balance:
        raise ValueError("Insufficient balance")   # raise

try:
    withdraw(500, 100)
except ValueError:
    log("failed")
    raise                       # re-raise same exception

try:
    int("x")
except ValueError as e:
    raise RuntimeError("Config invalid") from e   # chain exceptions
```

### How do you create a custom exception?

Inherit from `Exception` (not `BaseException`).

```python
class ElementNotFoundError(Exception):
    def __init__(self, locator):
        super().__init__(f"Element not found: {locator}")
        self.locator = locator

raise ElementNotFoundError("#login")
```

### What is the exception hierarchy? Name common exceptions.

`BaseException` is the root. `SystemExit`, `KeyboardInterrupt` and `GeneratorExit` inherit from it directly; **all regular errors inherit from `Exception`**.

| Exception | When |
| --- | --- |
| `ValueError` | Right type, wrong value: `int("abc")` |
| `TypeError` | Wrong type: `"1" + 1` |
| `KeyError` | Missing dict key |
| `IndexError` | List index out of range |
| `AttributeError` | Missing attribute/method |
| `NameError` | Undefined variable |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | Missing file |
| `ImportError` / `ModuleNotFoundError` | Import fails |
| `StopIteration` | Iterator exhausted |
| `RecursionError` | Recursion too deep |

### What is `assert`?

`assert condition, message` raises `AssertionError` if the condition is false. Used for **debugging checks and tests**; it is removed when Python runs with `-O`, so never use it for input validation in production.

```python
def apply_discount(price, pct):
    assert 0 <= pct <= 100, "Invalid percentage"
    return price * (1 - pct / 100)
```

### What is a context manager?

An object that sets up and tears down a resource automatically using `with`. It implements `__enter__()` (setup) and `__exit__()` (cleanup, runs even on error).

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc, tb):
        import time
        print(f"Took {time.time() - self.start:.2f}s")
        return False          # don't suppress exceptions

with Timer():
    run_suite()
```

Simpler version with `contextlib`:

```python
from contextlib import contextmanager

@contextmanager
def browser_session():
    driver = start_browser()
    try:
        yield driver          # body of 'with' runs here
    finally:
        driver.quit()         # always cleaned up

with browser_session() as d:
    d.get("https://example.com")
```

## File Handling and Serialization

### `open()` vs `with open() as f`?

`open()` alone needs `f.close()` — if an error occurs first, the file stays open (resource leak). `with` uses a **context manager** that closes the file automatically, even on errors. Always prefer `with`.

```python
with open("data.txt") as f:
    data = f.read()
# file closed here automatically
```

### What are the file modes?

| Mode | Meaning | File exists | File missing |
| --- | --- | --- | --- |
| `r` | Read (default) | Reads | `FileNotFoundError` |
| `w` | Write | **Overwrites** | Creates |
| `a` | Append | Adds at end | Creates |
| `x` | Exclusive create | `FileExistsError` | Creates |
| `r+` | Read + write | Read/write from start | Error |
| `b` / `t` | Binary / text, combine: `rb`, `wb` | — | — |

### What are the different ways to read and write a file?

```python
with open("log.txt", "w") as f:
    f.write("line 1\n")
    f.writelines(["line 2\n", "line 3\n"])

with open("log.txt") as f:
    f.read()          # whole file as one string
    # f.readline()    # one line
    # f.readlines()   # list of all lines

with open("log.txt") as f:
    for line in f:    # best for large files - one line at a time
        print(line.strip())
```

### How do you read a very large file efficiently?

Iterate line by line (the file object is a lazy iterator) or read in fixed-size chunks; never `read()` a multi-GB file at once.

```python
def read_chunks(path, size=1024 * 1024):
    with open(path, "rb") as f:
        while chunk := f.read(size):
            yield chunk
```

### How do you work with JSON?

| Function | Direction |
| --- | --- |
| `json.dumps(obj)` | Python object → JSON **string** |
| `json.loads(s)` | JSON string → Python object |
| `json.dump(obj, f)` | Python object → JSON **file** |
| `json.load(f)` | JSON file → Python object |

```python
import json
payload = {"user": "kamal", "active": True, "roles": ["qa"]}
text = json.dumps(payload, indent=2)
data = json.loads('{"id": 1, "ok": true}')   # true -> True

with open("config.json", "w") as f:
    json.dump(payload, f)
```

Mnemonic: the **s** in `dumps`/`loads` means **string**.

### What is pickling and unpickling?

- **Pickling** (serialisation) — Python object → **byte stream** with `pickle.dump()` / `dumps()`.
- **Unpickling** (deserialisation) — byte stream → Python object with `pickle.load()` / `loads()`.

```python
import pickle
config = {"env": "qa", "browsers": ["chrome", "firefox"]}
with open("config.pkl", "wb") as f:
    pickle.dump(config, f)
with open("config.pkl", "rb") as f:
    loaded = pickle.load(f)
loaded == config     # True
```

Never unpickle data from an **untrusted source** — it can execute arbitrary code.

### JSON vs pickle?

| | JSON | Pickle |
| --- | --- | --- |
| Format | Text, human-readable | Binary |
| Language | Any language | Python only |
| Types | Basic: dict, list, str, number, bool, None | Almost any Python object |
| Security | Safe | Unsafe with untrusted data |
| Use for | APIs, config, data exchange | Caching Python objects |

### How do you read and write CSV files?

```python
import csv
with open("users.csv", newline="") as f:
    for row in csv.DictReader(f):     # each row is a dict
        print(row["name"], row["email"])

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "status"])
    writer.writerow(["login", "PASS"])
```

### How do you work with files and directories (`os` and `pathlib`)?

```python
import os
from pathlib import Path

os.path.exists("data.txt")
os.listdir(".")
os.makedirs("reports/2026", exist_ok=True)
os.environ.get("ENV", "qa")           # environment variable

p = Path("reports") / "result.json"   # modern, object-oriented paths
p.exists(), p.suffix, p.stem          # True, '.json', 'result'
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("{}"); p.read_text()
list(Path(".").glob("*.py"))
```

## Modules, Packages and Environment

### Module vs package vs library?

- **Module** — a single `.py` file with functions, classes, variables.
- **Package** — a folder of modules, traditionally with `__init__.py`.
- **Library** — a collection of packages/modules for reusable functionality (`requests`, `playwright`, `pytest`).

```text
framework/                 <- package
    __init__.py
    pages/                 <- sub-package
        __init__.py
        login_page.py      <- module
    utils.py               <- module
```

### What is `__init__.py`?

It marks a directory as a **regular package** and runs when the package is first imported — used to expose a clean API or run setup. Since Python 3.3, folders without it can still be imported as **namespace packages**, but including it is best practice.

```python
# framework/__init__.py
from .pages.login_page import LoginPage
# now: from framework import LoginPage
```

### What does `if __name__ == "__main__":` do?

Every module has a `__name__`. When a file is **run directly**, `__name__` is `"__main__"`; when it is **imported**, `__name__` is the module name. The guard runs code only on direct execution, not on import.

```python
def main():
    print("running")

if __name__ == "__main__":
    main()          # runs with: python script.py, not on import
```

### What are the different ways to import?

```python
import os                       # whole module
import numpy as np              # alias
from math import sqrt, pi       # specific names
from .utils import helper       # relative import (inside a package)
from os import *                # avoid - pollutes namespace
import importlib; importlib.import_module("json")   # dynamic import
```

A **circular import** (A imports B, B imports A) causes `ImportError`; fix by moving shared code to a third module or importing inside the function.

### What is `PYTHONPATH` / `sys.path`?

`sys.path` is the list of directories Python searches when you `import`: the script's folder → `PYTHONPATH` entries → standard library → `site-packages`. `PYTHONPATH` is an environment variable that adds extra directories.

```python
import sys
print(sys.path)
sys.path.append("/path/to/modules")   # add at runtime
```

```bash
export PYTHONPATH="$PYTHONPATH:/path/to/project"   # Linux/Mac
set PYTHONPATH=C:\project                           # Windows
```

### What is pip?

pip is Python's **package installer**; it downloads packages from **PyPI**.

```bash
pip install playwright
pip install requests==2.32.3      # pinned version
pip install -r requirements.txt   # all dependencies
pip freeze > requirements.txt     # save current versions
pip list
pip uninstall requests
```

### What is a virtual environment and why use one?

A virtual environment is an **isolated Python environment per project** with its own packages, so different projects can use different versions without conflicts.

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
pip install -r requirements.txt
deactivate
```

Alternatives: `poetry`, `pipenv`, `uv`, `conda`.

## Memory Management and Internals

### How does Python manage memory?

Python manages memory automatically in a **private heap**:

1. The **memory manager** allocates heap space; small objects (≤ 512 bytes) use the fast **pymalloc** allocator.
2. **Variables are references** — `a = 10` creates an int object on the heap; `a` points to it.
3. **Reference counting** — each object tracks how many references point to it; at zero it is freed immediately.
4. **Garbage collector** — frees objects stuck in **reference cycles**.
5. **Caching / interning** — small ints (-5 to 256) and some strings are reused.

```python
import sys
a = []
b = a
sys.getrefcount(a)   # 3 -> a, b and the function argument
```

### How does garbage collection work? How do you control it?

- **Reference counting** (primary) — frees an object as soon as its count reaches 0.
- **Generational cyclic GC** (backup) — detects reference cycles such as `a.ref = b; b.ref = a`. Objects live in **3 generations (0, 1, 2)**; new objects start in gen 0, survivors move to older generations, which are scanned less often because most objects die young.

```python
import gc
gc.collect()            # force a collection, returns objects freed
gc.disable(); gc.enable()
gc.get_threshold()      # when each generation is collected
gc.get_count()          # current counts per generation
del obj                 # removes a reference, not necessarily the object
```

### What is interning / small integer caching?

CPython pre-creates integers **-5 to 256** and interns many short identifier-like strings, so equal values may share one object. That is why `is` can surprisingly return `True` — never rely on it for values.

```python
a = 256; b = 256
a is b               # True  - cached
a = 1000; b = 1000
a == b               # True
a is b               # may be False - don't use 'is' for values
import sys
sys.intern("hello")  # force interning
```

### What is the GIL (Global Interpreter Lock)?

The GIL is a mutex in CPython that allows **only one thread to execute Python bytecode at a time**, even on multi-core CPUs. It exists because CPython's reference counting is not thread-safe.

- **CPU-bound** work gets **no speed-up** from threads.
- **I/O-bound** work **does** benefit — a thread releases the GIL while waiting on network, disk or browser.
- Workaround for CPU work: `multiprocessing` (each process has its own GIL), or C extensions like NumPy.
- Python 3.13 added an optional, experimental **free-threaded build** without the GIL; standard CPython still has it.

### How do you check an object's memory size?

```python
import sys
sys.getsizeof(42)          # 28 bytes
sys.getsizeof("")          # ~41 bytes - shallow size only
import tracemalloc         # trace allocations to find memory leaks
```

## Concurrency: Threads, Processes and Async

### What is the difference between a process and a thread?

- **Process** — an independent program with its **own memory space**; heavier; crashes are isolated.
- **Thread** — a lightweight unit inside a process that **shares the process memory**; cheaper but needs synchronisation.

### Multithreading vs multiprocessing?

| | Multithreading | Multiprocessing |
| --- | --- | --- |
| Unit | Threads in one process | Separate processes |
| Memory | Shared — needs locks | Separate — needs IPC (Queue, Pipe) |
| GIL | One shared GIL → no true parallel CPU | One GIL per process → true parallelism |
| Best for | **I/O-bound**: API calls, file I/O, waits | **CPU-bound**: computation, data crunching |
| Overhead | Light, fast start | Heavy, slower start |
| Module | `threading`, `ThreadPoolExecutor` | `multiprocessing`, `ProcessPoolExecutor` |

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests

def fetch(url):                       # I/O-bound -> threads
    return requests.get(url).status_code

def heavy(n):                         # CPU-bound -> processes
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as ex:
        print(list(ex.map(fetch, ["https://example.com"] * 5)))
    with ProcessPoolExecutor() as ex:
        print(list(ex.map(heavy, [10**6] * 4)))
```

`pytest-xdist` (`pytest -n 4`) runs tests in parallel using **separate processes**.

### What is a race condition? How do you prevent it?

A race condition happens when threads update **shared data at the same time** and the result depends on timing. Prevent it with a **Lock**.

```python
import threading
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:              # only one thread at a time
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)                  # 400000
```

### What is asyncio? When should you use it?

`asyncio` gives **single-threaded concurrency** using an **event loop**. `async def` defines a coroutine; `await` pauses it while waiting for I/O so other coroutines can run. Best for **many concurrent I/O tasks** (thousands of HTTP calls, websockets). Playwright has a full async API.

```python
import asyncio

async def fetch(i):
    await asyncio.sleep(1)       # non-blocking wait
    return i

async def main():
    results = await asyncio.gather(*(fetch(i) for i in range(5)))
    print(results)               # ~1 second total, not 5

asyncio.run(main())
```

| Model | Best for |
| --- | --- |
| `asyncio` | Very many I/O tasks, async libraries |
| Threads | I/O tasks with blocking libraries |
| Processes | CPU-heavy work |

## Testing in Python

### What is unit testing? `unittest` vs `pytest`?

Unit testing checks the smallest units of code (functions, methods) in isolation.

| | `unittest` | `pytest` |
| --- | --- | --- |
| Source | Built-in standard library | Third-party |
| Style | Class-based, `TestCase` | Plain functions |
| Assertions | `self.assertEqual(...)` | Plain `assert` with rich diffs |
| Setup | `setUp` / `tearDown` | Fixtures (scoped, reusable) |
| Data-driven | Manual / `subTest` | `@pytest.mark.parametrize` |
| Plugins | Few | Huge (`xdist`, `html`, `allure`, `rerunfailures`) |

```python
import unittest

def add(a, b): return a + b

class TestAdd(unittest.TestCase):
    def setUp(self):              # before each test
        self.data = (2, 3)
    def test_add(self):
        self.assertEqual(add(*self.data), 5)

if __name__ == "__main__":
    unittest.main()
```

### What are pytest fixtures and their scopes?

A fixture provides **setup/teardown and test data**, injected by parameter name. Code after `yield` is teardown. Scopes: `function` (default), `class`, `module`, `package`, `session`. Shared fixtures live in **`conftest.py`** and are auto-discovered.

```python
import pytest

@pytest.fixture(scope="session")
def api_client():
    client = create_client()
    yield client            # test runs here
    client.close()          # teardown

def test_health(api_client):
    assert api_client.get("/health").status_code == 200
```

### How do you write data-driven tests in pytest?

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### What are pytest markers?

```python
@pytest.mark.smoke                   # custom marker -> pytest -m smoke
def test_login(): ...

@pytest.mark.skip(reason="bug 123")
def test_export(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="linux only")
def test_shell(): ...

@pytest.mark.xfail(reason="known issue")
def test_report(): ...
```

### What is mocking? How do you mock in Python?

Mocking replaces a real dependency (API, DB, time) with a **fake object** so the unit is tested in isolation. Use `unittest.mock` (or pytest's `monkeypatch` / `pytest-mock`).

```python
from unittest.mock import patch, MagicMock

def get_user_name(uid):
    return requests.get(f"/users/{uid}").json()["name"]

@patch("requests.get")
def test_get_user_name(mock_get):
    mock_get.return_value.json.return_value = {"name": "Ravi"}
    assert get_user_name(1) == "Ravi"
    mock_get.assert_called_once_with("/users/1")
```

Patch the name **where it is looked up**, not where it is defined.

## Time Complexity and Performance

### What is time complexity (Big-O)?

Big-O describes how running time **grows with input size n** (worst case).

| Big-O | Name | Python example |
| --- | --- | --- |
| O(1) | Constant | `lst[i]`, `d[key]`, `x in set`, `lst.append()` |
| O(log n) | Logarithmic | Binary search, `bisect` |
| O(n) | Linear | `x in list`, loop, `lst.insert(0, x)`, `min()` |
| O(n log n) | Linearithmic | `sorted()`, `lst.sort()` |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci |

### What are the complexities of common operations?

| Operation | list | dict | set |
| --- | --- | --- | --- |
| Index / key access | O(1) | O(1) | — |
| `x in` | O(n) | O(1) | O(1) |
| Append / add | O(1) | O(1) | O(1) |
| Insert / delete at start | O(n) | — | — |
| Pop last | O(1) | — | — |
| Delete by key | — | O(1) | O(1) |
| Sort | O(n log n) | — | — |

Use `collections.deque` when you need O(1) adds/removes at **both ends**.

### How do you optimise Python code?

```python
# O(n^2) - nested loops
def has_dup_slow(lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False

# O(n) - set lookup
def has_dup_fast(lst):
    return len(lst) != len(set(lst))
```

- Replace list lookups with **set/dict** lookups (O(n) → O(1))
- Use **built-ins** and comprehensions (implemented in C)
- Use **generators** for large data
- Use `"".join()` instead of `+` in loops
- Cache with `functools.lru_cache`
- Measure first: `timeit`, `cProfile`

```python
import timeit
timeit.timeit("sum(range(1000))", number=10_000)
```
