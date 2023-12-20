import unittest


X_KEY = None

def parse_steps(steps: str) -> int:
    return int(float.fromhex(steps))

def parse(text: str) -> tuple[dict[int, list[range]],list[int], dict[tuple[int,int], int], list[int]]:
    min_y = max_y = 0
    trenches = dict()
    trenches[X_KEY] = []
    corners = dict()
    current = [0,0]
    columns = {current[0]}
    rows = {current[1]}
    for line in text.splitlines():
        dir, steps, color = line.split()
        match (color[2:7], color[7]):
            case (steps, '0'):
                steps = parse_steps(steps)
                trenches[None].append(range(current[0], current[0]+steps))
                current[0] += steps
                columns.add(current[0])
            case (steps, '1'):
                corners[tuple(current)] = 1
                steps = parse_steps(steps)
                if current[0] in trenches:
                    trenches[current[0]].append(range(current[1], current[1]+steps))
                else:
                    trenches[current[0]] = [range(current[1], current[1]+steps)]
                current[1] += steps
                rows.add(current[1])
                corners[tuple(current)] = 1
                max_y = max(max_y, current[1])
            case (steps, '3'):
                corners[tuple(current)] = -1
                steps = parse_steps(steps)
                if current[0] in trenches:
                    trenches[current[0]].append(range(current[1]-steps, current[1]))
                else:
                    trenches[current[0]] = [range(current[1]-steps, current[1])]
                current[1] -= steps
                rows.add(current[1])
                corners[tuple(current)] = -1
                min_y = min(min_y, current[1])
            case (steps, '2'):
                steps = parse_steps(steps)
                trenches[None].append(range(current[0]-steps, current[0]))
                current[0] -= steps
                columns.add(current[0])
            case other:
                raise Exception(f'Unknown directions {other}')
    columns = sorted(columns)
    rows = sorted(rows)
    return trenches, rows, corners, columns


def sign(num: int) -> int:
    if num < 0:
        return -1
    elif num >= 0:
        return 1
    return 0

def main(text: str) -> int:
    trenches, rows, corners, columns = parse(text)
    
    print(f'{len(trenches)=}')
    print(f'{trenches=}')
    print(f'{corners=}')
    print(f'{columns=}')
    print(f'{rows=}')
    inners = 0 
    inner_poss = []
    for i_y, y in enumerate(rows[:-1]):
        next_y = rows[i_y+1]
        crossings = 0
        half_crossings = 0
        for i_x, x in enumerate(columns[:1]):
            print(f'{(x,y)=}')
            next_x = columns[i_x+1]
            columns_trenches = trenches[x]
            if (x,y) in corners:
                half_crossings += corners[(x,y)]
                print(f'{half_crossings=} {crossings=}')
                if abs(half_crossings) // 2 == 1:
                    print(f'{abs(half_crossings) // 2 == 1}')
                    half_crossings = 0
                    crossings += 1
            elif any(y in trench for trench in columns_trenches):
                print(f'any {y} in trench')
                crossings += 1
            if crossings % 2 == 1:
                print(f'({next_x=} - {x=}) * ({next_y=} - {y=})')
                inners += (next_x - x) * (next_y - y )
                for _y in range(y, next_y):
                    for _x in range(x, next_x):
                        inner_poss.append((_x,_y))

                print(f'increased {inners=}')
        print(f'end {crossings=}')
    print(f'{inner_poss=}')
    for y in range(rows[0]-1, rows[-1]+1):
        for x in range(columns[0]-1, columns[-1]+1):
            if (x,y) == (0,0):
                print('0', end='')
            elif (x,y) in inner_poss:
                print('I', end='')
            else:
                print('.', end='')
        print()


    print(f'{trenches=}')
    trench_lens = 0
    for l in trenches.values():
        trench_lens += sum(map(len, l))
    print(f'{trench_lens =}')

    return inners


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
# 0 means R, 1 means D, 2 means L, and 3 means U.
    def test(self):
        text = '''R 6 (#000060)
R 6 (#000043)
R 6 (#000022)
R 6 (#000021)
R 6 (#000022)
R 6 (#000023)
R 6 (#000022)
R 6 (#000041)
'''
        self.assertEqual(25, main(text))

#     def test(self):
#         text = '''R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)
# '''
#         self.assertEqual(952408144115, main(text))

