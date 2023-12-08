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
    print(f'{nodes=}')
    nodes = {n[0]: n[1] for n in nodes}
    current = ('AAA', nodes['AAA'])
    i = 0
    count = 0
    while current[0] != 'ZZZ':
        count += 1
        lr = route[i]
        i = (i+1) % len(route)
        next = current[1][lr]
        current = (next, nodes[next])
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
