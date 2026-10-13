## Coding Round Programs

Say the approach and its complexity first, then write the code. Pythonic one-liners impress, but be ready to write the manual loop if asked "without built-ins".

### Reverse a string

```python
s = "automation"
s[::-1]                     # 'noitamotua'
"".join(reversed(s))

def reverse(s):             # without built-ins
    result = ""
    for ch in s:
        result = ch + result
    return result
```

### Check if a string is a palindrome

```python
def is_palindrome(s):
    s = "".join(ch.lower() for ch in s if ch.isalnum())
    return s == s[::-1]

is_palindrome("Madam")                           # True
is_palindrome("A man, a plan, a canal: Panama")  # True
```

### Reverse each word / reverse word order in a sentence

```python
s = "python is fun"
" ".join(s.split()[::-1])             # 'fun is python'
" ".join(w[::-1] for w in s.split())  # 'nohtyp si nuf'
```

### Count vowels in a string

```python
s = "Automation Testing"
sum(1 for ch in s.lower() if ch in "aeiou")   # 8
```

### Count frequency of each character / word

```python
from collections import Counter
text = "test pass test fail test"
Counter(text.split())          # Counter({'test': 3, 'pass': 1, 'fail': 1})

freq = {}                      # without Counter
for w in text.split():
    freq[w] = freq.get(w, 0) + 1
```

### Find the most frequent character

```python
from collections import Counter
Counter("banana").most_common(1)[0]   # ('a', 3)
```

### Find the first non-repeating character

```python
from collections import Counter
def first_unique(s):
    counts = Counter(s)
    for ch in s:
        if counts[ch] == 1:
            return ch
    return None

first_unique("swiss")      # 'w'
```

### Check if two strings are anagrams

```python
from collections import Counter
sorted("listen") == sorted("silent")       # True - O(n log n)
Counter("listen") == Counter("silent")     # True - O(n)
```

### Remove duplicates from a list (keep order)

```python
nums = [3, 1, 3, 2, 1]
list(dict.fromkeys(nums))      # [3, 1, 2] - keeps order
list(set(nums))                # order not guaranteed

seen, result = set(), []       # manual
for n in nums:
    if n not in seen:
        seen.add(n)
        result.append(n)
```

### Find duplicate elements in a list

```python
nums = [1, 2, 3, 2, 4, 1]
seen, dups = set(), set()
for n in nums:
    if n in seen:
        dups.add(n)
    seen.add(n)
print(dups)                    # {1, 2}

from collections import Counter
[k for k, v in Counter(nums).items() if v > 1]   # [1, 2]
```

### Find the second largest number

```python
nums = [10, 40, 30, 40, 20]
sorted(set(nums))[-2]          # 30

def second_largest(nums):      # single pass, O(n)
    first = second = float("-inf")
    for n in nums:
        if n > first:
            first, second = n, first
        elif first > n > second:
            second = n
    return second
```

### Find max and min without built-ins

```python
def find_max(nums):
    largest = nums[0]
    for n in nums[1:]:
        if n > largest:
            largest = n
    return largest
```

### Swap two numbers without a temporary variable

```python
a, b = 5, 10
a, b = b, a                    # Pythonic

a = a + b; b = a - b; a = a - b   # arithmetic way
```

### Fibonacci series

```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

list(fib(7))                   # [0, 1, 1, 2, 3, 5, 8]
```

### Factorial (iterative and recursive)

```python
def fact_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fact_rec(n):
    return 1 if n <= 1 else n * fact_rec(n - 1)

import math; math.factorial(5)   # 120
```

### Check if a number is prime / print primes up to n

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):   # check up to sqrt(n)
        if n % i == 0:
            return False
    return True

[n for n in range(1, 30) if is_prime(n)]
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

### Check Armstrong number

A number equal to the sum of its digits each raised to the number of digits (153 = 1³ + 5³ + 3³).

```python
def is_armstrong(n):
    digits = str(n)
    return n == sum(int(d) ** len(digits) for d in digits)

is_armstrong(153)     # True
```

### Sum of digits and reverse a number

```python
n = 1234
sum(int(d) for d in str(n))    # 10
int(str(n)[::-1])              # 4321

rev = 0                        # mathematical way
while n:
    rev = rev * 10 + n % 10
    n //= 10
```

### Find the missing number in 1..n

```python
nums = [1, 2, 4, 5, 6]
n = len(nums) + 1
n * (n + 1) // 2 - sum(nums)   # 3
```

### Two Sum: find indices of two numbers that add to a target

Use a dict of value → index for O(n).

```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i

two_sum([2, 7, 11, 15], 9)     # [0, 1]
```

### Flatten a nested list

```python
nested = [[1, 2], [3, 4], [5]]
[x for sub in nested for x in sub]      # one level

def flatten(lst):                        # any depth
    out = []
    for item in lst:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

flatten([1, [2, [3, 4]], 5])            # [1, 2, 3, 4, 5]
```

### Rotate a list by k positions

```python
nums, k = [1, 2, 3, 4, 5], 2
nums[-k:] + nums[:-k]          # [4, 5, 1, 2, 3]  right rotate
nums[k:] + nums[:k]            # [3, 4, 5, 1, 2]  left rotate
```

### Merge two sorted lists

```python
def merge(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]

merge([1, 3, 5], [2, 4])       # [1, 2, 3, 4, 5]
```

### Find common elements in two lists

```python
a, b = [1, 2, 3, 4], [3, 4, 5]
list(set(a) & set(b))          # [3, 4]
```

### Check balanced parentheses

Use a stack: push openers, pop and match on closers.

```python
def is_balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

is_balanced("{[()]}")      # True
is_balanced("([)]")        # False
```

### String compression (aaabb → a3b2)

```python
from itertools import groupby
s = "aaabbc"
"".join(f"{ch}{len(list(g))}" for ch, g in groupby(s))   # 'a3b2c1'
```

### Split a list into chunks of size n

```python
def chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

chunks([1, 2, 3, 4, 5], 2)     # [[1, 2], [3, 4], [5]]
```

### Transpose a matrix

```python
m = [[1, 2, 3], [4, 5, 6]]
[list(row) for row in zip(*m)]   # [[1, 4], [2, 5], [3, 6]]
```

### Bubble sort

Repeatedly swap adjacent items that are out of order. O(n²).

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:          # already sorted
            break
    return arr

bubble_sort([5, 2, 9, 1])        # [1, 2, 5, 9]
```

### Binary search

Works on a **sorted** list. Halve the search range each step. O(log n).

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

binary_search([1, 3, 5, 7, 9], 7)   # 3
```

### Print a pyramid pattern

```python
n = 4
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))
#    *
#   ***
#  *****
# *******
```

### FizzBuzz

```python
for i in range(1, 16):
    print("FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0
          else "Buzz" if i % 5 == 0 else i)
```

### Extract all numbers / emails from text using regex

```python
import re
text = "Order 42 shipped to ravi@test.com, 3 items"
re.findall(r"\d+", text)                  # ['42', '3']
re.findall(r"[\w.]+@[\w.]+", text)        # ['ravi@test.com']
re.sub(r"\d", "#", "pin 560001")          # 'pin ######'
```

`re.match` checks only at the **start**; `re.search` finds the **first match anywhere**; `re.findall` returns **all** matches.

## Output Prediction and Tricky Questions

### Mutable default argument

```python
def f(x, lst=[]):
    lst.append(x)
    return lst
print(f(1), f(2))
```

**Output:** `[1, 2] [1, 2]` — the same default list is shared and both calls return that one object.

### List multiplication with nested lists

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```

**Output:** `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]` — the three rows are the **same list object**. Fix: `[[0] * 3 for _ in range(3)]`.

### Late binding in closures

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
```

**Output:** `[2, 2, 2]` — `i` is looked up when called, not when created. Fix: `lambda i=i: i`.

### Modifying a list while iterating

```python
nums = [1, 2, 3, 4]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
print(nums)
```

**Output:** `[1, 3]` here by luck — removing shifts indexes and can skip elements (try `[2, 4]` → `[4]`). Fix: iterate over a copy `nums[:]` or use a comprehension.

### `is` vs `==` with integers

```python
a = 256; b = 256
print(a is b)
a = [1]; b = [1]
print(a == b, a is b)
```

**Output:** `True`, then `True False` — small ints are cached; lists are separate objects.

### Boolean is a subclass of int

```python
print(True + True, True == 1, isinstance(True, int))
d = {1: "a", True: "b"}
print(d)
```

**Output:** `2 True True` and `{1: 'b'}` — `True == 1` and they have the same hash, so they are the same key.

### Chained comparison and `and`/`or` return values

```python
print(1 < 2 < 3, 3 > 2 > 1 > 0, 1 == 1.0)
print(0 or [] or "x", 5 and 0)
```

**Output:** `True True True` and `x 0`.

### String and list immutability

```python
a = "hi"; b = a; b += "!"
x = [1]; y = x; y += [2]
print(a, x)
```

**Output:** `hi [1, 2]` — `+=` on a string creates a new object; on a list it mutates in place.

### Class variable shared through instances

```python
class A:
    items = []
a1, a2 = A(), A()
a1.items.append(1)
print(a2.items)
```

**Output:** `[1]` — `items` is a class variable shared by all instances. Fix: create `self.items = []` in `__init__`.

### `finally` overrides `return`

```python
def f():
    try:
        return "try"
    finally:
        return "finally"
print(f())
```

**Output:** `finally` — a `return` in `finally` wins (and swallows exceptions); avoid writing this.

### Slicing beyond range and negative steps

```python
s = [1, 2, 3, 4, 5]
print(s[10:], s[-2:], s[::-2], s[3:1])
```

**Output:** `[] [4, 5] [5, 3, 1] []` — slicing never raises IndexError.

### Variable scope: UnboundLocalError

```python
x = 10
def f():
    print(x)
    x = 5
f()
```

**Output:** `UnboundLocalError` — because `x` is assigned inside `f`, Python treats it as local for the **whole** function. Fix: `global x`, or don't reassign.

### Integer division and rounding

```python
print(7 // 2, -7 // 2, round(2.5), round(3.5), int(-3.7))
```

**Output:** `3 -4 2 4 -3` — `round` uses **banker's rounding** (to nearest even); `int()` truncates toward zero.
