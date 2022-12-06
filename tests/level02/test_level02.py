import os

import utils
from level02 import level02

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    assert level02.p1(in_data) == 15
