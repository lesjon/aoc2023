import unittest


def parse(text: str) -> list[tuple[range, range]]:
    result = []
    for line in text.splitlines():
        match line.split():
            case ('D', steps, color):
                result.append((range(0),range(int(steps))))
            case ('R', steps, color):
                result.append((range(int(steps)),range(0)))
            case ('U', steps, color):
                result.append((range(0),range(-int(steps),0)))
            case ('L', steps, color):
                result.append((range(-int(steps), 0),range(0)))
    return result
    




def sign(num: int) -> int:
    if num < 0:
        return -1
    elif num >= 0:
        return 1
    return 0

def main(text: str) -> int:
    instrs = parse(text)
    min_x = max_x = min_y = max_y = 0
    current = (0,0)
    path: dict[tuple[int,int], tuple[int, int]] = {}
    path.update({current: (0,0)})
    for (x_range,y_range) in instrs:
        print(f'{x_range} {y_range}')
        for y in y_range:
            path.update({current:(0, sign(y))})
            current = (current[0], current[1] + sign(y))
            path.update({current:(0, sign(y))})
            min_y = min(min_y, current[1])
            max_y = max(max_y, current[1])
        for x in x_range:
            current = (current[0] + sign(x), current[1])
            path.update({current:(sign(x), 0)})
            min_x = min(min_x, current[0])
            max_x = max(max_x, current[0])
    print(f'{min_x=}-{max_x=} {min_y=}-{max_y=}')
    print(path)
    inners = set()
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in path:
                match path.get((x,y)):
                    case (0,1):
                        print('v', end='')
                    case (0,-1):
                        print('^', end='')
                    case (1,0):
                        print('>', end='')
                    case (-1,0):
                        print('<', end='')
            else:
                lefts_coords = ((check_x, y) for check_x in range(min_x, x))
                crossings = 0
                in_trench = 0
                for coord in lefts_coords:
                    if coord in path:
                        (_,y_dir) = path.get(coord)
                        in_trench += y_dir
                    else:
                        if in_trench != 0:
                            crossings += 1
                        in_trench = 0
                if in_trench != 0:
                    crossings += 1

                if crossings % 2 == 1:
                    inners.add((x,y))
                    print('I', end='')
                else:
                    print('.', end='')
        print()

    return len(path) + len(inners)


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    def test(self):
        text = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''
        self.assertEqual(62, main(text))
    
    
