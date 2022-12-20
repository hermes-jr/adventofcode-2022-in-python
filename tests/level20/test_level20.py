import os

import level20
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level20.p1(*level20.parse_input(in_data)) == 3


def test_part2():
    assert level20.p2(*level20.parse_input(in_data, 811589153)) == 1623178306
