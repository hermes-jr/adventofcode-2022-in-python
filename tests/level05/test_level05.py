import os

import level05
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = level05.parse_data(utils.read_file(td1))

stacks = [
    ['Z', 'N'],
    ['M', 'C', 'D'],
    ['P']
]


def test_part1():
    result = level05.p1(stacks, in_data)
    assert result == "CMZ", "Part 1 works"


def test_part2():
    result = level05.p2(stacks, in_data)
    assert result == "MCD", "Part 2 works"
