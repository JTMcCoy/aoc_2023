from data.input_data import input

import re


def get_input(day: int) -> list:
    if day == 5:
        # get each double line as an entry
        values = [[y.strip() for y in x.split(":")] for x in input[day].split("\n\n")]
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


def day_5_min_dest(map_dict: dict):
    inputs = [int(row[1]) for row in map_dict]
    outputs = [int(row[0]) for row in map_dict]

    # find input which minimises output:

    # find unmapped input which is smaller than smallest output:

    return
