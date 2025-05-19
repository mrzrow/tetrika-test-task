def parse_intervals(times: list[int]) -> list[tuple[int, int]]:
    return [(times[i], times[i + 1]) for i in range(0, len(times), 2)]

def clip_intervals(intervals: list[tuple[int, int]], start: int, end: int) -> list[tuple[int, int]]:
    result = []
    for a, b in intervals:
        if b > start and a < end:
            result.append((max(a, start), min(b, end)))
    return result

def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    intervals.sort()
    merged = [list(intervals[0])]
    for a, b in intervals[1:]:
        last = merged[-1]
        if a <= last[1]:
            last[1] = max(last[1], b)
        else:
            merged.append([a, b])
    return [(x, y) for x, y in merged]

def intersect_intervals(a: list[tuple[int, int]], b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end   = min(a[i][1], b[j][1])
        if start < end:
            result.append((start, end))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']

    pupil_raw = parse_intervals(intervals['pupil'])
    tutor_raw = parse_intervals(intervals['tutor'])

    pupil_clipped = clip_intervals(pupil_raw, lesson_start, lesson_end)
    tutor_clipped = clip_intervals(tutor_raw, lesson_start, lesson_end)

    pupil_merged = merge_intervals(pupil_clipped)
    tutor_merged = merge_intervals(tutor_clipped)

    common = intersect_intervals(pupil_merged, tutor_merged)

    return sum(end - start for start, end in common)


if __name__ == '__main__':
    tests = [
        {'intervals': {'lesson': [1594663200, 1594666800],
                       'pupil':  [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                       'tutor':  [1594663290, 1594663430, 1594663443, 1594666473]},
         'answer': 3117},
        {'intervals': {'lesson': [1594702800, 1594706400],
                       'pupil':  [1594702789, 1594704500, 1594702807, 1594704542,
                                  1594704512, 1594704513, 1594704564, 1594705150,
                                  1594704581, 1594704582, 1594704734, 1594705009,
                                  1594705095, 1594705096, 1594705106, 1594706480,
                                  1594705158, 1594705773, 1594705849, 1594706480,
                                  1594706500, 1594706875, 1594706502, 1594706503,
                                  1594706524, 1594706524, 1594706579, 1594706641],
                       'tutor':  [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
         'answer': 3577},
        {'intervals': {'lesson': [1594692000, 1594695600],
                       'pupil':  [1594692033, 1594696347],
                       'tutor':  [1594692017, 1594692066, 1594692068, 1594696341]},
         'answer': 3565},
    ]

    for i, test in enumerate(tests):
        res = appearance(test['intervals'])
        assert res == test['answer'], f'Тест {i} провален: получили {res}, ожидаем {test["answer"]}'
    print("Все тесты пройдены!")    
