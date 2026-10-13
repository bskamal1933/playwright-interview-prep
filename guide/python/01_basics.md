## Python Basics

### What is Python? What are its key features?

Python is a high-level, interpreted, general-purpose programming language known for readable syntax.

- **Interpreted** — runs line by line via the interpreter, no separate compile step for you
- **Dynamically typed** — variable types are decided at runtime
- **Strongly typed** — no silent type mixing (`"1" + 1` raises `TypeError`)
- **Multi-paradigm** — procedural, object-oriented and functional
- **Automatic memory management** — reference counting + garbage collector
- **Huge standard library and ecosystem** — "batteries included"
- **Cross-platform** and open source

### Is Python compiled or interpreted?

Both. The source `.py` is first **compiled to bytecode** (`.pyc`), and the bytecode is then **executed by the Python Virtual Machine (PVM)**. The standard implementation is **CPython**; others are PyPy (JIT), Jython (JVM), IronPython (.NET).

```text
source.py  -->  compiler  -->  bytecode (.pyc)  -->  PVM  -->  output
```

### What is the difference between `.py` and `.pyc` files?

- `.py` — human-readable **source code**.
- `.pyc` — **compiled bytecode**, created automatically when a module is **imported**, stored in `__pycache__/`.

`.pyc` makes **imports faster** (skips recompiling); it does not make the program run faster. The script you run directly is not cached.

### Dynamic typing vs static typing? What are type hints?

- **Dynamic typing** — the type belongs to the object, not the variable; a variable can point to any type at runtime.
- **Static typing** (Java, C) — the variable type is fixed at compile time.

**Type hints** (Python 3.5+) document expected types. They are **not enforced at runtime**; tools like `mypy` check them.

```python
x = 10        # int
x = "ten"     # now str - allowed

def add(a: int, b: int) -> int:
    return a + b

add("a", "b")   # still runs -> 'ab'; mypy would flag it
```

### What are the differences between Python 2 and Python 3?

Python 2 reached end of life on **1 January 2020**; all new work uses Python 3.

| Feature | Python 2 | Python 3 |
| --- | --- | --- |
| print | Statement: `print "hi"` | Function: `print("hi")` |
| Division | `5 / 2 = 2` | `5 / 2 = 2.5` (`//` for 2) |
| Strings | ASCII by default | Unicode by default |
| `range` | Returns a list; `xrange` is lazy | `range` is lazy; no `xrange` |
| Input | `raw_input()` | `input()` |
| Exceptions | `except E, e` | `except E as e` |
| `dict.keys()` | Returns a list | Returns a view object |

### What is PEP 8?

PEP 8 is Python's official **style guide**.

- 4 spaces per indent, no tabs
- Max line length 79 characters
- `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- 2 blank lines around top-level functions/classes, 1 between methods
- Imports at the top: standard library → third-party → local
- Spaces around operators: `x = a + b`

Tools: `flake8`, `pylint` (lint), `black`, `ruff` (format), usually enforced in CI.

### Why is indentation important in Python?

Python uses **indentation instead of braces `{}`** to define code blocks. Wrong indentation gives `IndentationError` or, worse, changes logic silently.

```python
if True:
    print("inside")
print("outside")
```

### Comments vs docstrings?

- **Comment** (`#`) — ignored by the interpreter; explains *why*.
- **Docstring** (`"""..."""`) — first statement in a module, class or function; stored in `__doc__` and shown by `help()`; explains *what*.

```python
def login(user):
    """Log the user in and return a session token."""
    # TODO: add retry
    ...

print(login.__doc__)
```

### What is `None`?

`None` is a special singleton object meaning "no value". Its type is `NoneType`. A function without `return` returns `None`. Always compare with `is`.

```python
def f(): pass
print(f())          # None
x = None
if x is None:       # correct way
    ...
```

### What is the difference between `is` and `==`?

- `==` compares **values** (calls `__eq__`).
- `is` compares **identity** — whether both names point to the **same object** (same `id()`).

```python
a = [1, 2]; b = [1, 2]; c = a
a == b    # True  - same values
a is b    # False - different objects
a is c    # True  - same object
```

Rule: use `is` only for `None`, `True`, `False`; use `==` for everything else.

## Data Types and Variables

### What are the built-in data types in Python?

| Category | Types |
| --- | --- |
| Numeric | `int`, `float`, `complex` |
| Boolean | `bool` (`True`/`False`, subclass of `int`) |
| Text | `str` |
| Sequence | `list`, `tuple`, `range` |
| Mapping | `dict` |
| Set | `set`, `frozenset` |
| Binary | `bytes`, `bytearray`, `memoryview` |
| None | `NoneType` |

### Mutable vs immutable types?

Mutable objects can be changed **in place**; immutable objects cannot — any "change" creates a **new object** with a new `id()`.

| Mutable | Immutable |
| --- | --- |
| `list`, `dict`, `set`, `bytearray`, user classes | `int`, `float`, `complex`, `bool`, `str`, `tuple`, `frozenset`, `bytes` |

```python
nums = [1, 2]; before = id(nums); nums.append(3)
id(nums) == before     # True  -> same object changed

s = "hi"; before = id(s); s += "!"
id(s) == before        # False -> new object created
```

Only **immutable (hashable)** objects can be dictionary keys or set elements.

### How do variables work in Python?

A variable is a **name that refers to an object**; it is not a box holding a value. Assignment binds a name to an object.

```python
a = [1, 2]
b = a           # b points to the SAME list
b.append(3)
print(a)        # [1, 2, 3]

x, y = 1, 2     # multiple assignment
x, y = y, x     # swap without temp variable
a = b = c = 0   # chained assignment
```

### What is type conversion?

- **Implicit** — Python converts automatically: `3 + 2.5` → `5.5`.
- **Explicit (type casting)** — you convert with built-ins.

```python
int("10")          # 10
int(3.9)           # 3   -> truncates, does not round
float("3.5")       # 3.5
str(100)           # '100'
list("abc")        # ['a', 'b', 'c']
tuple([1, 2])      # (1, 2)
set([1, 1, 2])     # {1, 2}
dict([("a", 1)])   # {'a': 1}
int("1010", 2)     # 10  -> binary to int
bin(10), hex(255)  # ('0b1010', '0xff')
# int("abc")       # ValueError
```

### What are truthy and falsy values?

In a boolean context, these are **falsy**: `False`, `None`, `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `range(0)`. Everything else is **truthy**.

```python
items = []
if not items:
    print("empty list")    # Pythonic empty check
```

### Why does `0.1 + 0.2 != 0.3`?

Floats are stored in **binary floating point**, which cannot represent 0.1 exactly. Use `math.isclose()` for comparison or `Decimal` for money.

```python
0.1 + 0.2                    # 0.30000000000000004
import math
math.isclose(0.1 + 0.2, 0.3) # True
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")  # Decimal('0.3')
```

## Operators

### What operators does Python support?

| Type | Operators |
| --- | --- |
| Arithmetic | `+ - * / // % **` |
| Comparison | `== != > < >= <=` |
| Logical | `and or not` |
| Assignment | `= += -= *= /= //= %= **= :=` |
| Identity | `is`, `is not` |
| Membership | `in`, `not in` |
| Bitwise | `& | ^ ~ << >>` |

### What is the difference between `/`, `//` and `%`?

- `/` — true division, always returns `float`.
- `//` — floor division, rounds **down** toward negative infinity.
- `%` — remainder (modulo); result takes the sign of the divisor.

```python
7 / 2     # 3.5
7 // 2    # 3
-7 // 2   # -4   -> floors, not truncates
7 % 2     # 1
-7 % 2    # 1
2 ** 3    # 8
divmod(7, 2)  # (3, 1)
```

### How do `and` / `or` work? What is short-circuiting?

`and` / `or` **return one of the operands**, not just `True`/`False`, and stop evaluating as soon as the result is known.

```python
0 or "default"      # 'default'
"a" or "b"          # 'a'
0 and 1/0           # 0   -> 1/0 never runs
name = user_input or "Guest"   # common default pattern
```

### What is the ternary (conditional) operator?

A one-line if-else: `value_if_true if condition else value_if_false`.

```python
age = 20
status = "Adult" if age >= 18 else "Minor"
result = "PASS" if actual == expected else "FAIL"
```

### What are membership and identity operators?

```python
"py" in "python"       # True   - membership
3 not in [1, 2]        # True
x = None
x is None              # True   - identity
```

Membership test is **O(1)** for `set`/`dict`, **O(n)** for `list`/`tuple`.

### What is the walrus operator `:=`?

Python 3.8+ **assignment expression** — assigns and returns a value in one expression.

```python
data = [1, 2, 3, 4]
if (n := len(data)) > 3:
    print(f"List too long: {n}")

while (line := f.readline()):
    process(line)
```

### What are chained comparisons?

Python allows `a < b < c`, which means `a < b and b < c`, with `b` evaluated once.

```python
x = 5
1 < x < 10        # True
1 < x > 3         # True  -> 1<x and x>3
```

## Strings

### What are strings? Are they mutable?

A string is an **immutable sequence of Unicode characters**. You cannot change a character in place; every modification creates a new string.

```python
s = "hello"
# s[0] = "H"      # TypeError
s = "H" + s[1:]   # 'Hello' - new object
```

### How does slicing work?

Syntax `seq[start:stop:step]` — `start` included, `stop` excluded, negative indexes count from the end. Slicing **never raises IndexError**.

```python
s = "Playwright"
s[0:4]     # 'Play'
s[4:]      # 'wright'
s[-5:]     # 'right'
s[::2]     # 'Pawih'
s[::-1]    # 'thgirwyalP'  -> reverse
s[:]       # copy
s[100:]    # ''  -> no error
```

### What are the most common string methods?

```python
s = "  Hello World  "
s.strip()               # 'Hello World'   (lstrip/rstrip)
s.lower(), s.upper()    # case change
"hello qa".title()      # 'Hello Qa'
"a,b,c".split(",")      # ['a', 'b', 'c']
"-".join(["a", "b"])    # 'a-b'
s.replace("World", "QA")
s.find("o")             # index or -1
s.index("o")            # index or ValueError
s.count("l")            # 3
s.startswith("  He")    # True
"123".isdigit()         # True  (isalpha, isalnum, isspace)
"abc".center(7, "*")    # '**abc**'
```

### `find()` vs `index()`?

Both return the first position of a substring. If not found, `find()` returns **-1**; `index()` raises **ValueError**.

### f-string vs `.format()` vs `%` formatting?

| Style | Example | Notes |
| --- | --- | --- |
| `%` | `"Hi %s, %d" % (name, age)` | Oldest, C-style |
| `.format()` | `"Hi {}, {}".format(name, age)` | Python 2.6+ |
| f-string | `f"Hi {name}, {age}"` | Python 3.6+, fastest, most readable |

```python
name, score = "Kamal", 92.456
f"{name} scored {score:.2f}"   # 'Kamal scored 92.46'
f"{2 + 3}"                     # '5'  - expressions allowed
f"{name=}"                     # "name='Kamal'" - debugging (3.8+)
f"{1000000:,}"                 # '1,000,000'
f"{'QA':>6}"                   # '    QA'  - right align
```

### Why is `"".join()` better than `+` in a loop?

Strings are immutable, so `+` in a loop creates a new string every iteration — **O(n²)**. `join()` builds the result once — **O(n)**.

```python
words = ["a", "b", "c"]
result = ""
for w in words:
    result += w          # slow for large lists

result = "".join(words)  # fast
```

### What do `ord()` and `chr()` do?

`ord()` returns the Unicode code point of a character; `chr()` does the reverse.

```python
ord("a")            # 97
chr(122)            # 'z'
chr(ord("a") + 1)   # 'b'
```

### What is a raw string?

Prefix `r` makes backslashes literal — useful for regex and Windows paths.

```python
print("C:\new")     # newline breaks it
print(r"C:\new")    # C:\new
```

## Control Flow

### What conditional statements does Python have?

`if` / `elif` / `else`, the ternary operator, and from Python 3.10 **`match-case`** (structural pattern matching).

```python
status = 404
match status:
    case 200:
        msg = "OK"
    case 404 | 410:
        msg = "Not found"
    case _:
        msg = "Unknown"      # default
```

### `for` loop vs `while` loop?

- `for` — iterates over a sequence/iterable; use when the number of items is known.
- `while` — repeats while a condition is true; use when the end depends on a condition.

```python
for i in range(3):
    print(i)

retries = 0
while retries < 3:
    retries += 1
```

### `break` vs `continue` vs `pass`?

| Keyword | Effect |
| --- | --- |
| `break` | Exits the loop completely |
| `continue` | Skips the rest of the current iteration |
| `pass` | Does nothing; placeholder where a statement is required |

```python
for i in range(1, 6):
    if i == 2:
        continue      # skip 2
    if i == 4:
        break         # stop at 4
    print(i)          # 1, 3

def todo():
    pass
```

### What is the `else` clause on a loop?

The `else` block runs only if the loop finishes **without hitting `break`**. Useful for search loops.

```python
for n in [3, 5, 7]:
    if n % 2 == 0:
        print("Found even")
        break
else:
    print("No even number")   # runs
```

### `range()` vs `xrange()`?

In Python 2, `range()` built a full list; `xrange()` was lazy. In Python 3, **`xrange` was removed** and `range()` is lazy and memory-efficient.

```python
r = range(10**9)        # instant, tiny memory
len(r), r[5], 999 in r  # supports len, index, fast membership
list(range(1, 10, 2))   # [1, 3, 5, 7, 9]
list(range(5, 0, -1))   # [5, 4, 3, 2, 1]
```

### What do `enumerate()` and `zip()` do?

- `enumerate()` gives **index + value** while looping.
- `zip()` pairs items from multiple iterables; stops at the shortest.

```python
for i, browser in enumerate(["chrome", "firefox"], start=1):
    print(i, browser)

names, scores = ["a", "b"], [90, 80]
dict(zip(names, scores))          # {'a': 90, 'b': 80}
list(zip(*[(1, "a"), (2, "b")]))  # unzip -> [(1, 2), ('a', 'b')]
```
