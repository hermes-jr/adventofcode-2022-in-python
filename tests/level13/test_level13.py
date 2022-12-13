import os

import level13
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    pkts = level13.parse_input(in_data)
    assert level13.p1(pkts) == 13


#def test_part2():
#    assert level13.p2(in_data) == 0
