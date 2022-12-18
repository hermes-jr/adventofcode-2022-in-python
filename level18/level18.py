from typing import Generator

import networkx as nx

from utils import read_file, Point3D


def p1(graph: nx.Graph) -> int:
    result = 0
    for n in graph.nodes():
        e = graph.edges(n)
        result += 6 - len(e)
    return result


def p2(graph: nx.Graph) -> int:
    """
    Fill all volume with water with a little margin, BFS through water voxels
    """
    water = nx.Graph()
    lava = set(graph.nodes)
    o = next(iter(lava))
    d1 = Point3D(o.x, o.y, o.z)
    d2 = Point3D(o.x, o.y, o.z)
    for n in lava:
        d1.x = min(n.x - 1, d1.x)
        d1.y = min(n.y - 1, d1.y)
        d1.z = min(n.z - 1, d1.z)
        d2.x = max(n.x + 2, d2.x)
        d2.y = max(n.y + 2, d2.y)
        d2.z = max(n.z + 2, d2.z)

    for i in range(d1.z, d2.z):
        for j in range(d1.y, d2.y):
            for k in range(d1.x, d2.x):
                next_point = Point3D(k, j, i)
                if next_point in lava:
                    continue
                water.add_node(next_point)
                for nbr in neighbors(next_point):
                    if water.has_node(nbr):
                        water.add_edge(nbr, next_point)

    # print('Total volume', d1, d2)
    # print('Water:', water)

    result = 0
    for next_point in nx.bfs_tree(water, d1):
        for nbr in neighbors(next_point):
            if nbr in lava:
                result += 1

    return result


def parse_input(input_lines: list[str]) -> nx.Graph:
    result = nx.Graph()

    for line in input_lines:
        x, y, z = map(int, line.split(','))
        next_point = Point3D(x, y, z)
        result.add_node(next_point)
        for nbr in neighbors(next_point):
            if result.has_node(nbr):
                result.add_edge(nbr, next_point)

    return result


def neighbors(p: Point3D) -> Generator[Point3D, None, None]:
    for d in {(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)}:
        yield Point3D(p.x + d[0], p.y + d[1], p.z + d[2])


if __name__ == "__main__":
    data_input = read_file("in.txt")
    result1 = p1(parse_input(data_input))
    print("result1: {}".format(result1))
    result2 = p2(parse_input(data_input))
    print("result2: {}".format(result2))

u"""
--- Day 18: Boiling Boulders ---

You and the elephants finally reach fresh air. You've emerged near the base of a large volcano that seems to be actively erupting! Fortunately, the lava seems to be flowing away from you and toward the ocean.

Bits of lava are still being ejected toward you, so you're sheltering in the cavern exit a little longer. Outside the cave, you can see the lava landing in a pond and hear it loudly hissing as it solidifies.

Depending on the specific compounds in the lava and speed at which it cools, it might be forming obsidian! The cooling rate should be based on the surface area of the lava droplets, so you take a quick scan of a droplet as it flies past you (your puzzle input).

Because of how quickly the lava is moving, the scan isn't very good; its resolution is quite low and, as a result, it approximates the shape of the lava droplet with 1x1x1 cubes on a 3D grid, each given as its x,y,z position.

To approximate the surface area, count the number of sides of each cube that are not immediately connected to another cube. So, if your scan were only two adjacent cubes like 1,1,1 and 2,1,1, each cube would have a single side covered and five sides exposed, a total surface area of 10 sides.

Here's a larger example:

2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5

In the above example, after counting up all the sides that aren't connected to another cube, the total surface area is 64.

What is the surface area of your scanned lava droplet?


--- Part Two ---

Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.

What is the exterior surface area of your scanned lava droplet?

"""
