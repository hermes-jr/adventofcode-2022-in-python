import os

import level08
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_input_parsing():
    parsed_map = level08.parse_input(in_data)
    assert parsed_map[0][0] == 3
    assert parsed_map[0][1] == 0
    assert parsed_map[1][1] == 5
    assert parsed_map[3][4] == 9
    assert parsed_map[3][2] == 5


def test_scenic_score_calculation():
    parsed_map = level08.parse_input(in_data)
    assert level08.get_candidate_scenic_score(parsed_map, 2, 1) == 4
    assert level08.get_candidate_scenic_score(parsed_map, 2, 3) == 8


def test_part1():
    parsed_map = level08.parse_input(in_data)
    assert level08.p1(parsed_map) == 21


def test_part2():
    parsed_map = level08.parse_input(in_data)
    assert level08.p2(parsed_map) == 8
