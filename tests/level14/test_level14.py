import os

import utils
from level14 import level14
from utils import Point2D

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_parser():
    occupied = level14.parse_input(in_data)
    checks = [
        Point2D(498, 4),
        Point2D(498, 5),
        Point2D(498, 6),
        Point2D(498, 9),
        Point2D(502, 7),
        Point2D(496, 9)
    ]
    for c in checks:
        assert c in occupied
    assert len(occupied) == 20


def test_part1():
    assert level14.p1(level14.parse_input(in_data)) == 24


def test_part2():
    assert level14.p2(level14.parse_input(in_data)) == 93
