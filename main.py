import unittest

def get_connections(x: int, y: int, field: list[str]) -> list[tuple[int,int]]:
    connections = []
    match field[y][x]:
        case 'S':
            print(f'get_connections with S at({x}, {y})')
            if x - 1 >= 0:
                c = field[y][x-1]
                if c in '-FL':
                    connections.append((x-1,y))
            if x + 1 >= 0:
                c = field[y][x+1]
                if c in '-7J':
                    connections.append((x+1,y))
            if y - 1 >= 0:
                c = field[y-1][x]
                if c in '|F7':
                    connections.append((x,y-1))
            if y + 1 >= 0:
                c = field[y+1][x]
                if c in '|LJ':
                    connections.append((x,y+1))
        case '-':
            connections.extend([(x-1,y), (x+1,y)])
        case '|':
            connections.extend([(x,y-1), (x,y+1)])
        case 'F':
            connections.extend([(x+1,y), (x,y+1)])
        case 'L':
            connections.extend([(x+1,y), (x,y-1)])
        case '7':
            connections.extend([(x-1,y), (x,y+1)])
        case 'J':
            connections.extend([(x-1,y), (x,y-1)])
    return connections


def is_enclosed(x: int, y: int, field: list[str], path: set[tuple[int, int]]) -> bool:
    result = 0
    fs = 0
    ls = 0
    ss = 0
    js = 0
    for l_x in range(x):
        if not (l_x, y) in path:
            continue
        c = field[y][l_x]
        match c:
            case 'S':
                raise Exception('Did not replace S!')
            case '-':
                pass
            case '|':
                result += 1
            case 'F':
                fs += 1
            case 'L':
                ls += 1
            case '7':
                ss += 1
            case 'J':
                js += 1
    result += ls - js
    return result % 2 == 1

def replace_start(field: list[str], x: int,y: int):
    row = field[y]
    assert row[x] == 'S'
    nexts = get_connections(x, y, field)
    print(f'{nexts=}')
    directions = {(n[0]-x, n[1]-y) for n in nexts}
    print(f'{directions=}')
    pipe = None
    if (0,1) in directions:
        if (0,-1) in directions:
            pipe = '|'
        elif (1,0) in directions:
            pipe = 'F'
        elif (-1,0) in directions:
            pipe = '7'
    elif (0,-1) in directions:
        if (-1,0) in directions:
            pipe = 'J'
        elif (1,0) in directions:
            pipe = 'L'
    elif (1,0) in directions:
        assert (-1,0) in directions
        pipe = '-'
    assert pipe
    field[y] = row[:x] + pipe + row[x+1:]

def main(text: str) -> int:
    path = set()
    field = text.splitlines()
    start = None
    for y, row in enumerate(field):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x,y)
                path.add(start)
    assert not start is None
    
    replace_start(field, start[0],start[1])

    positions = {start}
    while positions:
        current = positions.pop()
        path.add(current)
        nexts = get_connections(current[0], current[1], field)
        positions.update(nexts)
        positions -= path

    enclosed = set()
    for y, row in enumerate(field):
        for x, c in enumerate(row):
            if (x,y) in path:
                continue
            if is_enclosed(x, y, field, path):
                enclosed.add((x,y))
    for y, row in enumerate(field):
        for x, c in enumerate(row):
            if (x,y) in path:
                print(c, end='')
            elif (x,y) in enclosed:
                print('I', end='')
            else:
                print('.', end='')
        print()
    return len(enclosed)



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
