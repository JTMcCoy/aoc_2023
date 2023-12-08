from src.runner import daily_run
import time

day = 8

start = time.perf_counter_ns()
part1, part2 = daily_run(day)
end_t = time.perf_counter_ns()
print(part1)
print(part2)

print("Runtime: {:.3f}ms".format((end_t - start) / 1e6))

input = {}
input[
    day
] = """"""

# get each line as an entry
values = [x for x in input[day].split("\n")]
