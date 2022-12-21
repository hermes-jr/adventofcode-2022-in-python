import os

import level21
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    graph = level21.parse_input(in_data)
    assert level21.p1(graph) == 152


def test_part2():
    graph = level21.parse_input(in_data)
    assert level21.p2(graph) == 301
