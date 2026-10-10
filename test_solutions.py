"""Each solution is run as a program on generated input and compared with a brute force."""
import itertools
import math
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, text):
    result = subprocess.run([sys.executable, str(HERE / script)], input=text,
                            capture_output=True, text=True, check=True)
    return result.stdout


# ---------- prob1: fewest trips along the best-capacity route ----------

def best_capacity(n, edges, s, d):
    best = 0
    for length in range(n):
        for middle in itertools.permutations([v for v in range(1, n + 1) if v not in (s, d)], length):
            path = (s, *middle, d)
            caps = [max((p for a, b, p in edges if {a, b} == {u, v}), default=0) for u, v in zip(path, path[1:])]
            if all(caps):
                best = max(best, min(caps))
    return best


def test_prob1_sample():
    assert run("prob1.py", (HERE / "input.txt").read_text()) == "Scenario #1\nMinimum Number of Trips = 3\n\n"


def test_prob1_matches_brute_force():
    rng = random.Random(1)
    blocks, expected = [], []
    for case in range(1, 31):
        n = rng.randint(2, 5)
        edges = [(u, v, rng.randint(2, 30)) for u, v in itertools.combinations(range(1, n + 1), 2) if rng.random() < 0.6]
        if not edges:
            edges = [(1, 2, 5)]
        s, d = rng.sample(range(1, n + 1), 2)
        t = rng.randint(1, 100)
        blocks.append(f"{n} {len(edges)}\n" + "".join(f"{u} {v} {p}\n" for u, v, p in edges) + f"{s} {d} {t}\n")
        cap = best_capacity(n, edges, s, d)
        trips = math.ceil(t / (cap - 1)) if cap > 0 else 0
        expected.append(f"Scenario #{case}\nMinimum Number of Trips = {trips}\n\n")
    assert run("prob1.py", "".join(blocks) + "0 0\n") == "".join(expected)


# ---------- prob2: fewest preparations with N desk slots (optimal caching) ----------

def fewest_loads(n, requests):
    best = {frozenset(): 0}
    for v in requests:
        nxt = {}
        for desk, cost in best.items():
            if v in desk:
                options = [desk]
            elif len(desk) < n:
                options = [desk | {v}]
                cost += 1
            else:
                options = [(desk - {x}) | {v} for x in desk]
                cost += 1
            for o in options:
                nxt[o] = min(nxt.get(o, math.inf), cost)
        best = nxt
    return min(best.values())


def test_prob2_matches_brute_force():
    rng = random.Random(2)
    cases = [(rng.randint(1, 3), [rng.randint(1, 5) for _ in range(rng.randint(1, 10))]) for _ in range(60)]
    text = f"{len(cases)}\n" + "".join(f"{n} {len(r)}\n{' '.join(map(str, r))}\n" for n, r in cases)
    assert run("prob2.py", text).split() == [str(fewest_loads(n, r)) for n, r in cases]


# ---------- prob3: queue with "add" and "remove the k-th" ----------

def test_prob3_matches_a_list():
    rng = random.Random(3)
    text, expected = "40\n", []
    for case in range(1, 41):
        items = [rng.randint(1, 99) for _ in range(rng.randint(0, 6))]
        ops = [("a", rng.randint(1, 99)) if rng.random() < 0.4 else ("r", rng.randint(1, 8)) for _ in range(rng.randint(1, 10))]
        text += f"{len(items)} {len(ops)}\n{' '.join(map(str, items))}\n" + "".join(f"{o} {v}\n" for o, v in ops)
        expected.append(f"Case {case}:")
        queue = list(items)
        for o, v in ops:
            if o == "a":
                queue.append(v)
            elif v > len(queue):
                expected.append("none")
            else:
                expected.append(str(queue.pop(v - 1)))
    assert run("prob3.py", text).split("\n")[:-1] == expected


def test_prob3_handles_more_than_262143_slots():
    source = (HERE / "prob3.py").read_text().split("it=iter")[0]  # just the FenwickTree class
    namespace = {}
    exec(source, namespace)
    tree = namespace["FenwickTree"](300_000)
    tree.update(290_000, 1)
    assert tree.find_kth(1) == 290_000


# ---------- prob4: palindromic subsequences ----------

def palindromic_subsequences(word):
    count = 0
    for r in range(1, len(word) + 1):
        for idx in itertools.combinations(range(len(word)), r):
            s = "".join(word[i] for i in idx)
            count += s == s[::-1]
    return count


def test_prob4_matches_brute_force():
    rng = random.Random(4)
    words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 10))) for _ in range(40)]
    out = run("prob4.py", f"{len(words)}\n" + "\n".join(words) + "\n").splitlines()
    assert out == [f"Case {i}: {palindromic_subsequences(w)}" for i, w in enumerate(words, 1)]


# ---------- prob5: blocks that shrink by one each step and merge ----------

def steps_to_clear(s):
    runs = [[c, len(list(g))] for c, g in itertools.groupby(s)]
    steps = 0
    while runs:
        steps += 1
        merged = []
        for c, v in ([c, v - 1] for c, v in runs if v > 1):
            if merged and merged[-1][0] == c:
                merged[-1][1] += v
            else:
                merged.append([c, v])
        runs = merged
    return steps


def test_prob5_sample():
    assert run("prob5.py", (HERE / "test5.txt").read_text()).split() == ["3"]


def test_prob5_matches_a_step_by_step_simulation():
    rng = random.Random(5)
    words = ["".join(rng.choice("AB") for _ in range(rng.randint(1, 12))) for _ in range(200)]
    text = f"{len(words)}\n" + "".join(f"{len(w)} {w}\n" for w in words)
    assert run("prob5.py", text).split() == [str(steps_to_clear(w)) for w in words]


# ---------- prob6: digit sums over a range ----------

def digit_value(n):
    return sum(d if d % 2 else 2 * d for d in map(int, str(n))) % 10


def test_prob6_matches_brute_force():
    rng = random.Random(6)
    ranges = [sorted((rng.randint(0, 3000), rng.randint(0, 3000))) for _ in range(30)] + [[1, 9]]
    text = f"{len(ranges)}\n" + "".join(f"{a} {b}\n" for a, b in ranges)
    assert run("prob6.py", text).split() == [str(sum(digit_value(n) for n in range(a, b + 1))) for a, b in ranges]
