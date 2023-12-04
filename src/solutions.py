import re
from src.utils import get_first_last_digits, day_3_dicts


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
    cards_won = {x: 1 for x in lens}
    for card in lens:
        wins = range(card + 1, card + lens[card] + 1)
        for win_card in wins:
            cards_won[win_card] += cards_won[card]

    return sum([cards_won[x] for x in cards_won])


def day_5_1(values: list):
    return


def day_5_2(values: list):
    return


def day_6_1(values: list):
    return


def day_6_2(values: list):
    return


def day_7_1(values: list):
    return


def day_7_2(values: list):
    return


def day_8_1(values: list):
    return


def day_8_2(values: list):
    return


def day_9_1(values: list):
    return


def day_9_2(values: list):
    return


def day_10_1(values: list):
    return


def day_10_2(values: list):
    return


def day_11_1(values: list):
    return


def day_11_2(values: list):
    return


def day_12_1(values: list):
    return


def day_12_2(values: list):
    return


def day_13_1(values: list):
    return


def day_13_2(values: list):
    return


def day_14_1(values: list):
    return


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
