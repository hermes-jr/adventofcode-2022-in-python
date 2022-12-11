import os

import level11
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level11.p1(level11.parse_input(in_data, False)) == 10605


def test_part2():
    assert level11.p2(level11.parse_input(in_data, True)) == 2713310158
