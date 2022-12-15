import os

import level12
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    res1, _ = level12.p1(in_data)
    assert res1 == 31


def test_part2():
    _, parsed_graph = level12.p1(in_data)
    assert level12.p2(in_data, parsed_graph) == 29
