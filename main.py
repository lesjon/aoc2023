import unittest


PART2 = False

def parse(text: str) -> list[tuple[range, range]]:
    result = []
    for line in text.splitlines():
        dir, steps, color = line.split()
        if PART2:
            match (color[2:7], color[7]):
                case (steps, '1'):
                    steps = int(float.fromhex(steps))
                    result.append((range(0),range(steps)))
                case (steps, '0'):
                    steps = int(float.fromhex(steps))
                    result.append((range(steps),range(0)))
                case (steps, '3'):
                    steps = int(float.fromhex(steps))
                    result.append((range(0),range(-steps,0)))
                case (steps, '2'):
                    steps = int(float.fromhex(steps))
                    result.append((range(-steps, 0),range(0)))
        else:
            match (steps, dir):
                case (steps, 'D'):
                    result.append((range(0),range(int(float.fromhex(steps)))))
                case (steps, 'R'):
                    result.append((range(int(float.fromhex(steps))),range(0)))
                case (steps, 'U'):
                    result.append((range(0),range(-int(float.fromhex(steps)),0)))
                case (steps, 'L'):
                    result.append((range(-int(float.fromhex(steps)), 0),range(0)))
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
        y_length = len(y_range)
        for i, y in enumerate(y_range):
            if i == 0:
                path[current] = (0, sign(y))
            current = (current[0], current[1] + sign(y))
            if i+1 == y_length:
                path[current] = (0, sign(y))
            else:
                path[current] = (0, 2*sign(y))
            min_y = min(min_y, current[1])
            max_y = max(max_y, current[1])
        for x in x_range:
            current = (current[0] + sign(x), current[1])
            if not current in path:
                path.update({current:(sign(x), 0)})
            min_x = min(min_x, current[0])
            max_x = max(max_x, current[0])
    print(f'{min_x=}-{max_x=} {min_y=}-{max_y=}')
    print(f'{len(path)=}')
    inners = set()
    for y in range(min_y, max_y+1):
        inside = False
        in_trench = 0
        for x in range(min_x, max_x+1):
            if (x,y) in path:
                _,y_dir = path.get((x,y))
                print(abs(y_dir), end='')
                # match y_dir:
                #     case 1 | 2:
                #         if not PART2:
                #             print('v', end='')
                #     case -1 | -2:
                #         if not PART2:
                #             print('^', end='')
                #     case other:
                #         if not PART2:
                #             print(other, end='')
                in_trench += y_dir
            else:
                if (in_trench // 2 ) % 2 == 1:
                    inside = not inside
                    in_trench = 0
                if inside:
                    inners.add((x,y))
                    if not PART2:
                        print('I', end='')
                else:
                    if not PART2:
                        print('.', end='')
        if not PART2:
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
        self.assertEqual(952408144115, main(text))
    
    
