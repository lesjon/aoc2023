import unittest
import math
import itertools

TOKENS =  '*+#%$!@^&-=/'

def id_coords(text:str) -> set[tuple[int,int,int,int]]:
    ids = set()
    for y,l in enumerate(text.splitlines()):
        skip = 0
        for x, c in enumerate(l):
            if skip > 0:
                skip -= 1
                continue
            if c in '0123456789':
                num = itertools.takewhile(lambda c: c in '0123456789', l[x:] )
                num = ''.join(num)
                id = int(num)
                ids.add((x,y, id, len(num)))
                skip = len(num)
    return ids

def token_coords(text:str) -> set[tuple[int,int]]:
    coords = set()
    for y,l in enumerate(text.splitlines()):
        for x, c in enumerate(l):
            if c in TOKENS:
                coords.add((x,y))
            elif c in '0123456789':
                pass
            elif c in '.':
                pass
            else:
                print(c, 'not recognised as token')
    return coords

def adjacent_to_coord(loc: tuple[int, int], coords: set[tuple[int,int]]) -> int:
    for coord in coords:
        x,y = loc[0] -coord[0], loc[1] -coord[1] 
        if abs(x) <= 1 and abs(y) <= 1:
            return True
    return False

def d3p1(text: str) -> int:
    result = 0
    coords = token_coords(text)
    ids = id_coords(text)
    for id in ids:
        adjacent = False
        for x in range(id[0], id[0]+id[3]):
            if adjacent_to_coord((x,id[1]), coords):
                adjacent = True
                break
        if adjacent:
            print(id, 'is adjacent')
            result += id[2]
        else:
            print(id, 'is not adjacent')

    return result




def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d3p1(text))

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
        self.assertEqual(4361, d3p1(self.text))

