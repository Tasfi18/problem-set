# Problem Set

Solutions to six algorithm problems in Python, written in competitive-programming style: each program reads all of standard input and prints the answers. No libraries are needed beyond the standard library.

| File | Problem | Technique |
| --- | --- | --- |
| `prob1.py` | A guide must take T tourists from city S to city D. Each road carries at most P people per trip, and the guide takes one seat. Find the fewest trips. Input ends with `0 0`. | Floyd–Warshall for the widest (max-min) path, then ⌈T / (capacity − 1)⌉ |
| `prob2.py` | A desk holds N items and requests arrive in order. Each request for an item not on the desk costs one preparation. Find the fewest preparations. | Optimal caching: evict the item needed furthest in the future (Belady) |
| `prob3.py` | A queue of IDs with two operations: `a x` adds `x` at the end, `r k` removes and prints the k-th item, or `none` if there isn't one. | Fenwick tree with binary search for the k-th item |
| `prob4.py` | Count the palindromic subsequences of a word. | Interval dynamic programming |
| `prob5.py` | A string is split into blocks of equal letters. Each step every block loses one letter; blocks that meet with the same letter join. Count the steps until the string is empty. | Min-heap of blocks with a running offset and a linked list for merging |
| `prob6.py` | Each number's value is the last digit of the sum of its digits, where odd digits count once and even digits twice. Add up the values of every number from A to B. | Digit dynamic programming |

## Run

```bash
python prob1.py < input.txt
python prob5.py < test5.txt
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

Each program is run on hundreds of random inputs and compared with a simple brute-force answer:
- every path for `prob1`
- every eviction choice for `prob2`
- a Python list for `prob3`
- every subsequence for `prob4`
- a step-by-step simulation for `prob5`
- every number for `prob6`

GitHub Actions runs the tests on every push.
