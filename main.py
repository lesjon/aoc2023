import unittest


def connecteds(x: int, y: int, field: list[str]) -> list[tuple[int, int]]:
    match field[y][x]:
        case 'F':
            return [(x,y+1), (x+1,y)]
        case '7':
            return [(x,y+1), (x-1,y)]
        case '-':
            return [(x-1,y), (x+1,y)]
        case '|':
            return [(x,y-1), (x,y+1)]
        case 'J':
            return [(x-1,y), (x,y-1)]
        case 'L':
            return [(x,y-1), (x+1,y)]
        case '.':
            raise Exception('Illegal state')
        case other:
            raise Exception(f'Unexpected {other}')

def find_starts(s: tuple[int, int], field: list[str]) -> list[tuple[int,int]]:
    result = []
    x, y = s
    if x-1 >=0:
        match field[y][x-1]:
            case 'F' | '-' | 'L':
                result.append((x-1, y))
    if x+1 < len(field[y]):
        match field[y][x+1]:
            case 'J' | '-' | '7':
                result.append((x+1, y))
    if y-1 >=0:
        match field[y-1][x]:
            case 'F' | '|' | '7':
                result.append((x, y-1))
    if y+1 < len(field):
        match field[y+1][x]:
            case 'J' | '|' | 'L':
                result.append((x, y+1))
    assert len(result) == 2
    return result


def main(text: str) -> int:
    field = text.splitlines()
    l = r = None
    l_prev = r_prev = None
    for y,row in enumerate(field):
        for x, c in enumerate(row):
            if c == 'S':
                l_prev = r_prev = (x,y)
                l , r = find_starts((x,y), field)
    assert l
    assert r
    steps = 1
    while True:
        ls = connecteds(*l, field)
        rs = connecteds(*r, field)
        ls.remove(l_prev)
        l_prev = l
        l = ls[0]
        rs.remove(r_prev)
        r_prev  = r
        r = rs[0]

        steps += 1
        if l == r:
            return steps


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    def test(self):
        text = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''
        self.assertEqual(4, main(text))

    def test2(self):
        text = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''
        self.assertEqual(8, main(text))
