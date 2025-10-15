# Logíca de la lectura de los datos y almacenaje de ellos
import os
from typing import Dict, List, Tuple


def gamma(x: int) -> int:
    """Priority cap function: γ(x) = 3x - 1."""
    return 3 * x - 1


def parse_input_file(path: str):
    """
    Parse a plain-text input file for the course-allocation project.

    Returns:
        - course_index_by_code (Dict[str, int]):
            Maps course code (e.g., "1001") to its index (0..k-1).
        - capacities (List[int]):
            capacities[i] is the capacity for the course at index i.
        - requests_by_student (Dict[str, List[Tuple[int, int]]]):
            For each student code, a list of (course_idx, priority) pairs.

    Validations performed (inline):
        1) For each student, number of requests s must be in [1..7].
        2) A student must not request the same course more than once.
        3) Each priority must be in [1..5].
        4) For each student, sum of priorities must satisfy sum ≤ γ(s) = 3*s - 1.

    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    idx = 0
    num_courses = int(lines[idx]); idx += 1

    course_index_by_code: Dict[str, int] = {}
    capacities: List[int] = []
    for i in range(num_courses):
        code, capacity = lines[idx].split(',')
        course_index_by_code[code] = i
        capacities.append(int(capacity))
        idx += 1

    num_students = int(lines[idx]); idx += 1  # kept for format parity, not otherwise used

    requests_by_student: Dict[str, List[Tuple[int, int]]] = {}
    while idx < len(lines):
        student_code, n_requests_str = lines[idx].split(',')
        idx += 1

        # CHECK 1: number of requests s in [1..7]
        s = int(n_requests_str)
        if not (1 <= s <= 7):
            raise ValueError(f"Student {student_code}: invalid number of requests: {s} (expected 1..7)")

        requests_by_student[student_code] = []
        priority_sum = 0  # for γ(s)
        seen_course_indices = set()  # to forbid duplicates for this student

        for _ in range(s):
            course_code, priority_str = lines[idx].split(',')
            idx += 1

            # map to course index (assumes course exists in the header)
            course_idx = course_index_by_code[course_code]

            # CHECK 2: no duplicated course requests per student
            if course_idx in seen_course_indices:
                raise ValueError(
                    f"Student {student_code}: repeated course request for {course_code}"
                )
            seen_course_indices.add(course_idx)

            # CHECK 3: priority in [1..5]
            p = int(priority_str)
            if not (1 <= p <= 5):
                raise ValueError(
                    f"Student {student_code}: priority out of range (1..5) for course {course_code}: {p}"
                )

            requests_by_student[student_code].append((course_idx, p))
            priority_sum += p

        # CHECK 4: sum of priorities ≤ γ(s) = 3s - 1
        if priority_sum > gamma(s):
            raise ValueError(
                f"Student {student_code}: priority sum {priority_sum} exceeds γ({s})={gamma(s)}"
            )

    return course_index_by_code, capacities, requests_by_student