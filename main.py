from src.runner import daily_run
import time

day = 7

start = time.perf_counter_ns()
part1, part2 = daily_run(day)
end_t = time.perf_counter_ns()
print(part1)
print(part2)

print("Runtime: {:.3f}ms".format((end_t - start) / 1e6))

input = {}
input[
    day
] = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

# get each line as an entry
values = [x for x in input[day].split("\n")]

# separate into hands and bids:
hands = {x.split()[0]: x.split()[1] for x in values}

from collections import Counter
from src.utils import day_7_map_to_int

# use Counter to get count of each value
hands = {
    x: {
        "bid": hands[x],
        "cards": list(Counter(x).keys()),
        "counts": list(Counter(x).values()),
    }
    for x in hands
}

# rank using rules:
for x in hands:
    if 5 in hands[x]["counts"]:
        hands[x]["rank"] = 7
    elif 4 in hands[x]["counts"]:
        hands[x]["rank"] = 6
    elif (3 in hands[x]["counts"]) & (2 in hands[x]["counts"]):
        hands[x]["rank"] = 5
    elif (3 in hands[x]["counts"]) & (2 not in hands[x]["counts"]):
        hands[x]["rank"] = 4
    elif 2 in hands[x]["counts"]:
        if len(hands[x]["counts"]) == 3:
            # it's two pairs
            hands[x]["rank"] = 3
        else:
            # one pair
            hands[x]["rank"] = 2
    else:
        hands[x]["rank"] = 1

# 245344320 is too high
# where J is present, update ranks:
for x in [x for x in hands if "J" in hands[x]["cards"]]:
    j_idx = hands[x]["cards"].index("J")
    j_count = hands[x]["counts"][j_idx]

    if 4 in hands[x]["counts"]:
        # if it's four Js or 1 J and four other, it will be five of a kind:
        hands[x]["rank"] = 7
    elif (3 in hands[x]["counts"]) & (2 in hands[x]["counts"]):
        # either way this can be five of a kind:
        hands[x]["rank"] = 7
    elif 3 in hands[x]["counts"]:
        # 3 Js and two others, or a triple and a J: four of a kind:
        hands[x]["rank"] = 6
    elif 2 in hands[x]["counts"]:
        if (len(hands[x]["counts"]) == 3) & (j_count == 2):
            # it's two pairs, can become four of a kind
            hands[x]["rank"] = 6
        elif (len(hands[x]["counts"]) == 3) & (j_count == 1):
            # it's two pairs, one J, full house
            hands[x]["rank"] = 5
        else:
            # J pair, or pair and J, becomes three of a kind:
            hands[x]["rank"] = 4

hands_sorted = [(x, hands[x]["rank"], day_7_map_to_int(x, part=2)) for x in hands]
hands_sorted.sort(key=lambda pair: (pair[1], pair[2]))
# get list of bids and ranks:
wins = [(i + 1) * int(hands[x[0]]["bid"]) for i, x in enumerate(hands_sorted)]

print(sum(wins))
