import unittest


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
    while not all(map(lambda n: n[0].endswith('Z'), currents)):
        if count % 1000 == 0:
            print(f'{count}')
        for i in range(len(currents)):
            current = currents[i]
            lr = route[count % len(route)]
            count += 1
            next = current[1][lr]
            currents[i] = (next, nodes[next])
    return count


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
