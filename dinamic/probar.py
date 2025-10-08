import itertools
from typing import List, Tuple

def gamma(x: int) -> int:
    return 3 * x - 1

def precompute_student_info(students):
    info = []
    for s in students:
        prefs = sorted(s['prefs'], key=lambda t: -t[1])  # ordenar por prioridad
        m = len(prefs)
        priorities = [p for (_, p) in prefs]
        mats = [mat for (mat, _) in prefs]
        T = sum(priorities)
        sum_top = [0]
        running = 0
        for p in priorities:
            running += p
            sum_top.append(running)
        f = []
        gm = gamma(m) if m > 0 else 1
        for k in range(0, m + 1):
            if m == 0:
                f.append(0.0)
            else:
                val = (1.0 - (k / m)) * ((T - sum_top[k]) / gm)
                f.append(val)
        info.append({'m': m, 'mats': mats, 'f': f})
    return info

# ------------------ DP ------------------

def solve_dp(students, initial_caps):
    info = precompute_student_info(students)
    r = len(info)
    initial_caps = tuple(initial_caps)

    memo = {}
    choice = {}

    def dp(idx: int, caps: Tuple[int, ...]) -> float:
        if idx == r:
            return 0.0
        key = (idx, caps)
        if key in memo:
            return memo[key]

        student = info[idx]
        m = student['m']
        mats = student['mats']
        fvals = student['f']

        best = float("inf")
        best_k = 0
        best_caps = None

        for k in range(0, m + 1):
            feasible = True
            caps_list = list(caps)
            for t in range(k):
                mat_id = mats[t]
                if caps_list[mat_id] <= 0:
                    feasible = False
                    break
                caps_list[mat_id] -= 1
            if not feasible:
                continue
            caps2 = tuple(caps_list)
            val = fvals[k] + dp(idx + 1, caps2)
            if val < best:
                best = val
                best_k = k
                best_caps = caps2

        memo[key] = best
        choice[key] = (best_k, best_caps)
        return best

    min_cost = dp(0, initial_caps)

    # reconstrucción
    assignment = []
    idx = 0
    caps = initial_caps
    while idx < r:
        k, next_caps = choice[(idx, caps)]
        mats = info[idx]['mats'][:k]
        assignment.append((idx, mats))
        caps = next_caps
        idx += 1

    return min_cost, assignment

# ------------------ Fuerza bruta ------------------

def brute_force(students, caps):
    info = precompute_student_info(students)
    r = len(info)

    best = float("inf")
    best_assign = None

    def backtrack(idx, caps, current_cost, assign):
        nonlocal best, best_assign
        if idx == r:
            if current_cost < best:
                best = current_cost
                best_assign = assign[:]
            return

        student = info[idx]
        m = student['m']
        mats = student['mats']
        fvals = student['f']

        for k in range(0, m+1):
            feasible = True
            caps_list = list(caps)
            for t in range(k):
                mat_id = mats[t]
                if caps_list[mat_id] <= 0:
                    feasible = False
                    break
                caps_list[mat_id] -= 1
            if not feasible:
                continue
            assign.append((idx, mats[:k]))
            backtrack(idx+1, tuple(caps_list), current_cost + fvals[k], assign)
            assign.pop()

    backtrack(0, tuple(caps), 0.0, [])
    return best, best_assign

# ------------------ Ejemplo pequeño ------------------

if __name__ == "__main__":
    students = [
        {'prefs': [(0,5), (1,2), (2,1)]},
        {'prefs': [(0,4), (1,1), (2,3)]},
        {'prefs': [(1,3), (2,2)]},
        {'prefs': [(1,2), (2,3)]},
        {'prefs': [(0,3), (1,2),(2,3)]}
    ]
    caps = [3,4,2]

    min_dp, assign_dp = solve_dp(students, caps)
    min_brute, assign_brute = brute_force(students, caps)

    print("DP ->", min_dp, assign_dp)
    print("Brute ->", min_brute, assign_brute)
