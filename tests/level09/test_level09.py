import os

import level09
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
td2 = os.path.join(os.path.dirname(__file__), 'in2.txt')
in_data_1 = utils.read_file(td1)
in_data_2 = utils.read_file(td2)


def test_part1():
    assert level09.p1(in_data_1) == 13


def test_part2():
    assert level09.p2(in_data_1) == 1
    assert level09.p2(in_data_2) == 36
