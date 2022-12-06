import os

import level04
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level04.p1(level04.parse_data(in_data)) == 2


def test_part2():
    assert level04.p2(level04.parse_data(in_data)) == 4
