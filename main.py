import unittest
import math


def parse(node: str) -> tuple[str, dict[str,str]]:
    match node.split():
        case (name, '=', left, right):
            left = left[1:-1]
            right = right[:-1]
            return (name, {'L': left, 'R':right})
        case other:
            raise Exception(f'Could not parse {other}')


def main(text: str) -> int:
    lines = text.splitlines()
    route = lines[0]
    nodes = lines[2:]
    nodes = map(parse, nodes)
    nodes = {n[0]: n[1] for n in nodes}
    print(f'{nodes=}')
    currents = []
    for node in nodes.items():
        if node[0].endswith('A'):
            currents.append(node)
    print(f'path_starts={currents}')
    count = 0
    path_z_indices = [[] for _ in currents]
    while all(map(lambda zs: len(zs) == 0, path_z_indices)):
        for i in range(len(currents)):
            current = currents[i]
            if current[0].endswith('Z'):
                path_z_indices[i].append(count)
            lr = route[count % len(route)]
            count += 1
            next = current[1][lr]
            currents[i] = (next, nodes[next])
    print(f'{path_z_indices=}')
    lowest_zs = [zs[0] for zs in path_z_indices]
    return math.lcm(*lowest_zs)


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    text = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''
    def test(self):
        self.assertEqual(6, main(self.text))
