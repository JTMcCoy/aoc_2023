from src.runner import daily_run
import time

day = 7

start = time.perf_counter_ns()
part1, part2 = daily_run(day)
end_t = time.perf_counter_ns()
print(part1)
print(part2)

print("Runtime: {:.3f}ms".format((end_t - start)/1e6))

input = {}
input[
    day
] = """"""

