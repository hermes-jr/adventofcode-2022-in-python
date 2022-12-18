import os

import level18
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level18.p1(level18.parse_input(in_data)) == 64


def test_part2():
    assert level18.p2(level18.parse_input(in_data)) == 58
