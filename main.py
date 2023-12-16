import unittest

def parse(text: str) -> list[str]:
    return text.splitlines()

def run(text: str) -> int:
    cave = parse(text)
    width = len(cave[0])
    height = len(cave)
    lasers = {(0,0,1,0)}
    seen_positions = set()
    seen_lasers = set()
    while lasers:
        to_remove = []
        lasers_to_parse = list(lasers) 
        lasers.clear()
        for x,y,vx,vy in lasers_to_parse:
            seen_positions.add((x,y))
            seen_lasers.add((x,y,vx,vy))
            match cave[y][x]:
                case '.':
                    y += vy
                    x += vx
                    lasers.add((x,y,vx,vy))
                case '-':
                    if vy != 0:
                        lasers.add((x+1,y, 1,0))
                        lasers.add((x-1,y,-1,0))
                    else:
                        lasers.add((x+vx,y,vx,vy))
                case '|':
                    if vx != 0:
                        lasers.add((x,y+1,0, 1))
                        lasers.add((x,y-1,0,-1))
                    else:
                        lasers.add((x,y+vy,vx,vy))
                case '\\':
                    if vx == 1:
                        lasers.add((x,y+1,0, 1))
                    elif vx == -1:
                        lasers.add((x,y-1,0,-1))
                    elif vy == 1:
                        lasers.add((x+1,y,1,0))
                    elif vy == -1:
                        lasers.add((x-1,y,-1, 0))
                case '/':
                    if vx == 1:
                        lasers.add((x,y-1,0,-1))
                    elif vx == -1:
                        lasers.add((x,y+1,0, 1))
                    elif vy == 1:
                        lasers.add((x-1,y,-1, 0))
                    elif vy == -1:
                        lasers.add((x+1,y,1,0))
        # for y in range(height):
        #     for x in range(width):
        #         if (x,y) in seen_positions:
        #             print('#', end='')
        #         else:
        #             print(cave[y][x], end='')
        #     print()
        # print()

        lasers = {l for l in lasers if 0 <= l[0] < width and 0 <= l[1] < height}
        lasers -= seen_lasers
    for y in range(height):
        for x in range(width):
            if (x,y) in seen_positions:
                print('#', end='')
            else:
                print(cave[y][x], end='')
        print()

    return len(seen_positions)


if __name__ == "__main__":
    with open('input.txt') as f:
        print(run(f.read()))

class Tests(unittest.TestCase):
    def test(self):
        text = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''
        self.assertEqual(46, run(text))
