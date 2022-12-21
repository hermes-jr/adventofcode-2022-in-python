import decimal
from typing import List

from utils import read_file

context = decimal.getcontext()
import networkx as nx

root = 'root'
humn = 'humn'

funcs = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '/': lambda a, b: a / b,
    '*': lambda a, b: a * b,
}

inverse_funcs = {
    '+': '-',
    '-': '+',
    '/': '*',
    '*': '/'
}


def p1(graph: nx.DiGraph) -> int:
    bottom_up_calc(graph)
    values = nx.get_node_attributes(graph, 'value')
    return int(values[root])


def p2(graph: nx.DiGraph) -> int:
    bottom_up_calc(graph, root)
    values = nx.get_node_attributes(graph, 'value')
    n1, n2 = nx.neighbors(graph, root)
    n1_subtree = nx.dfs_tree(graph, n1)
    if humn in n1_subtree:
        candidate_root = n1
        target_value = values[n2]
        subtree = nx.subgraph(graph, n1_subtree)
    else:
        candidate_root = n2
        target_value = values[n1]
        subtree = nx.subgraph(graph, nx.dfs_tree(graph, candidate_root))

    if __debug__:
        print('to match: {} we have to rebalance {}'.format(target_value, subtree.nodes()))

    # find upper and lower boundaries
    low_diff = compare(candidate_root, 1, subtree, target_value)  # what if we should find a negative value?
    low_sign = low_diff / abs(low_diff)
    left_boundary = None
    right_boundary = 2
    # find upper and lower boundaries
    while True:
        test = compare(candidate_root, right_boundary, subtree, target_value)
        cur_sign = test / abs(test)
        if __debug__:
            print(right_boundary, '->', test)
        if low_sign != cur_sign:
            break  # overshot
        left_boundary = right_boundary
        right_boundary *= 2
    if __debug__:
        print('the answer must be between', left_boundary, 'and', right_boundary)

    # if low_sign > 0, invert search direction
    # binary search
    while left_boundary <= right_boundary:
        if __debug__:
            print('searching between', left_boundary, 'and', right_boundary)
        middle = (left_boundary + right_boundary) // 2
        test = compare(candidate_root, middle, subtree, target_value)
        if __debug__:
            print('testing', middle, '->', test)
        # again, too late and too lazy to optimize this:
        if test < 0:
            if low_sign < 0:
                left_boundary = middle + 1
            else:
                right_boundary = middle - 1
        elif test > 0:
            if low_sign < 0:
                right_boundary = middle - 1
            else:
                left_boundary = middle + 1
        else:
            return middle

    return -1  # fail


def compare(source, candidate_value, graph, target_value):
    if __debug__:
        print('Testing candidate value', candidate_value)
    values = nx.get_node_attributes(graph, 'value')
    values[humn] = candidate_value
    nx.set_node_attributes(graph, values, 'value')
    bottom_up_calc(graph, source)
    test = nx.get_node_attributes(graph, 'value')[source]
    return test - target_value


"""
def p2_reverse_attempt_failed_for_real_data(graph: nx.DiGraph) -> Decimal:
    # works for test but does not work for real data
    bottom_up_calc(graph)
    n1, n2 = nx.neighbors(graph, root)
    values = nx.get_node_attributes(graph, 'value')
    operations = nx.get_node_attributes(graph, 'operation')

    # which subtree has the target value
    n1_subtree = nx.dfs_tree(graph, n1)
    if humn in n1_subtree:
        target_value = values[n2]
    else:
        target_value = values[n1]
    if __debug__:
        print('Target value is:', target_value)

    # traverse to humn from root calculating its value with inverse functions
    path_to_humn = list(nx.dijkstra_path(graph, root, humn))
    for i, current in enumerate(path_to_humn[1:-1], start=1):
        next_hop = path_to_humn[i + 1]
        n1, n2 = nx.neighbors(graph, current)
        second_operand = values[n1] if n1 != next_hop else values[n2]
        # otv = int(target_value)
        otv = target_value
        direct_op = operations[current]
        inverse_op = inverse_funcs[direct_op]
        target_value = funcs[inverse_op](otv, second_operand)
        print('exploring {}, old target: {}, second_operand {}, operation {}, inverse {}, new target value {},'
              .format(current, otv, second_operand, direct_op, inverse_op, target_value))

    return target_value
"""


def bottom_up_calc(graph: nx.DiGraph, from_node=root):
    wt = reversed([node for node in nx.bfs_tree(graph, from_node) if graph.out_degree(node) > 0])
    values = nx.get_node_attributes(graph, 'value')
    operations = nx.get_node_attributes(graph, 'operation')
    for current in wt:
        neighbors = list(nx.neighbors(graph, current))
        v1 = values[neighbors[0]]
        v2 = values[neighbors[1]]
        if __debug__:
            print('Exploring junction {}, neighbors: {}, {} {} {}'
                  .format(current, neighbors, v1, operations[current], v2))
        op_result = funcs[operations[current]](v1, v2)
        values[current] = op_result
        if __debug__:
            print('op produced:', op_result)
    nx.set_node_attributes(graph, values, 'value')


def parse_input(input_lines: List[str]) -> nx.DiGraph:
    parsed = nx.DiGraph()
    for line in input_lines:
        lp, rp = line.split(': ')
        rps = rp.split(' ')
        if len(rps) == 1:
            parsed.add_node(lp, value=int(rps[0]))
        else:
            parsed.add_node(lp, operation=rps[1])
            parsed.add_edge(lp, rps[0])
            parsed.add_edge(lp, rps[2])

    if __debug__:
        print('parsed:', parsed)
        print(parsed.nodes)
        print(parsed.edges)
    return parsed


if __name__ == "__main__":
    data_input = read_file("in.txt")
    result1 = p1(parse_input(data_input))
    print("result1: {}".format(result1))
    result2 = p2(parse_input(data_input))
    print("result2: {}".format(result2))

u"""
--- Day 21: Monkey Math ---

The monkeys are back! You're worried they're going to try to steal your stuff again, but it seems like they're just holding their ground and making various monkey noises at you.

Eventually, one of the elephants realizes you don't speak monkey and comes over to interpret. As it turns out, they overheard you talking about trying to find the grove; they can show you a shortcut if you answer their riddle.

Each monkey is given a job: either to yell a specific number or to yell the result of a math operation. All of the number-yelling monkeys know their number from the start; however, the math operation monkeys need to wait for two other monkeys to yell a number, and those two other monkeys might also be waiting on other monkeys.

Your job is to work out the number the monkey named root will yell before the monkeys figure it out themselves.

For example:

root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32

Each line contains the name of a monkey, a colon, and then the job of that monkey:

    A lone number means the monkey's job is simply to yell that number.
    A job like aaaa + bbbb means the monkey waits for monkeys aaaa and bbbb to yell each of their numbers; the monkey then yells the sum of those two numbers.
    aaaa - bbbb means the monkey yells aaaa's number minus bbbb's number.
    Job aaaa * bbbb will yell aaaa's number multiplied by bbbb's number.
    Job aaaa / bbbb will yell aaaa's number divided by bbbb's number.

So, in the above example, monkey drzm has to wait for monkeys hmdt and zczc to yell their numbers. Fortunately, both hmdt and zczc have jobs that involve simply yelling a single number, so they do this immediately: 32 and 2. Monkey drzm can then yell its number by finding 32 minus 2: 30.

Then, monkey sjmn has one of its numbers (30, from monkey drzm), and already has its other number, 5, from dbpl. This allows it to yell its own number by finding 30 multiplied by 5: 150.

This process continues until root yells a number: 152.

However, your actual situation involves considerably more monkeys. What number will the monkey named root yell?

--- Part Two ---

Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

First, you got the wrong job for the monkey named root; specifically, you got the wrong math operation. The correct operation for monkey root should be =, which means that it still listens for two numbers (from the same two monkeys as before), but now checks that the two numbers match.

Second, you got the wrong monkey for the job starting with humn:. It isn't a monkey - it's you. Actually, you got the job wrong, too: you need to figure out what number you need to yell so that root's equality check passes. (The number that appears after humn: in your input is now irrelevant.)

In the above example, the number you need to yell to pass root's equality test is 301. (This causes root to get the same number, 150, from both of its monkeys.)

What number do you yell to pass root's equality test?

"""
