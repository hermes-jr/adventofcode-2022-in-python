import os

import level17
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
# td1 = os.path.join(os.path.dirname(__file__), '../../level17/in.txt')
in_data = utils.read_file(td1)[0]


def test_part1():
    assert level17.p1(in_data) == 3068


# def test_part2():
#     assert level17.p2(in_data) == 1514285714288
