import os

import level12
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
# td1 = os.path.join(os.path.dirname(__file__), '../../level12/in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level12.p1(in_data) == 31


def test_part2():
    assert level12.p2(in_data) == 29
