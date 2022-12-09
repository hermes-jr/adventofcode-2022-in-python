import os

import level09

import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level09.p1(in_data) == 13

# def test_part2():
#     assert level09.p2(in_data) == 123
