## Decorators, Iterators and Generators

### What is a decorator?

A decorator is a function that **takes another function, adds behaviour before/after it, and returns a new function** — without changing the original code. It works because functions are first-class objects and closures remember state. `@decorator` is shorthand for `func = decorator(func)`.

```python
import time, functools

def timer(func):
    @functools.wraps(func)            # keeps original name/docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def run_test():
    time.sleep(1)

run_test()     # run_test took 1.00s
```

Real-world examples: `@pytest.fixture`, `@pytest.mark.parametrize`, `@property`, `@staticmethod`, `@functools.lru_cache`.

### How do you write a decorator that takes arguments?

Add one more outer function that receives the arguments.

```python
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise
        return wrapper
    return decorator

@retry(3)
def click_button(): ...
```

### Why use `functools.wraps`? In what order do stacked decorators run?

Without `@wraps`, the decorated function loses its `__name__` and `__doc__` (it shows `wrapper`). Stacked decorators are **applied bottom-up** and **run top-down**.

```python
@timer      # applied second, runs first
@retry(3)   # applied first
def test(): ...
# same as: test = timer(retry(3)(test))
```

### Iterable vs iterator?

- **Iterable** — any object you can loop over; has `__iter__()` (list, str, dict, file).
- **Iterator** — object with `__iter__()` **and** `__next__()`; remembers position, returns one item at a time, raises `StopIteration` at the end. Can be consumed **only once**.

A `for` loop calls `iter()` then `next()` repeatedly behind the scenes.

```python
nums = [10, 20, 30]      # iterable
it = iter(nums)          # iterator
next(it)   # 10
next(it)   # 20
next(it)   # 30
# next(it) -> StopIteration
```

### How do you create a custom iterator?

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

list(CountDown(3))     # [3, 2, 1]
```

### What is a generator?

A generator is a function that uses **`yield`** instead of `return`. Each `yield` produces a value and **pauses** the function, saving its local state; the next `next()` resumes from there. It is the simplest way to create an iterator and is **lazy** (memory efficient).

```python
def read_errors(path):
    with open(path) as f:
        for line in f:
            if "ERROR" in line:
                yield line        # one line at a time

def steps():
    yield "open browser"
    yield "login"
    yield "logout"

g = steps()
next(g)   # 'open browser'
next(g)   # 'login'
```

### `yield` vs `return`?

| `return` | `yield` |
| --- | --- |
| Ends the function | Pauses the function, keeps state |
| Sends back one value | Produces a series of values |
| Normal function | Turns the function into a generator |

### Generator vs iterator?

| | Iterator | Generator |
| --- | --- | --- |
| How created | Class with `__iter__` + `__next__` | Function with `yield` or `( )` expression |
| Code | More boilerplate | Very little |
| State | Managed manually | Saved automatically |
| `StopIteration` | Raised manually | Raised automatically |
| Relation | — | Every generator **is** an iterator |

```python
import sys
sys.getsizeof([x for x in range(10**6)])   # ~8 MB
sys.getsizeof((x for x in range(10**6)))   # ~200 bytes
```

### What does `yield from` do?

It delegates to another iterable or generator, yielding all its values.

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```

### What is the `itertools` module used for?

Fast, memory-efficient iterator building blocks.

```python
from itertools import chain, islice, count, permutations, combinations, groupby
list(chain([1, 2], [3]))              # [1, 2, 3]
list(islice(count(10), 3))            # [10, 11, 12]
list(permutations("ab"))              # [('a','b'), ('b','a')]
list(combinations([1, 2, 3], 2))      # [(1,2), (1,3), (2,3)]
```

### What is `functools.lru_cache`?

A decorator that **caches results** of a function (memoisation), so repeated calls with the same arguments return instantly.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(100)      # instant instead of exponential time
```

## Object-Oriented Programming

### What are a class and an object?

- **Class** — a blueprint that defines attributes (data) and methods (behaviour).
- **Object** — an instance of a class, created from the blueprint.

```python
class Car:
    def __init__(self, brand):
        self.brand = brand
    def drive(self):
        return f"{self.brand} is driving"

c = Car("Tata")      # object / instance
c.drive()
```

### What are the four pillars of OOP?

- **Encapsulation** — bundle data and methods together and restrict direct access (`_protected`, `__private`, `@property`).
- **Abstraction** — show *what* an object does, hide *how* (`ABC` + `@abstractmethod`).
- **Inheritance** — a child class reuses and extends a parent class.
- **Polymorphism** — same method name, different behaviour per class.

### What is `__init__`? How is it different from `__new__`?

- `__new__` — **creates** the object (allocates it); called first; returns the instance. Rarely overridden (singletons, immutable subclasses).
- `__init__` — **initialises** the already-created object; sets attributes; returns `None`.

```python
class Car:
    def __new__(cls, *args):
        print("1. creating")
        return super().__new__(cls)
    def __init__(self, brand):
        print("2. initialising")
        self.brand = brand

Car("Tata")
```

### What is `self`?

`self` is a reference to the **current object**. Python passes it automatically as the first argument of instance methods: `obj.method()` becomes `Class.method(obj)`. `self` is a convention, not a keyword.

```python
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1

c = Counter(); c.increment()   # same as Counter.increment(c)
```

### Instance variables vs class (static) variables?

- **Instance variable** — `self.x`, unique to each object.
- **Class variable** — defined in the class body, **shared** by all objects.

```python
class Test:
    count = 0                 # class variable
    def __init__(self, name):
        self.name = name      # instance variable
        Test.count += 1

a, b = Test("login"), Test("logout")
a.name, b.name, Test.count    # ('login', 'logout', 2)
```

Trap: `a.count = 10` creates a **new instance variable** on `a`; `Test.count` is unchanged.

### Instance method vs class method vs static method?

| Type | First argument | Can access | Use when |
| --- | --- | --- | --- |
| Instance method | `self` | Instance + class data | Behaviour depends on object state |
| `@classmethod` | `cls` | Class data | Alternate constructors, factories |
| `@staticmethod` | None | Nothing automatic | Utility that logically belongs to the class |

```python
class Employee:
    company = "Deloitte"
    def __init__(self, name, salary):
        self.name, self.salary = name, salary

    def greet(self):                  # instance method
        return f"Hi, I am {self.name}"

    @classmethod
    def from_csv(cls, line):          # alternate constructor
        name, salary = line.split(",")
        return cls(name, int(salary))

    @staticmethod
    def is_valid_salary(amount):      # pure utility
        return amount > 0

e = Employee.from_csv("Ravi,50000")
Employee.is_valid_salary(100)         # True
```

### What is `@property`?

It lets you access a method **like an attribute** and add validation through getter/setter/deleter, without changing how callers use it.

```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):            # getter -> acc.balance
        return self._balance

    @balance.setter
    def balance(self, value):     # setter -> acc.balance = 50
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

acc = Account(100)
acc.balance = 50       # validated
```

### What is inheritance? What types exist?

Inheritance lets a child class acquire the attributes and methods of a parent class.

| Type | Shape |
| --- | --- |
| Single | `B(A)` |
| Multiple | `C(A, B)` |
| Multilevel | `C(B)`, `B(A)` |
| Hierarchical | `B(A)`, `C(A)` |
| Hybrid | Mix of the above |

```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
    def open(self, url):
        self.driver.get(url)

class LoginPage(BasePage):          # single inheritance
    def __init__(self, driver):
        super().__init__(driver)    # call parent constructor
    def login(self, user, pwd): ...
```

In automation, the **Page Object Model** uses this: every page inherits common actions from `BasePage`.

### What is `super()` and MRO?

- `super()` calls the **next class in the MRO**, usually the parent — used to extend rather than replace parent behaviour.
- **MRO (Method Resolution Order)** is the order Python searches classes for a method, computed by the **C3 linearisation** algorithm. See it with `Class.__mro__` or `Class.mro()`.

```python
class A:
    def hi(self): return "A"
class B(A):
    def hi(self): return "B"
class C(A):
    def hi(self): return "C"
class D(B, C):          # diamond problem
    pass

D().hi()     # 'B'
D.__mro__    # (D, B, C, A, object)
```

### What is polymorphism and duck typing?

**Polymorphism** — the same interface works with different types. **Duck typing** — Python cares whether an object **has the method**, not what class it is: "if it walks like a duck and quacks like a duck, it is a duck".

```python
class Chrome:
    def launch(self): return "Launching Chrome"
class Firefox:
    def launch(self): return "Launching Firefox"

for browser in (Chrome(), Firefox()):
    print(browser.launch())   # no common parent needed

len("abc"), len([1, 2]), len({"a": 1})   # built-in polymorphism
```

### What is encapsulation? `_a` vs `__a` vs `__a__`?

Encapsulation hides internal state and exposes controlled access. Python has **no true private** members; it uses naming conventions.

| Name | Meaning | Effect |
| --- | --- | --- |
| `_a` | Protected (convention) | Still accessible; signals internal use |
| `__a` | Private | **Name mangling** → stored as `_ClassName__a` |
| `__a__` | Dunder / magic | Reserved for Python special methods |

```python
class Bank:
    def __init__(self):
        self._branch = "BLR"
        self.__balance = 1000

b = Bank()
b._branch            # works
# b.__balance        # AttributeError
b._Bank__balance     # 1000 -> name mangling
```

### What is abstraction? What is an abstract class?

An **abstract class** cannot be instantiated and defines methods that **every subclass must implement**. Use the `abc` module.

```python
from abc import ABC, abstractmethod

class Browser(ABC):
    @abstractmethod
    def launch(self): ...

class Chrome(Browser):
    def launch(self):
        return "Chrome started"

Chrome().launch()
# Browser()   -> TypeError: Can't instantiate abstract class
```

### Method overloading vs method overriding?

- **Overloading** — same name, different parameters, same class. Python does **not support it directly**; the last definition wins. Achieve it with default args, `*args`, or `functools.singledispatchmethod`.
- **Overriding** — child class redefines a parent method with the same name. Fully supported.

```python
class Calc:                      # overloading via defaults
    def add(self, a, b=0, c=0):
        return a + b + c
Calc().add(1), Calc().add(1, 2), Calc().add(1, 2, 3)

class Parent:
    def show(self): return "Parent"
class Child(Parent):
    def show(self): return "Child"   # overriding
```

### What are dunder (magic) methods? What is operator overloading?

**Dunder methods** (`__init__`, `__len__`, `__add__`, `__eq__`, `__str__`) are special methods Python calls behind the scenes. **Operator overloading** means implementing those dunders so operators like `+`, `==`, `<` work with your class.

```python
class Money:
    def __init__(self, amt): self.amt = amt
    def __add__(self, other): return Money(self.amt + other.amt)  # +
    def __eq__(self, other):  return self.amt == other.amt        # ==
    def __lt__(self, other):  return self.amt < other.amt         # <
    def __len__(self):        return len(str(self.amt))           # len()
    def __str__(self):        return f"Rs {self.amt}"

print(Money(100) + Money(50))     # Rs 150
```

### `__str__` vs `__repr__`?

- `__str__` — **readable**, for end users; used by `print()` and `str()`.
- `__repr__` — **unambiguous**, for developers; used in the shell, lists and `repr()`. Ideally looks like code that recreates the object.

If only `__repr__` is defined, `print()` falls back to it.

```python
class User:
    def __init__(self, name): self.name = name
    def __str__(self):  return f"User {self.name}"
    def __repr__(self): return f"User(name={self.name!r})"

u = User("Ravi")
print(u)       # User Ravi
[u]            # [User(name='Ravi')]
```

### What is a dataclass?

`@dataclass` (Python 3.7+) auto-generates `__init__`, `__repr__` and `__eq__` for classes that mainly hold data.

```python
from dataclasses import dataclass, field

@dataclass
class TestResult:
    name: str
    passed: bool = True
    tags: list = field(default_factory=list)

r = TestResult("login")
print(r)    # TestResult(name='login', passed=True, tags=[])
```

### Composition vs inheritance?

- **Inheritance** — "is-a" relationship (`LoginPage` **is a** `BasePage`).
- **Composition** — "has-a" relationship; a class holds other objects (`Car` **has an** `Engine`).

Prefer composition when classes only need to **use** behaviour; it keeps coupling low.

```python
class Engine:
    def start(self): return "Engine on"

class Car:
    def __init__(self):
        self.engine = Engine()       # composition
    def start(self):
        return self.engine.start()
```

### What is `__slots__`?

`__slots__` declares a fixed set of attributes, which **saves memory** and blocks adding new attributes dynamically. Useful when creating millions of small objects.

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
# p.z = 3   -> AttributeError
```

### What is a metaclass?

A metaclass is the **class of a class** — it controls how classes are created. The default metaclass is `type`. Used in frameworks (ORMs, validation); rarely needed in application code.

```python
class Demo: pass
type(Demo)          # <class 'type'>
Dynamic = type("Dynamic", (), {"x": 1})   # create a class at runtime
```

### What is a singleton? How do you implement it?

A singleton allows **only one instance** of a class — for example a shared config or driver manager.

```python
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

Config() is Config()     # True
```
