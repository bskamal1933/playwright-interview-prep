## Collections: List, Tuple, Set, Dictionary

### What is the difference between a list and a tuple?

| | List | Tuple |
| --- | --- | --- |
| Syntax | `[1, 2]` | `(1, 2)` |
| Mutable | Yes | No |
| Speed / memory | Slower, more memory | Faster, less memory |
| Hashable (dict key) | No | Yes, if all items are immutable |
| Methods | Many (`append`, `remove`, `sort`…) | Only `count`, `index` |
| Use for | Data that changes | Fixed records: DB rows, coordinates, config |

```python
import sys
sys.getsizeof([1, 2, 3])   # 88
sys.getsizeof((1, 2, 3))   # 64
```

### Compare list, tuple, set and dictionary.

| | List | Tuple | Set | Dict |
| --- | --- | --- | --- | --- |
| Syntax | `[1, 2]` | `(1, 2)` | `{1, 2}` | `{"a": 1}` |
| Ordered | Yes | Yes | No | Yes (insertion order, 3.7+) |
| Mutable | Yes | No | Yes | Yes |
| Duplicates | Allowed | Allowed | Not allowed | Keys unique |
| Access | Index | Index | No indexing | Key |
| Lookup `in` | O(n) | O(n) | O(1) | O(1) |

### `append()` vs `extend()` vs `insert()`?

- `append(x)` — adds `x` as **one element** at the end.
- `extend(iterable)` — adds **each element** of the iterable.
- `insert(i, x)` — adds `x` at index `i` (O(n)).

```python
a = [1, 2]; a.append([3, 4])    # [1, 2, [3, 4]]
b = [1, 2]; b.extend([3, 4])    # [1, 2, 3, 4]
c = [1, 2]; c.insert(0, 0)      # [0, 1, 2]
```

### `remove()` vs `pop()` vs `del` vs `clear()`?

```python
x = [10, 20, 30, 20]
x.remove(20)     # removes FIRST matching VALUE -> [10, 30, 20]; ValueError if absent
x.pop()          # removes by INDEX (default last), RETURNS it -> 20
x.pop(0)         # -> 10
del x[0]         # removes by index/slice, returns nothing
x.clear()        # empties the list -> []
```

### `sort()` vs `sorted()`?

- `list.sort()` — sorts **in place**, returns `None`, only for lists.
- `sorted(iterable)` — returns a **new sorted list**, works on any iterable.

Both accept `key=` and `reverse=True`. Python uses **Timsort**, O(n log n), and the sort is **stable**.

```python
nums = [3, 1, 2]
nums.sort()                       # nums -> [1, 2, 3]
new = sorted((3, 1, 2), reverse=True)  # [3, 2, 1]
words = ["banana", "Apple", "cherry"]
sorted(words, key=str.lower)      # case-insensitive
sorted(words, key=len)            # by length
```

### How do you create a single-element tuple? How do you concatenate tuples?

The **comma** makes a tuple, not the parentheses. Tuples have no `append`/`extend`; use `+`, which creates a new tuple.

```python
t = (5)        # int!
t = (5,)       # tuple
t1, t2 = (1, 2), (3, 4)
t3 = t1 + t2   # (1, 2, 3, 4)
t1 * 2         # (1, 2, 1, 2)
```

### What is packing and unpacking?

```python
point = 3, 4              # packing -> (3, 4)
x, y = point              # unpacking
first, *rest = [1, 2, 3, 4]    # first=1, rest=[2, 3, 4]
head, *_, last = [1, 2, 3, 4]  # head=1, last=4
```

### Can a tuple be modified if it contains a list?

The tuple itself is immutable (its references cannot change), but a **mutable object inside it can change**.

```python
t = (1, [2, 3])
t[1].append(4)    # works -> (1, [2, 3, 4])
# t[1] = [9]      # TypeError
```

Such a tuple is **not hashable**, so it cannot be a dict key.

### What are set operations?

A set is an **unordered collection of unique, hashable items**. Great for removing duplicates and fast membership tests.

```python
a, b = {1, 2, 3}, {2, 3, 4}
a | b      # {1, 2, 3, 4}  union
a & b      # {2, 3}        intersection
a - b      # {1}           difference
a ^ b      # {1, 4}        symmetric difference
a.add(5); a.discard(9)     # discard: no error if missing; remove: KeyError
fs = frozenset([1, 2])     # immutable set, can be a dict key
```

### What are the important dictionary methods?

```python
d = {"env": "qa", "browser": "chrome"}
d["env"]                 # 'qa'  - KeyError if missing
d.get("port", 8080)      # 8080  - safe access with default
d.keys(), d.values(), d.items()
d.update({"port": 80})   # add/overwrite
d.setdefault("tags", []) # insert if missing, return value
d.pop("port")            # remove key, return value
d.popitem()              # remove last inserted pair
for k, v in d.items():
    print(k, v)
```

### How do you get all dictionary keys into a list?

```python
d = {"a": 1, "b": 2, "c": 3}
list(d)            # ['a', 'b', 'c']  - simplest
list(d.keys())     # ['a', 'b', 'c']
[*d]               # unpacking
list(d.values())   # [1, 2, 3]
```

### How do you merge two dictionaries?

```python
d1, d2 = {"a": 1}, {"b": 2, "a": 9}
{**d1, **d2}       # {'a': 9, 'b': 2}  - right side wins
d1 | d2            # same, Python 3.9+
d1.update(d2)      # in place
```

### How do you sort a dictionary by value?

```python
scores = {"ravi": 80, "anu": 95, "sam": 70}
dict(sorted(scores.items(), key=lambda kv: kv[1]))
# {'sam': 70, 'ravi': 80, 'anu': 95}
max(scores, key=scores.get)     # 'anu' -> key with highest value
```

### How do you copy and delete a dictionary?

```python
d = {"env": "qa"}
c1 = d.copy()     # shallow copy
c2 = dict(d)      # shallow copy
del d["env"]      # delete one key
d.clear()         # empty -> {}
del d             # delete the variable itself
```

### What can be a dictionary key?

Any **hashable (immutable)** object: `int`, `str`, `tuple` of immutables, `frozenset`. Lists, dicts and sets **cannot**, because their hash would change when they change.

```python
d = {(1, 2): "point"}     # OK
# d = {[1, 2]: "x"}       # TypeError: unhashable type: 'list'
```

### How do you initialize an empty list, tuple, set and dict without keywords?

```python
lst = []
tup = ()
dct = {}         # {} is a DICT, not a set
st  = {*()}      # empty set without set()
```

### Python array vs list?

A `list` holds mixed types; an `array` (from the `array` module) holds **one numeric type** and uses less memory. For heavy maths use **NumPy** arrays.

```python
from array import array
arr = array("i", [1, 2, 3])   # 'i' = signed int
# arr.append("a")             # TypeError
lst = [1, "a", 2.5]           # mixed types OK
```

### What useful classes does the `collections` module provide?

```python
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict

Counter("banana")                 # Counter({'a': 3, 'n': 2, 'b': 1})
Counter("banana").most_common(1)  # [('a', 3)]

groups = defaultdict(list)        # no KeyError for missing keys
groups["fail"].append("test_login")

q = deque([1, 2, 3])              # fast O(1) append/pop at BOTH ends
q.appendleft(0); q.pop()

Point = namedtuple("Point", "x y")
p = Point(3, 4); p.x              # readable tuple

od = OrderedDict(a=1, b=2)
od.move_to_end("a")               # reorder -> b, a (LRU caches)
```

### Shallow copy vs deep copy?

- **Assignment** `b = a` — no copy; same object.
- **Shallow copy** (`copy.copy()`, `.copy()`, `[:]`) — new outer object, nested objects are **shared**.
- **Deep copy** (`copy.deepcopy()`) — recursively copies everything; fully independent.

```python
import copy
orig    = [[1, 2], [3, 4]]
shallow = copy.copy(orig)
deep    = copy.deepcopy(orig)
orig[0].append(99)
shallow    # [[1, 2, 99], [3, 4]]  -> affected
deep       # [[1, 2], [3, 4]]      -> independent
```

## Comprehensions

### What is a list comprehension?

A concise, single-line way to build a list from an iterable. Usually **faster** than a `for` loop with `append`.

Syntax: `[expression for item in iterable if condition]`

```python
q = [1, 2, 3, 4, 5]
[x * x for x in q]                          # [1, 4, 9, 16, 25]
[x for x in q if x % 2 == 0]                # [2, 4]
[x * 2 if x % 2 == 0 else x * 3 for x in q] # [3, 4, 9, 8, 15]
```

Rule: a **filter `if`** goes **after** `for`; an **`if-else`** goes **before** `for`.

### What are dict and set comprehensions?

```python
q = [1, 2, 3]
{x: x * x for x in q}                       # {1: 1, 2: 4, 3: 9}
{v: k for k, v in {"a": 1, "b": 2}.items()} # swap keys/values
{x % 2 for x in q}                          # {0, 1}  set comprehension
```

### What is a nested comprehension?

```python
matrix = [[1, 2], [3, 4], [5, 6]]
[n for row in matrix for n in row]          # flatten -> [1, 2, 3, 4, 5, 6]
[[row[i] for row in matrix] for i in range(2)]  # transpose -> [[1, 3, 5], [2, 4, 6]]
```

Read loops **left to right** in the same order as nested `for` statements.

### List comprehension vs generator expression?

- `[...]` builds the **whole list in memory** at once.
- `(...)` is a **generator expression** — produces items **lazily**, one at a time, tiny memory.

```python
sum([x * x for x in range(10**6)])   # creates a big list first
sum(x * x for x in range(10**6))     # no list, low memory
```

Use a generator expression when you only iterate once (e.g. `sum`, `any`, `max`).

## Functions

### How do you define a function? Can it return multiple values?

Use `def`. A function can return multiple values — Python packs them into a **tuple**.

```python
def min_max(nums):
    return min(nums), max(nums)

lo, hi = min_max([4, 1, 9])   # 1, 9
```

### What types of function arguments are there?

```python
def api_call(url, method="GET", *args, timeout, **kwargs):
    ...
```

| Type | Example | Notes |
| --- | --- | --- |
| Positional | `f(1, 2)` | Matched by position |
| Keyword | `f(a=1, b=2)` | Matched by name, any order |
| Default | `def f(a, b=10)` | Optional argument |
| Variable positional | `*args` | Extra positionals → **tuple** |
| Variable keyword | `**kwargs` | Extra keywords → **dict** |
| Keyword-only | params after `*` or `*args` | Must be passed by name |
| Positional-only | params before `/` (3.8+) | Must be passed by position |

```python
def f(a, /, b, *, c):
    print(a, b, c)
f(1, 2, c=3)       # OK
f(1, b=2, c=3)     # OK
# f(a=1, b=2, c=3) # TypeError - a is positional-only
```

### What are `*args` and `**kwargs`?

- `*args` collects extra **positional** arguments into a **tuple**.
- `**kwargs` collects extra **keyword** arguments into a **dict**.
- Signature order: normal → `*args` → keyword-only → `**kwargs`.

```python
def log(level, *args, **kwargs):
    print(level, args, kwargs)

log("INFO", 1, 2, user="kamal", env="qa")
# INFO (1, 2) {'user': 'kamal', 'env': 'qa'}

nums, cfg = [1, 2, 3], {"sep": "-"}
print(*nums, **cfg)    # unpacking at call time -> 1-2-3
```

### What is the mutable default argument trap?

Default values are evaluated **once**, when the function is defined — not on each call. A mutable default (list/dict) is shared between calls.

```python
def add_item(item, bucket=[]):     # BUG
    bucket.append(item)
    return bucket

add_item(1)   # [1]
add_item(2)   # [1, 2]  <- same list reused!

def add_item(item, bucket=None):   # FIX
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

### Is Python pass-by-value or pass-by-reference?

Neither exactly — it is **pass-by-object-reference** (call by sharing). The function receives a reference to the same object:

- Mutating a **mutable** object inside the function is visible outside.
- **Reassigning** the parameter only changes the local name.

```python
def modify(lst):
    lst.append(4)     # visible outside
    lst = [0]         # local rebinding, not visible

data = [1, 2, 3]
modify(data)
print(data)           # [1, 2, 3, 4]
```

### What is a lambda (anonymous) function?

A lambda **is** Python's anonymous function: a single-expression function with no name. It cannot contain statements or multiple lines.

```python
square = lambda x: x * x
add = lambda a, b: a + b
users = [("Ravi", 30), ("Anu", 25)]
sorted(users, key=lambda u: u[1])   # sort by age
```

Use for short throwaway functions passed to `sorted`, `map`, `filter`; use `def` for anything reusable.

### `map()` vs `filter()` vs `reduce()`?

| Function | What it does | Returns |
| --- | --- | --- |
| `map(func, it)` | Applies `func` to every item | Iterator, same count |
| `filter(func, it)` | Keeps items where `func` is truthy | Iterator, fewer or equal |
| `reduce(func, it)` | Combines items into one value | Single value (`functools`) |

```python
from functools import reduce
nums = [1, 2, 3, 4]
list(map(lambda x: x * 2, nums))          # [2, 4, 6, 8]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]
reduce(lambda a, b: a + b, nums)          # 10
```

`map` and `filter` return **lazy iterators** in Python 3, so wrap with `list()` to see results.

### What are first-class and higher-order functions?

Functions are **first-class objects**: they can be assigned to variables, passed as arguments, returned from other functions and stored in data structures. A **higher-order function** takes or returns a function (`map`, `sorted(key=)`, decorators).

```python
def shout(t): return t.upper()
def whisper(t): return t.lower()

def greet(fn):            # higher-order
    return fn("Hello")

greet(shout)              # 'HELLO'
actions = {"up": shout, "down": whisper}
actions["down"]("Hi")     # 'hi'
```

### What is a closure?

A closure is an **inner function that remembers variables from its enclosing function**, even after the outer function has finished. Closures are the basis of decorators.

```python
def multiplier(n):
    def multiply(x):
        return x * n      # remembers n
    return multiply

double = multiplier(2)
triple = multiplier(3)
double(5), triple(5)      # (10, 15)
```

### What is a namespace and the LEGB rule?

A **namespace** maps **names to objects**. Python resolves names in **LEGB** order:

1. **Local** — inside the current function
2. **Enclosing** — outer function (for nested functions)
3. **Global** — module level
4. **Built-in** — `print`, `len`, `range`

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)       # local
    inner()
outer()
```

### Global vs local variables? What do `global` and `nonlocal` do?

- **Local** — created inside a function, exists only during the call.
- **Global** — created at module level, readable everywhere.
- To **modify** a global inside a function use `global`; to modify an enclosing function's variable use `nonlocal`.

```python
count = 0
def increment():
    global count
    count += 1          # without global -> UnboundLocalError

def outer():
    total = 0
    def inner():
        nonlocal total
        total += 1
    inner()
    return total        # 1
```

### What is recursion?

A function that **calls itself**. It needs a **base case** to stop, otherwise `RecursionError` (default limit about 1000, `sys.getrecursionlimit()`).

```python
def factorial(n):
    if n <= 1:                   # base case
        return 1
    return n * factorial(n - 1)

def build_list(n):               # build a list recursively
    if n == 0:
        return []
    return build_list(n - 1) + [n]

build_list(5)                    # [1, 2, 3, 4, 5]
```

Recursion is elegant for trees and nested data but uses more memory than loops; Python has **no tail-call optimisation**.

### Which built-in functions should you know?

```python
nums = [3, 1, 4]
len(nums), sum(nums), min(nums), max(nums)   # 3 8 1 4
max(["aa", "b"], key=len)     # 'aa'
any(n > 3 for n in nums)      # True  - at least one
all(n > 0 for n in nums)      # True  - every one
abs(-5), round(2.567, 2)      # 5, 2.57
isinstance(5, int)            # True  - prefer over type() ==
reversed(nums)                # iterator in reverse
dir(str), help(len), type(nums), id(nums)
```
