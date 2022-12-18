import os

import utils
from level15 import level15

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_merge():
    v1 = level15.merge_neighbors([[1, 2], [2, 3]])
    assert v1[0] == [1, 3]
    v2 = level15.merge_neighbors([[2, 6], [7, 10]])
    assert v2[0] == [2, 10]
    v3 = level15.merge_neighbors([[1, 3], [5, 7], [6, 10]])
    assert v3 == [[1, 3], [5, 10]]
    v4 = level15.merge_neighbors([[1, 1], [5, 6], [10, 11]])
    assert v4 == [[1, 1], [5, 6], [10, 11]]


def test_part1():
    assert level15.p1(*level15.parse_input(in_data), target_line=10) == 26


def test_part2():
    assert level15.p2(level15.parse_input(in_data)[0], 20) == 56000011
