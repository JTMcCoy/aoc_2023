from src.solutions import *
from src.utils import get_input

day_funcs = {
    1: (day_1_1, day_1_2),
    2: (day_2_1, day_2_2),
    3: (day_3_1, day_3_2),
    4: (day_4_1, day_4_2),
    5: (day_5_1, day_5_2),
    6: (day_6_1, day_6_2),
    7: (day_7_1, day_7_2),
    8: (day_8_1, day_8_2),
    9: (day_9_1, day_9_2),
    10: (day_10_1, day_10_2),
    11: (day_11_1, day_11_2),
    12: (day_12_1, day_12_2),
    13: (day_13_1, day_13_2),
    14: (day_14_1, day_14_2),
    15: (day_15_1, day_15_2),
    16: (day_16_1, day_16_2),
    17: (day_17_1, day_17_2),
    18: (day_18_1, day_18_2),
    19: (day_19_1, day_19_2),
    20: (day_20_1, day_20_2),
    21: (day_21_1, day_21_2),
    22: (day_22_1, day_22_2),
    23: (day_23_1, day_23_2),
    24: (day_24_1, day_24_2),
    25: (day_25_1, day_25_2),
}


def daily_run(day: int):
    values = get_input(day)
    part_1 = day_funcs[day][0](values)

    part_2 = day_funcs[day][1](values)

    return part_1, part_2
