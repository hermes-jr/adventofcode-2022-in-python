import os

import level03
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_to_points():
    assert level03.to_points('p') == 16
    assert level03.to_points('L') == 38
    assert level03.to_points('P') == 42
    assert level03.to_points('v') == 22
    assert level03.to_points('t') == 20
    assert level03.to_points('s') == 19


def test_part1():
    result = level03.p1(in_data)
    assert result == 157


def test_part2():
    result = level03.p2(in_data)
    assert result == 70
