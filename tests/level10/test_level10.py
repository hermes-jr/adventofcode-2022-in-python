import os

import level10
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
in_data = utils.read_file(td1)


def test_part1():
    count, _ = level10.p1(in_data)
    assert count == 13140


def test_part2():
    template = '##  ##  ##  ##  ##  ##  ##  ##  ##  ##  \n' \
               '###   ###   ###   ###   ###   ###   ### \n' \
               '####    ####    ####    ####    ####    \n' \
               '#####     #####     #####     #####     \n' \
               '######      ######      ######      ####\n' \
               '#######       #######       #######     \n'
    assert level10.p2(in_data) == template
