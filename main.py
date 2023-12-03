import unittest
import math
from itertools import takewhile

def find_adjacent_nums(text: str, loc: tuple[int,int]) -> list[int]:
    result = []
    lines = text.splitlines()
    for y in range(loc[1]-1,loc[1]+2):
        skip = 0
        for x in range(loc[0]-1,loc[0]+2):
            print(f'{x=}{y=}{skip=}')
            if skip > 1:
                skip -= 1
                continue
            if x == 0 and y == 0:
                continue
            if lines[y][x] in '0123456789':
                digits = takewhile(lambda c: c in '0123456789', reversed(lines[y][:x]))
                start = ''.join(reversed(list(digits)))
                end = ''.join(takewhile(lambda c: c in '0123456789', lines[y][x:]))
                skip = len(end)
                print('start, end:', start, end)
                result.append(int(start+end))
    return result
    
def d3p2(text: str) -> int:
    result = 0
    for y, l in enumerate(text.splitlines()):
        for x,c in enumerate(l):
            if c == '*':
                print('gear at', (x,y))
                nums = find_adjacent_nums(text, (x,y))
                if len(nums) == 2:
                    ratio = math.prod(nums)
                    result += ratio
    return result




def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d3p2(text))

if __name__ == "__main__":
    main()


class Tests(unittest.TestCase):
    text = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
    def test(self):
        self.assertEqual(467835, d3p2(self.text))

