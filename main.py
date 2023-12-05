from src.runner import daily_run
import time

day = 5

start = time.perf_counter_ns()
part1, part2 = daily_run(day)
end_t = time.perf_counter_ns()
print(part1)
print(part2)

print("Runtime: {:.3f}ms".format((end_t - start)/1e6))

input = {}
input[
    day
] = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
from src.utils import day_5_seed_loc

# get each double line as an entry
values = [[y.strip() for y in x.split(":")] for x in input[day].split("\n\n")]

dicts = {x[0]: [y.strip().split(" ") for y in x[1].split("\n")] for x in values}
seed_nums = [int(i) for i in dicts["seeds"][0]]
del dicts["seeds"]

# get the range of seed numbers:
seed_nums = [[i,j] for i, j in zip(seed_nums[0:None:2], seed_nums[1:None:2])]

lowest_loc = 1e50
for seed_range in seed_nums:
    seed_st = seed_range[0]
    seed_inc = seed_range[1]
    seed_nums_ = [seed_st + x for x in range(seed_inc)]
    loc_nums = day_5_seed_loc(seed_nums_, dicts)
    
    # find lowest loc_num:
    loc_nums.sort()
    
    if loc_nums[0] < lowest_loc:
        lowest_loc = loc_nums[0]
    del loc_nums

# try iterating over each seed number
print(lowest_loc)
