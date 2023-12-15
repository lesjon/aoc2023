import unittest

class State:
    def __init__(self, width: int, height: int):
        self.rocks = []
        self.boulders = []
        self.rolled_boulders = []
        self.width = width
        self.height = height

    def roll_north(self):
        while self.boulders:
            x,y = self.boulders.pop()
            while y > 0:
                y -= 1
                if (x,y) in self.rocks or (x,y) in self.rolled_boulders or y == 0:
                    self.rolled_boulders.append((x,y+1))
                    break

    def __repr__(self) -> str:
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.boulders:
                    s += 'o'
                elif (x, y) in self.rolled_boulders:
                    s += '0'
                elif (x, y) in self.rocks:
                    s += '#'
                else:
                    s += '.'
            s += '\n'
        return s
    
    def load_on_north(self) -> int:
        assert not self.boulders
        total = 0
        for _, y in self.rolled_boulders:
            total += self.height - y
        return total





def parse(text: str) -> State:
    lines = text.splitlines()
    state = State(len(lines[0]), len(lines))
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case '#':
                    state.rocks.append((x,y))
                case '.':
                    pass
                case 'O':
                    state.boulders.append((x,y))
                case other:
                    raise Exception(f'Unexpected char: {other}')
    return state

def run(text: str) -> int:
    state = parse(text)
    print(f'{state}')
    state.roll_north()
    print(f'{state}')
    return state.load_on_north()
    

if __name__ == "__main__":
    with open('input.txt') as f:
        print(run(f.read()))

class Tests(unittest.TestCase):
    def test(self):
        text = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....\
'''
        self.assertEqual(136, run(text))


