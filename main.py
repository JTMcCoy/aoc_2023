from src.runner import daily_run
import time

day = 10

start = time.perf_counter_ns()
part1, part2 = daily_run(day)
end_t = time.perf_counter_ns()
print(part1)
print(part2)

print("Runtime: {:.3f}ms".format((end_t - start) / 1e6))

input = {}
input[
    day
] = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

# input[
#     day
# ] = """7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ"""

# get each line as an entry
values = [x for x in input[day].split("\n")]

# split into each element:
m = [x for x in values]

s_pos, row_d, col_d = day_10_s_mapper(m)

# check each possible vertical starting direction:
for v_dir in row_d:
    pos = list(s_pos)
    print(pos)
    
# check each possible horizontal starting direction:
for h_dir in col_d:
    print(h_dir)
