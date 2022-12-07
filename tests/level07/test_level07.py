import os
import sys

import networkx as nx
import pytest

import level07
import utils

td1 = os.path.join(os.path.dirname(__file__), 'in.txt')
# td1 = os.path.join(os.path.dirname(__file__), '../../level07/in.txt')
in_data = utils.read_file(td1)


@pytest.mark.skip(reason='Manual run to render')
@pytest.mark.skipif('matplotlib' not in sys.modules,
                    reason="requires Matplotlib library")
def test_render_1():
    import matplotlib.pyplot as plt
    fs, _ = level07.parse_input(in_data)
    pos = nx.nx_agraph.graphviz_layout(fs, prog="dot", args="")
    plt.figure(figsize=(50, 9), dpi=60)
    nx.draw(fs, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
    nx.draw_networkx_labels(fs, pos, bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round'),
                            horizontalalignment='left', verticalalignment='top')
    plt.show()


def test_input_parsing():
    fs, _ = level07.parse_input(in_data)
    assert fs.number_of_nodes() == 14


def test_directory_calculation():
    fs, root = level07.parse_input(in_data)
    # root node is not pre-calculated
    assert fs.nodes[root]['file_size'] == 0
    fs, root = level07.calc_directories(fs, root)
    # file sizes were calculated properly up to root node
    assert fs.nodes[root]['file_size'] == 48381165


def test_part1():
    fs, root = level07.parse_input(in_data)
    fs, _ = level07.calc_directories(fs, root)
    assert level07.p1(fs) == 95437


def test_part2():
    fs, root = level07.parse_input(in_data)
    fs, root = level07.calc_directories(fs, root)
    assert level07.p2(fs, root) == 24933642
