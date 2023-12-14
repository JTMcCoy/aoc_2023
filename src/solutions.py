import re
import math
import numpy as np
import itertools
from src.utils import (
    get_first_last_digits,
    day_3_dicts,
    day_5_seed_loc,
    day_5_in_out,
    day_6_dist,
    day_7_map_to_int,
    day_7_hands_dict,
    day_10_s_mapper,
    day_10_dir,
    day_10_next_pos,
    day_12_groups,
    day_12_perms,
    day_13_reflector,
)


def day_1_1(values: list):
    nums = get_first_last_digits(values)

    return sum(nums)


def day_1_2(values: list):
    sub_dict = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    pattern = re.compile(r"one|two|three|four|five|six|seven|eight|nine")
    nums = []
    for value in values:
        # use search to find index of string digits and place the value in front of it
        # repeated search from new starting points to find all occurences
        num = value
        # track length of string and of start point for search
        num_len = len(num)
        i = 0
        while i < num_len:
            matches = pattern.search(num, i)
            if matches:
                digit = matches.group()
                if matches.start() == 1:
                    num = num[0:1] + sub_dict[digit] + num[1:]
                elif matches.start() != 0:
                    num = (
                        num[0 : matches.start()]
                        + sub_dict[digit]
                        + num[matches.start() :]
                    )
                else:
                    num = sub_dict[digit] + num
                # we've added one element to the string, increment
                num_len += 1
                # start for next search needs to be two steps forwards
                i = matches.start() + 2
            else:
                i += 1
        nums.append(num)

    nums = get_first_last_digits(values)

    return sum(nums)


def day_2_1(values: list):
    max_cubes = {"red": 12, "green": 13, "blue": 14}

    # split on colon to get the game numbers as keys:
    games = {
        int(re.sub(r"[^0-9]| ", "", x.split(":")[0])): x.split(":")[1:][0]
        for x in values
    }

    game_sum = 0
    for game in games:
        # for now, replace semicolons with commas, as it doesn't matter which draw we're in:
        draws = re.sub(" ", "", re.sub(";", ",", games[game])).split(",")
        valid = True
        for draw in draws:
            for colour in max_cubes:
                if colour in draw:
                    if int(re.sub(colour, "", draw)) > max_cubes[colour]:
                        valid = False
                        break
        if valid:
            game_sum += game

    return game_sum


def day_2_2(values: list):
    # split on colon to get the game numbers as keys:
    games = {
        int(re.sub(r"[^0-9]| ", "", x.split(":")[0])): x.split(":")[1:][0]
        for x in values
    }

    game_sum = 0
    for game in games:
        # again, replace semicolons with commas, as it doesn't matter which draw we're in:
        draws = re.sub(" ", "", re.sub(";", ",", games[game])).split(",")

        # initialise how many we think could be in each colour with 0:
        min_cubes = {"red": 0, "green": 0, "blue": 0}

        for draw in draws:
            for colour in min_cubes:
                if colour in draw:
                    # we need to find the biggest number of each colour
                    colour_num = int(re.sub(colour, "", draw))
                    if colour_num > min_cubes[colour]:
                        min_cubes[colour] = colour_num
        power = 1
        for colour in min_cubes:
            power *= min_cubes[colour]

        game_sum += power
    return game_sum


def day_3_1(values: list):
    num_dict, sym_dict, _ = day_3_dicts(values)

    part_sum = 0
    for i in num_dict:
        for num in num_dict[i]:
            # look for symbols next to the numbers:
            start = num["span"][0]
            num_end = num["span"][1]
            if ((num_end) in sym_dict[i]) | ((start - 1) in sym_dict[i]):
                part_sum += num["num"]

            if (i > 0) & (i < (len(values) - 1)):
                # check rows above and below for adjacent or diagonal:
                adj = False
                for idx in range(start - 1, num_end + 1):
                    adj = adj | (idx in sym_dict[i - 1])
                    adj = adj | (idx in sym_dict[i + 1])
                if adj:
                    part_sum += num["num"]
            elif i == (len(values) - 1):
                # check rows above for adjacent or diagonal:
                adj = False
                for idx in range(start - 1, num_end + 1):
                    adj = adj | (idx in sym_dict[i - 1])
                if adj:
                    part_sum += num["num"]
            elif i == 0:
                # check rows below for adjacent or diagonal:
                adj = False
                for idx in range(start - 1, num_end + 1):
                    adj = adj | (idx in sym_dict[i + 1])
                if adj:
                    part_sum += num["num"]
    return part_sum


def day_3_2(values: list):
    num_dict, _, gear_dict = day_3_dicts(values)

    # find the asterisks adjacent to two numbers
    prod_sum = 0
    for i in gear_dict:
        for gear_pos in gear_dict[i]:
            gear_adj = 0
            gear_prod = 1

            # check for numbers next to this gear in the row:
            if i in num_dict.keys():
                for num in num_dict[i]:
                    # look for numbers next to the gears:
                    start = num["span"][0]
                    num_end = num["span"][1]
                    if (num_end) == gear_pos:
                        gear_prod *= num["num"]
                        gear_adj += 1
                    if (start - 1) == gear_pos:
                        gear_prod *= num["num"]
                        gear_adj += 1

            # check above and below:
            for other_row in [i - 1, i + 1]:
                if other_row in num_dict.keys():
                    for num in num_dict[other_row]:
                        # look for numbers above/below the gears:
                        start = num["span"][0]
                        num_end = num["span"][1]
                        num_range = [x for x in range(start - 1, num_end + 1)]

                        if gear_pos in num_range:
                            gear_prod *= num["num"]
                            gear_adj += 1

            if gear_adj == 2:
                prod_sum += gear_prod

    return prod_sum


def day_4_1(values: list):
    # separate into winning numbers and numbers we have:
    values = [
        [
            [int(z) for z in y.strip().replace("  ", " ").split(" ")]
            for y in x.split(":")[-1].split("|")
        ]
        for x in values
    ]

    # get number of winning numbers we have:
    lens = [len([y for y in x[1] if y in x[0]]) for x in values]

    # calculate score:
    scores = [2 ** (x - 1) for x in lens if x > 0]
    return sum(scores)


def day_4_2(values: list):
    # separate into winning numbers and numbers we have with card numbers:
    not_num_pattern = re.compile(r"[^0-9]+")
    cards = {
        int(re.sub(not_num_pattern, "", x.split(":")[0])): [
            [int(z) for z in y.strip().replace("  ", " ").split(" ")]
            for y in x.split(":")[-1].split("|")
        ]
        for x in values
    }

    # get number of winning numbers we have:
    lens = {x: len([y for y in cards[x][1] if y in cards[x][0]]) for x in cards}

    # loop through cards and add copies:
    cards_won = [1 for _ in lens]
    for card in lens:
        wins = range(card + 1, card + lens[card] + 1)
        for win_card in wins:
            cards_won[win_card - 1] += cards_won[card - 1]

    return sum(cards_won)


def day_5_1(values: tuple):
    dicts, seed_nums = values

    # iterating over each seed number
    loc_nums = day_5_seed_loc(seed_nums, dicts)

    # find lowest loc_num:
    loc_min = min(loc_nums)

    return loc_min


def day_5_2(values: tuple):
    dicts, seed_nums = values

    # get the range of seed numbers:
    seed_nums = [
        [i, i + j - 1] for i, j in zip(seed_nums[0:None:2], seed_nums[1:None:2])
    ]
    seed_nums.sort()

    # do a forward pass, converting the boundaries of each range into the output domain
    # also split the ranges where they intersect with the input defined ranges
    min_locs = []
    for bnd in seed_nums:
        bnds = list(set(bnd))
        bnds.sort()
        for x in dicts:
            # update the boundaries given the input ranges
            for row in dicts[x]:
                # split ranges given in_start and in_end:
                in_start = int(row[1])
                in_end = int(row[1]) + int(row[-1])
                if in_start > bnds[0]:
                    bnds = list(set(bnds + [in_start, in_start - 1]))
                    bnds.sort()
                if in_end < bnds[-1]:
                    bnds = list(set(bnds + [in_end, in_end + 1]))
                    bnds.sort()

            # project bnds to next dict's input:
            out_vals = []
            for in_val in bnds:
                out_vals.append(day_5_in_out(in_val, dicts[x]))

            # print(bnds)
            # print(out_vals)

            bnds = list(set(out_vals[:]))
            bnds.sort()

        # keep the minimum output:
        min_locs.append(min(bnds))

    return min(min_locs)


def day_6_1(values: list):
    # separate into lists of times and distances:
    values = [
        [int(y) for y in x.split(":")[-1].strip().split(" ")]
        for x in values.split("\n")
    ]

    ways = []
    for dur, dist_record in zip(values[0], values[1]):
        way = 0
        for hold in range(dur):
            dist = day_6_dist(hold, dur)
            if dist > dist_record:
                way += 1
        ways.append(way)

    prod = 1
    for way in ways:
        prod *= way
    return prod


def day_6_2(values: list):
    # separate into lists of times and distances:
    # remove all spaces, split into two numbers
    values = [int(x.split(":")[-1]) for x in re.sub(r" ", "", values).split("\n")]

    dur, dist_record = values[0], values[1]

    way = 0
    for hold in range(dur):
        dist = day_6_dist(hold, dur)
        if dist > dist_record:
            way += 1

    return way


def day_7_1(values: list):
    hands = day_7_hands_dict(values)

    hands_sorted = [(x, hands[x]["rank"], day_7_map_to_int(x)) for x in hands]
    hands_sorted.sort(key=lambda pair: (pair[1], pair[2]))

    # get list of bids and ranks:
    wins = [(i + 1) * int(hands[x[0]]["bid"]) for i, x in enumerate(hands_sorted)]
    return sum(wins)


def day_7_2(values: list):
    hands = day_7_hands_dict(values)

    # where J is present, update ranks:
    for x in [i for i in hands if "J" in hands[i]["cards"]]:
        j_idx = hands[x]["cards"].index("J")
        j_count = hands[x]["counts"][j_idx]

        if (4 in hands[x]["counts"]) | (5 in hands[x]["counts"]):
            # if it's four Js or 1 J and four other, it will be five of a kind:
            hands[x]["rank"] = 7
        elif (3 in hands[x]["counts"]) & (2 in hands[x]["counts"]):
            # either way this can be five of a kind:
            hands[x]["rank"] = 7
        elif (3 in hands[x]["counts"]) & (2 not in hands[x]["counts"]):
            # 3 Js and two others, or a triple and a J: four of a kind:
            hands[x]["rank"] = 6
        elif 2 in hands[x]["counts"]:
            if (len(hands[x]["counts"]) == 3) & (j_count == 2):
                # pair and two Js, can become four of a kind
                hands[x]["rank"] = 6
            elif (len(hands[x]["counts"]) == 3) & (j_count == 1):
                # it's two pairs, one J, full house
                hands[x]["rank"] = 5
            else:
                # J pair, or pair and J, becomes three of a kind:
                hands[x]["rank"] = 4
        else:
            # a J and four others, one pair:
            hands[x]["rank"] = 2

    hands_sorted = [(x, hands[x]["rank"], day_7_map_to_int(x, part=2)) for x in hands]
    hands_sorted.sort(key=lambda pair: (pair[1], pair[2]))

    # get list of bids and ranks:
    wins = [(i + 1) * int(hands[x[0]]["bid"]) for i, x in enumerate(hands_sorted)]
    return sum(wins)


def day_8_1(values: tuple):
    inst, seq = values

    # iterate over the dict until we find ZZZ:
    len_inst = len(inst)
    step = 0
    rpt = 0
    found = False
    prev_loc = "AAA"
    while not found:
        if step == len_inst:
            rpt += 1
            step = step - len_inst
        next_loc = seq[prev_loc][inst[step]]
        step += 1
        if next_loc == "ZZZ":
            found = True
        else:
            prev_loc = next_loc

    return rpt * len_inst + step


def day_8_2(values: tuple):
    inst, seq = values

    # nodes that end with A
    start_nodes = [x for x in seq if x[-1] == "A"]

    # find the first detection for each starting node
    # for some reason, the number of steps is the least common multiple
    # of the first detections... they must be cyclic graphs?
    len_inst = len(inst)
    first_det = []
    for node in start_nodes:
        step = 0
        rpt = 0
        found = False
        prev_loc = node
        while not found:
            if step == len_inst:
                rpt += 1
                step = step - len_inst
            next_loc = seq[prev_loc][inst[step]]
            step += 1
            if next_loc[-1] == "Z":
                first_det.append(rpt * len_inst + step)
                found = True
            else:
                prev_loc = next_loc

    return math.lcm(*first_det)


def day_9_1(values: list):
    val_sum = 0  # total for sum of next values, part 1
    prev_val = 0  # total for sum of previous values, part 2
    for row in values:
        diff = row[:]
        prev_diff = 0
        neg = -1
        while diff:
            val_sum += diff[-1]
            diff = [x - y for x, y in zip(diff[1:], diff)]
            if diff:
                prev_diff += neg * diff[0]
                neg *= -1  # sign changes each row
        prev_val += row[0] + prev_diff

    return val_sum, prev_val


def day_9_2(values: list):
    # done in part 1
    return


def day_10_1(values: list):
    # split into each element:
    m = [x for x in values]

    s_pos, d = day_10_s_mapper(m)

    # first step is to the first starting points:
    steps = 1
    prev_pos = [s_pos, s_pos]
    cur_pos = day_10_next_pos(s_pos, d)
    found = False
    while not found:
        # take a step from each position:
        next_pos = []
        for pos, prv in zip(cur_pos, prev_pos):
            next_pos += [
                x
                for x in day_10_next_pos(pos, day_10_dir(m[pos[0]][pos[1]]))
                if x != prv
            ]
        if next_pos[0] == next_pos[1]:
            found = True
        else:
            prev_pos = cur_pos
            cur_pos = next_pos
            steps += 1

    return steps


def day_10_2(values: list):
    # split into each element:
    m = [x for x in values]

    s_pos, d = day_10_s_mapper(m)

    # get the ids of each location in loop:
    loop_ids = [s_pos]

    # first step is to the first starting points:
    steps = 1
    prev_pos = [s_pos, s_pos]
    cur_pos = day_10_next_pos(s_pos, d)
    found = False
    while not found:
        # take a step from each position:
        next_pos = []
        for pos, prv in zip(cur_pos, prev_pos):
            next_pos += [
                x
                for x in day_10_next_pos(pos, day_10_dir(m[pos[0]][pos[1]]))
                if x != prv
            ]
        if next_pos[0] == next_pos[1]:
            loop_ids.append(next_pos[0])
            found = True
        else:
            loop_ids += next_pos
            prev_pos = cur_pos
            cur_pos = next_pos
            steps += 1
    return loop_ids


def day_11_1(values: list):
    # get an int with space as 0 and galaxy as 1:
    values = np.array(
        [[int(y) for y in x.replace(".", "0").replace("#", "1")] for x in values]
    )

    # all 0 rows and columns:
    exp_rows = [i for i, x in enumerate(values.sum(axis=1)) if x == 0]
    exp_cols = [i for i, x in enumerate(values.sum(axis=0)) if x == 0]

    # add cols of zeros from back to front:
    for col in reversed(exp_cols):
        values = np.concatenate(
            [values[:, 0:col], np.zeros(shape=(values.shape[0], 1)), values[:, col:]],
            axis=1,
        )

    # add rows of zeros from back to front:
    for row in reversed(exp_rows):
        values = np.concatenate(
            [values[0:row, :], np.zeros(shape=(1, values.shape[1])), values[row:, :]],
            axis=0,
        )

    # number each position:
    values = values.cumsum().reshape(values.shape) * values

    # distance between galaxies is sum of distance in rows and columns...
    galaxies = np.argwhere(values)
    dist = 0
    for i, gal1 in enumerate(galaxies):
        for gal2 in galaxies[i:]:
            dist += np.abs(gal2[0] - gal1[0]) + np.abs(gal2[1] - gal1[1])

    return dist


def day_11_2(values: list):
    # get an int with space as 0 and galaxy as 1:
    values = np.array(
        [[int(y) for y in x.replace(".", "0").replace("#", "1")] for x in values]
    )

    # all 0 rows and columns:
    exp_rows = [i for i, x in enumerate(values.sum(axis=1)) if x == 0]
    exp_cols = [i for i, x in enumerate(values.sum(axis=0)) if x == 0]

    zero_mult = 1e6

    # number each position:
    values = values.cumsum().reshape(values.shape) * values

    # distance between galaxies is sum of distance in rows and columns
    # add in the expanded distances
    galaxies = np.argwhere(values)
    dist = 0
    for i, gal1 in enumerate(galaxies):
        for gal2 in galaxies[i:]:
            # rows which will be expanded:
            rows_sorted = sorted([gal1[0], gal2[0]])
            cols_sorted = sorted([gal1[1], gal2[1]])
            rows = [x for x in exp_rows if x in range(rows_sorted[0], rows_sorted[1])]
            cols = [x for x in exp_cols if x in range(cols_sorted[0], cols_sorted[1])]
            dist += (
                np.abs(gal2[0] - gal1[0])
                + np.abs(gal2[1] - gal1[1])
                + (zero_mult - 1) * (len(rows + cols))
            )
    return int(dist)


def day_12_1(values: list):
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

        # perm_list = day_12_perms(miss_spr, n_un)

        # # TODO this iterates over too many permutations, need to be able to prune
        # for perm in perm_list:
        #     for idx, perm_val in zip(unknown_idx, perm):
        #         spring[idx] = perm_val
        #     if group == day_12_groups(spring):
        #         combinations += 1

    return combinations


def day_12_2(values: list):
    return


def day_13_1(values: list):
    col_sum = 0
    row_sum = 0

    # for each pattern, get the number of columns/rows before the reflection
    for pattern in values:
        pattern_sums = day_13_reflector(pattern)
        col_sum += pattern_sums[0]
        row_sum += pattern_sums[1]

    return col_sum + 100 * row_sum


def day_13_2(values: list):
    col_sum = 0
    row_sum = 0
    for pattern in values:
        # get the Part 1 locations
        pattern_sums = day_13_reflector(pattern)
        cols_ignore = pattern_sums[2]
        rows_ignore = pattern_sums[3]

        # look at other candidates: either identical pairs,
        # or pairs that are off by one.
        # Exclude the detections from Part 1
        candidate_cols = [
            x[0] + 1
            for x in np.argwhere(
                np.sum(pattern[:, 1:] != pattern[:, 0:-1], axis=0) <= 1
            )
            if (x[0] + 1) not in cols_ignore
        ]
        candidate_rows = [
            x[0] + 1
            for x in np.argwhere(
                np.sum(pattern[1:, :] != pattern[0:-1, :], axis=1) <= 1
            )
            if (x[0] + 1) not in rows_ignore
        ]

        # find the location of the smudge:
        smudge_found = False
        row_found = []
        col_found = []
        while not smudge_found:
            for col in candidate_cols:
                h_splits = np.array_split(pattern, np.array([col]), axis=1)
                cols = min([x.shape[1] for x in h_splits])
                mismatch = np.argwhere(
                    np.flip(h_splits[0], axis=1)[:, 0:cols] != h_splits[1][:, 0:cols]
                )
                if len(mismatch) == 1:
                    # there is just one change to make
                    smudge_loc = [mismatch[0, 0], col - mismatch[0, 1] - 1]
                    col_found.append(col)
                    smudge_found = True
                    break

            for row in candidate_rows:
                v_splits = np.array_split(pattern, np.array([row]), axis=0)
                rows = min([x.shape[0] for x in v_splits])
                mismatch = np.argwhere(
                    np.flip(v_splits[0], axis=0)[0:rows, :] != v_splits[1][0:rows, :]
                )
                if len(mismatch) == 1:
                    # there is just one change to make
                    smudge_loc = [row - mismatch[0, 0] - 1, mismatch[0, 1]]
                    row_found.append(row)
                    smudge_found = True
                    break

        # update pattern at the location of the smudge:
        if pattern[smudge_loc[0], smudge_loc[1]] == 0:
            pattern[smudge_loc[0], smudge_loc[1]] = 1
        else:
            pattern[smudge_loc[0], smudge_loc[1]] = 0

        # ignore pairs from Part 1, and from the search above
        # which weren't the smudge location
        cols_ignore = [x for x in cols_ignore + candidate_cols if x not in col_found]
        rows_ignore = [x for x in rows_ignore + candidate_rows if x not in row_found]

        # add to the count of cols and rows
        pattern_sums = day_13_reflector(
            pattern, cols_ignore=cols_ignore, rows_ignore=rows_ignore
        )
        col_sum += pattern_sums[0]
        row_sum += pattern_sums[1]
    return col_sum + 100 * row_sum


def day_14_1(values: list):
    # naive approach, go for each column
    rocks = [0 for _ in values]
    for col_i in range(len(values[0])):
        col = [x[col_i] for x in values]

        last_sq = 0
        idx = 0 if "O" in col else len(col)
        while idx < len(col):
            # location of next
            if "#" in col[last_sq:]:
                idx = col[last_sq:].index("#") + last_sq
            else:
                idx = len(col[last_sq:]) + last_sq

            # number of 0s up to that square rock:
            col_rocks = len([x for x in col[last_sq:idx] if x == "O"])
            for row in range(col_rocks):
                rocks[row + last_sq] += 1

            last_sq = idx + 1

    return sum([(i + 1) * x for i, x in enumerate(reversed(rocks))])


def day_14_2(values: list):
    return


def day_15_1(values: list):
    return


def day_15_2(values: list):
    return


def day_16_1(values: list):
    return


def day_16_2(values: list):
    return


def day_17_1(values: list):
    return


def day_17_2(values: list):
    return


def day_18_1(values: list):
    return


def day_18_2(values: list):
    return


def day_19_1(values: list):
    return


def day_19_2(values: list):
    return


def day_20_1(values: list):
    return


def day_20_2(values: list):
    return


def day_21_1(values: list):
    return


def day_21_2(values: list):
    return


def day_22_1(values: list):
    return


def day_22_2(values: list):
    return


def day_23_1(values: list):
    return


def day_23_2(values: list):
    return


def day_24_1(values: list):
    return


def day_24_2(values: list):
    return


def day_25_1(values: list):
    return


def day_25_2(values: list):
    return
