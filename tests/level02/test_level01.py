import level01
import utils
import os

td1 = os.path.join(os.path.dirname(__file__), 'in_01.txt')
in_data = level01.parse_data(utils.read_file(td1))


def test_part1():
    result, summed = level01.p1(in_data)
    assert result == 24000, "Part 1 works"


def test_part2():
    result, summed = level01.p1(in_data)
    assert level01.p2(summed) == 45000, "Part 2 works"
