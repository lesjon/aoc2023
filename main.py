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
        case _:
            return []

def find_starts(s: tuple[int, int], field: list[str]) -> tuple[list[tuple[int,int]], str]:
    result = []
    x, y = s
    replacements = {'-','|','F','L','7','J'}
    if x-1 >=0:
        match field[y][x-1]:
            case 'F' | '-' | 'L':
                replacements.remove('F')
                replacements.remove('|')
                replacements.remove('L')
                result.append((x-1, y))
    if x+1 < len(field[y]):
        match field[y][x+1]:
            case 'J' | '-' | '7':
                replacements.remove('J')
                replacements.remove('|')
                replacements.remove('7')
                result.append((x+1, y))
    if y-1 >=0:
        match field[y-1][x]:
            case 'F' | '|' | '7':
                replacements.remove('J')
                replacements.remove('|')
                replacements.remove('7')
                result.append((x, y-1))
    if y+1 < len(field):
        match field[y+1][x]:
            case 'J' | '|' | 'L':
                result.append((x, y+1))
    assert len(result) == 2
    return '', result


def main(text: str) -> int:
    field = text.splitlines()
    l = r = None
    l_prev = r_prev = None
    path = set()
    for y,row in enumerate(field):
        for x, c in enumerate(row):
            if c == 'S':
                path.add((x,y))
                l_prev = r_prev = (x,y)
                l, r = find_starts((x,y), field)
                path.add(l)
                path.add(r)
    assert l
    assert r
    steps = 1
    l_path = []
    r_path = []
    while True:
        ls = connecteds(*l, field)
        rs = connecteds(*r, field)
        ls.remove(l_prev)
        l_prev = l
        l = ls[0]
        l_path.append(l)
        rs.remove(r_prev)
        r_prev  = r
        r = rs[0]
        r_path.append(r)

        steps += 1
        if l == r:
            break
    path = path.union(l_path)
    path = path.union(r_path)
    print(f'{path=}')
    enclosed_fields = set()
    for y,row in enumerate(field):
        for x, c in enumerate(row):
            if (x,y) in path:
                continue
            if enclosed(x, y, path, field):
                enclosed_fields.add((x,y))
    print(f'{enclosed_fields =}')
    
    for y,row in enumerate(field):
        for x, c in enumerate(row):
            if (x,y) in path:
                print('p', end='')
            elif enclosed(x, y, path, field):
                print('I', end='')
            else:
                print('.', end='')
        print()
    return len(enclosed_fields)


def enclosed(x: int, y:int, path: set[tuple[int,int]], field: list[str]) -> bool:
    l=r=t=b = 0
    in_from = 0
    for l_x in range(x):
        if (l_x, y) in path:
            c = field[y][l_x]
            match c:
                case '|':
                    l += 1
                case '-':
                    pass
                case 'F' | '7':
                    match in_from:
                        case 0:
                            in_from = -1
                        case -1:
                            in_from = 0
                        case 1:
                            l += 1
                            in_from = 0
                case 'J' | 'L':
                    match in_from:
                        case 0:
                            in_from = 1
                        case 1:
                            in_from = 0
                        case -1:
                            l += 1
                            in_from = 0
                case other:
                    raise Exception(f'Unknown path: {other} at {(l_x, y)=}')
    assert in_from == 0
    for r_x in range(x, len(field[y])):
        if ((r_x, y) in path):
            c = field[y][r_x]
            match c:
                case '|':
                    r += 1
                case '-':
                    pass
                case 'F' | '7':
                    match in_from:
                        case 0:
                            in_from = -1
                        case -1:
                            in_from = 0
                        case 1:
                            r += 1
                            in_from = 0
                case 'J' | 'L':
                    match in_from:
                        case 0:
                            in_from = 1
                        case 1:
                            in_from = 0
                        case -1:
                            r += 1
                            in_from = 0
                case other:
                    raise Exception(f'Unknown path: {other} at {(r_x, y)=}')
    assert in_from == 0
    for t_y in range(y):
        if ((x, t_y) in path):
            c = field[t_y][x]
            match c:
                case '-':
                    t += 1
                case '|':
                    pass
                case 'J' | '7':
                    match in_from:
                        case 0:
                            in_from = -1
                        case -1:
                            in_from = 0
                        case 1:
                            t += 1
                            in_from = 0
                case 'F' | 'L':
                    match in_from:
                        case 0:
                            in_from = 1
                        case 1:
                            in_from = 0
                        case -1:
                            t += 1
                            in_from = 0
                case other:
                    raise Exception(f'Unknown path: {other} at {(x, t_y)}')
    assert in_from == 0
    for b_y in range(y, len(field)):
        if (x, b_y) in path:
            c = field[b_y][x]
            match c:
                case '-':
                    b += 1
                case '|':
                    pass
                case 'J' | '7':
                    match in_from:
                        case 0:
                            in_from = -1
                        case -1:
                            in_from = 0
                        case 1:
                            b += 1
                            in_from = 0
                case 'F' | 'L':
                    match in_from:
                        case 0:
                            in_from = 1
                        case 1:
                            in_from = 0
                        case -1:
                            b += 1
                            in_from = 0
                case other:
                    raise Exception(f'Unknown path: {other} at {(x, b_y)=}')
    assert in_from == 0
    return l % 2 == 1 and r % 2 == 1 and t % 2 == 1 and b % 2 == 1

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
