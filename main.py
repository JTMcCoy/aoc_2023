from src.runner import daily_run
import time

day = 12

start = time.perf_counter_ns()
part1, part2 = daily_run(day)
end_t = time.perf_counter_ns()
print(part1)
print(part2)

print("Runtime: {:.3f}ms".format((end_t - start) / 1e6))

input = {}
input[
    day
] = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

# get each line as an entry
values = [x for x in input[day].split("\n")]

import itertools

springs = [x.split(" ")[0] for x in values]
grps = [[int(y) for y in x.split(" ")[1].replace(",", "")] for x in values]

# map springs to ints:
springs = [
    [y if y == "?" else int(y) for y in x.replace(".", "0").replace("#", "1")]
    for x in springs
]

combinations = 0
for spring, group in zip(springs, grps):
    # non-working springs in group:
    group_spr = sum(group)

    # non-working springs in spring:
    n_spr = sum([x for x in spring if x != "?"])

    # non_working springs to add:
    miss_spr = group_spr - n_spr

    # unknown springs:
    unknown_idx = [i for i, x in enumerate(spring) if x == "?"]
    n_un = len(unknown_idx)

    perm_list = [1] * miss_spr + [0] * (n_un - miss_spr)

    for perm in set([c for c in itertools.permutations(perm_list)]):
        for idx, perm_val in zip(unknown_idx, perm):
            spring[idx] = perm_val
        spr_groups = [
            sum(1 for _ in g) for val, g in itertools.groupby(spring) if val == 1
        ]
        if spr_groups == group:
            combinations += 1

print(combinations)
