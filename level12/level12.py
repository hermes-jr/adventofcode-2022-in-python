import copy

import networkx as nx

from utils import Point2D
from utils import read_file


def p1(input_lines: list[str]) -> tuple[int, nx.DiGraph]:
    lines = copy.deepcopy(input_lines)
    h = len(lines)
    w = len(lines[0])

    graph = nx.DiGraph()
    start, end = None, None

    for y in range(h):
        for x in range(w):
            if lines[y][x] == 'S':
                lines[y] = lines[y].replace('S', 'a')
                start = Point2D(x, y)
            if lines[y][x] == 'E':
                lines[y] = lines[y].replace('E', 'z')
                end = Point2D(x, y)

    for y in range(0, h):
        for x in range(0, w):
            current = lines[y][x]
            if x + 1 < w:
                if ord(lines[y][x + 1]) - ord(current) <= 1:
                    graph.add_edge(Point2D(x, y), Point2D(x + 1, y), weight=1)
                if ord(current) - ord(lines[y][x + 1]) <= 1:
                    graph.add_edge(Point2D(x + 1, y), Point2D(x, y), weight=1)
            if y + 1 < h:
                if ord(lines[y + 1][x]) - ord(current) <= 1:
                    graph.add_edge(Point2D(x, y), Point2D(x, y + 1), weight=1)
                if ord(current) - ord(lines[y + 1][x]) <= 1:
                    graph.add_edge(Point2D(x, y + 1), Point2D(x, y), weight=1)

    # level_map = [list(line) for line in lines]
    # for p in list(nx.connected_components(graph))[0]:
    #     level_map[p.y][p.x] = 'A'
    # print('\n===========')
    # for i in level_map:
    #     print(''.join(i))
    # print('===========')

    return nx.dijkstra_path_length(graph, start, end), graph


def p2(input_lines: list[str], graph: nx.DiGraph) -> int:
    lines = copy.deepcopy(input_lines)

    h = len(lines)
    w = len(lines[0])

    end = None

    for y in range(h):
        for x in range(w):
            if lines[y][x] == 'S':
                lines[y] = lines[y].replace('S', 'a')
            if lines[y][x] == 'E':
                lines[y] = lines[y].replace('E', 'z')
                end = Point2D(x, y)

    graph = nx.reverse(graph)
    ssd = dict(nx.single_source_dijkstra_path_length(graph, end))
    result = max(ssd.values())
    for destination, distance in ssd.items():
        if lines[destination.y][destination.x] == 'a':
            result = min(result, distance)
    return result


if __name__ == "__main__":
    data_input = read_file("in.txt")
    result1, parsed_graph = p1(data_input)
    print("result1: {}".format(result1))
    result2 = p2(data_input, parsed_graph)
    print("result2: {}".format(result2))

u"""
--- Day 12: Hill Climbing Algorithm ---

You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

--- Part Two ---

As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

"""
