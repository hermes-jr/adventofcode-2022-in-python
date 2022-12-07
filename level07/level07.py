from enum import Enum

import networkx as nx

from utils import utils


class NodeType(Enum):
    FILE = 1
    DIRECTORY = 2


class FilesystemNode(object):

    def __init__(self, node_type: NodeType, name: str, size: int):
        self.node_type = node_type
        self.name = name
        self.size = size  # just for display, actual sizes are stored in the graph

    def __repr__(self):
        return "(FilesystemNode[{0},{1},{2}])".format(self.node_type, self.name, self.size)

    def __str__(self):
        return "[{0} {1}]".format(self.name, self.size)


def p1(fs: nx.Graph) -> int:
    result = 0
    for item in fs.nodes:
        file_size = fs.nodes[item]['file_size']
        if item.node_type == NodeType.DIRECTORY and file_size <= 100000:
            result += file_size
    return result


def p2(fs: nx.Graph, root: FilesystemNode) -> int:
    root_size = fs.nodes[root]['file_size']
    unused = 70000000 - root_size
    if __debug__:
        print("Currently unused: ", unused)
    to_freeup = 30000000 - unused
    if __debug__:
        print("To freeup:", to_freeup)
    smallest_sacrificial = root_size
    for item in fs.nodes:
        file_size = fs.nodes[item]['file_size']
        if item.node_type == NodeType.DIRECTORY and to_freeup <= file_size:
            smallest_sacrificial = min(file_size, smallest_sacrificial)
    return smallest_sacrificial


def parse_input(lines: list[str]) -> tuple[nx.Graph, FilesystemNode]:
    fs = nx.DiGraph()
    root = FilesystemNode(NodeType.DIRECTORY, '/', 0)
    fs.add_node(root, file_size=0)
    current_dir = root
    for line in lines:
        if line.startswith("$"):
            # handle action
            action = line[2:]
            if __debug__:
                print("Invoking action:", action)
            if action == 'ls':
                continue
            elif action == 'cd ..':
                if fs.predecessors(current_dir).__length_hint__() > 0:
                    current_dir = fs.predecessors(current_dir).__next__()
            elif action.startswith("cd "):
                next_dir_name = action[3:]
                if __debug__:
                    print("Traversing to subdir", next_dir_name)
                if next_dir_name == '/':
                    next_dir = root
                else:
                    next_dir = filter(lambda s: (s.name == next_dir_name and s.node_type == NodeType.DIRECTORY),
                                      fs.successors(current_dir)).__next__()
                current_dir = next_dir
            else:
                raise Exception('Command unknown')
        else:
            if line.startswith("dir "):
                # add directory
                dir_name = line[4:]
                if __debug__:
                    print("Adding directory", dir_name)
                dir_to_add = FilesystemNode(NodeType.DIRECTORY, dir_name, 0)
                fs.add_node(dir_to_add, file_size=0)
                fs.add_edge(current_dir, dir_to_add)
            else:
                # add file
                size, filename = line.split(' ')
                size = int(size)
                if __debug__:
                    print("Adding file {} with size {}".format(filename, size))
                file_to_add = FilesystemNode(NodeType.FILE, filename, size)
                fs.add_node(file_to_add, file_size=size)
                fs.add_edge(current_dir, file_to_add)

    if __debug__:
        print("FS:", fs.nodes(data=True))

    return fs, root


def calc_directories(fs: nx.Graph, root: FilesystemNode) -> tuple[nx.Graph, FilesystemNode]:
    paths = list(reversed(list(nx.edge_dfs(fs, root))))
    if __debug__:
        print("Walkthrough order:", paths)
    for item in paths:
        fs.nodes[item[0]]['file_size'] = fs.nodes[item[0]].get('file_size', 0) + fs.nodes[item[1]]['file_size']
    return fs, root


if __name__ == "__main__":
    data_input = utils.read_file("in.txt")
    i_fs, i_root = parse_input(data_input)
    i_fs, i_root = calc_directories(i_fs, i_root)
    result1 = p1(i_fs)
    print("result1: {}".format(result1))
    result2 = p2(i_fs, i_root)
    print("result2: {}".format(result2))

u"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?


--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?

"""
