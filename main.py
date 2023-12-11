import unittest

def parse(text: str) -> tuple[dict[int, tuple[int, int]], set[int], set[int]]:
    empty_rows = set()
    galaxies = dict()
    lines = text.splitlines()
    empty_columns = {x for x in range(len(lines[0]))}
    for y, line in enumerate(lines):
        row_empty = True
        for x, c in enumerate(line):
            if c == '#':
                galaxies.update({len(galaxies): (x,y)})
                row_empty = False
                empty_columns.discard(x)
        if row_empty:
            empty_rows.add(y)

    for col in range(len(lines[0])):
        if col in empty_columns:
            print('v', end='')
        else:
            print(' ', end='')
    print()
    for y, line in enumerate(lines):
        if y in empty_rows:
            print('-' * len(line))
        else:
            print(line)
    return galaxies, empty_rows, empty_columns

def main(text: str) -> int:
    galaxies, empty_rows, empty_columns = parse(text)
    total = 0
    for i, pos in galaxies.items():
        for j in range(i+1, len(galaxies)):
            other_pos = galaxies[j]
            dist = abs(pos[0]-other_pos[0]) + abs(pos[1]-other_pos[1])
            for col in empty_columns:
                if col in range(*sorted([pos[0],other_pos[0]])):
                    dist += 1000000-1
            for row in empty_rows:
                if row in range(*sorted([pos[1],other_pos[1]])):
                    dist += 1000000-1
            # print(f'Between galaxy {i} and galaxy {j}: {dist}')
            total += dist 
    return total



if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
     def test(self):
        text = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''
        self.assertEqual(374, main(text))
