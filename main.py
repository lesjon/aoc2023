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
    z_indices = [[] for _ in currents]
    seens = [set() for _ in currents]
    repeats: list[int|None] = [None for _ in currents]
    count = 0
    while not all(repeats):
        print(f'{count}')
        for i in range(len(currents)):
            current = currents[i]
            print(f'{current=}')
            if current is None:
                continue
            lr = route[count % len(route)]
            next = current[1][lr]
            if current[0].endswith('Z'):
                z_indices[i].append(count)
            state = (count % len(route), current[0])
            if state in seens[i]:
                repeats[i] = count
                currents[i] = None
            else:
                seens[i].add(state)
            currents[i] = (next, nodes[next])
        count += 1
    print(f'{repeats=}')
    print(f'{z_indices=}')
    lcm = math.lcm(*map(lambda zs: zs[0], z_indices))
    return lcm


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    text = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''
    def test(self):
        self.assertEqual(6, main(self.text))
