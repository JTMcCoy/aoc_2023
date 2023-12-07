from data.input_data import input
from collections import Counter

import re


def get_input(day: int) -> list:
    if day == 5:
        # get each double line as an entry
        values = [[y.strip() for y in x.split(":")] for x in input[day].split("\n\n")]
    elif day == 6:
        values = re.sub(r" +", " ", input[day])
    else:
        # get each line as an entry
        values = [x for x in input[day].split("\n")]

    return values


def day_3_dicts(
    values,
):
    num_pattern = re.compile(r"[0-9]+")
    symbol_pattern = re.compile(r"[^0-9|^.]")
    gear_pattern = re.compile(r"[*]")

    # we need to check if each number has a symbol next to it or if the row above or below has a symbol
    num_dict = {}
    sym_dict = {}
    gear_dict = {}
    for row_i, row in enumerate(values):
        num_dict[row_i] = []
        sym_dict[row_i] = []
        gear_dict[row_i] = []

        # get positions of symbols in each row:
        i = 0
        while i <= len(row):
            sym_match = symbol_pattern.search(row, i)
            if sym_match:
                sym_dict[row_i].append(sym_match.start())
                i = sym_match.start() + 1
            else:
                break

        # get each number in the row:
        i = 0
        while i <= len(row):
            num_match = num_pattern.search(row, i)
            if num_match:
                num_dict_i = {}
                num_dict_i["span"] = num_match.span()
                num_dict_i["num"] = int(num_match.group())
                num_dict[row_i].append(num_dict_i)
                i = num_match.end()
            else:
                break

        # get positions of gears in each row:
        i = 0
        while i <= len(row):
            gear_match = gear_pattern.search(row, i)
            if gear_match:
                gear_dict[row_i].append(gear_match.start())
                i = gear_match.start() + 1
            else:
                break
    return num_dict, sym_dict, gear_dict


def get_first_last_digits(values: list) -> list:
    # we need to extract the digits and remove the strings
    nums = [re.sub(r"[^0-9]", "", x) for x in values]

    # we need the first and last digit for each
    nums = [int(x[0] + x[-1]) for x in nums]

    return nums


def day_5_seed_loc(seed_nums: list, dicts: dict):
    loc_nums = []
    for seed in seed_nums:
        prev_num = seed
        for x in dicts:
            prev_num = day_5_in_out(prev_num, dicts[x])
        loc_nums.append(prev_num)

    return loc_nums


def day_5_in_out(in_val: int, map_dict: dict) -> int:
    # given an input, map to output
    output = in_val
    for row in map_dict:
        if (in_val >= int(row[1])) & (in_val < (int(row[1]) + int(row[-1]))):
            output = int(row[0]) + (in_val - int(row[1]))
            break

    return output


def day_6_dist(hold: int, dur: int) -> int:
    # dist = speed*(dur-hold)
    # speed = hold
    dist = hold * (dur - hold)

    return dist


def day_7_map_to_int(str_in: str, part: int = 1) -> list:
    map_dict = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11 if part == 1 else 1,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    output = [map_dict[x] for x in str_in]

    return output


def day_7_hands_dict(values: list) -> dict:
    # separate into hands and bids:
    hands = {x.split()[0]: x.split()[1] for x in values}

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
                hands[x]["rank"] = 2
        else:
            hands[x]["rank"] = 1
    return hands
