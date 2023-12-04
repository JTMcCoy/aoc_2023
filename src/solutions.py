import re
from data.input_data import input


def day_1_1(day: int):
    # get each line as an entry
    values = [x for x in input[day].split("\n")]

    # we need to extract the digits and remove the strings
    nums = [re.sub(r"[^0-9]", "", x) for x in values]

    # we need the first and last digit for each
    nums = [int(x[0] + x[-1]) for x in nums]

    return sum(nums)


def day_1_2(day: int):
    # get each line as an entry
    values = [x for x in input[day].split("\n")]

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

    nums = []
    for value in values:
        # use search to find index of string digits and place the value in front of it
        # repeated search from new starting points to find all occurences
        pattern = re.compile(r"one|two|three|four|five|six|seven|eight|nine")
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

    # we need to extract the digits and remove the strings
    nums = [re.sub(r"[^0-9]", "", x) for x in nums]

    # we need the first and last digit for each
    nums = [int(x[0] + x[-1]) for x in nums]

    return sum(nums)


def day_2_1(day: int):
    max_cubes = {"red": 12, "green": 13, "blue": 14}

    # get each line as an entry
    games = [x for x in input[day].split("\n")]

    # split on colon to get the game numbers as keys:
    games = {
        int(re.sub(r"[^0-9]| ", "", x.split(":")[0])): x.split(":")[1:][0]
        for x in games
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


def day_2_2(day: int):
    # get each line as an entry
    games = [x for x in input[day].split("\n")]

    # split on colon to get the game numbers as keys:
    games = {
        int(re.sub(r"[^0-9]| ", "", x.split(":")[0])): x.split(":")[1:][0]
        for x in games
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


def day_3_1(day: int):
    # get each line as an entry
    values = [x for x in input[day].split("\n")]

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


def day_3_2(day: int):
    # get each line as an entry
    values = [x for x in input[day].split("\n")]

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


def day_4_1(day: int):
    # get each line as an entry
    values = [x for x in input[day].split("\n")]

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


def day_4_2(day: int):
    # get each line as an entry
    values = [x for x in input[day].split("\n")]

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
    cards_won = {x: 1 for x in lens}
    for card in lens:
        wins = range(card + 1, card + lens[card] + 1)
        for win_card in wins:
            cards_won[win_card] += cards_won[card]

    return sum([cards_won[x] for x in cards_won])


def day_5_1(day: int):
    return


def day_5_2(day: int):
    return


def day_6_1(day: int):
    return


def day_6_2(day: int):
    return


def day_7_1(day: int):
    return


def day_7_2(day: int):
    return


def day_8_1(day: int):
    return


def day_8_2(day: int):
    return


def day_9_1(day: int):
    return


def day_9_2(day: int):
    return


def day_10_1(day: int):
    return


def day_10_2(day: int):
    return


def day_11_1(day: int):
    return


def day_11_2(day: int):
    return


def day_12_1(day: int):
    return


def day_12_2(day: int):
    return


def day_13_1(day: int):
    return


def day_13_2(day: int):
    return


def day_14_1(day: int):
    return


def day_14_2(day: int):
    return


def day_15_1(day: int):
    return


def day_15_2(day: int):
    return


def day_16_1(day: int):
    return


def day_16_2(day: int):
    return


def day_18_1(day: int):
    return


def day_18_2(day: int):
    return


def day_19_1(day: int):
    return


def day_19_2(day: int):
    return


def day_20_1(day: int):
    return


def day_20_2(day: int):
    return


def day_21_1(day: int):
    return


def day_21_2(day: int):
    return


def day_22_1(day: int):
    return


def day_22_2(day: int):
    return


def day_23_1(day: int):
    return


def day_23_2(day: int):
    return


def day_24_1(day: int):
    return


def day_24_2(day: int):
    return


def day_25_1(day: int):
    return


def day_25_2(day: int):
    return


def day_17_1(day: int):
    return


def day_17_2(day: int):
    return
