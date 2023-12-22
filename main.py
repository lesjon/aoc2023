import unittest

def parse(text: str) -> tuple[list[str], tuple[int,int]]:
    lines = text.splitlines()
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x,y)
    assert start 
    return lines, start

def next_positions(pos: tuple[int,int], maze: list[str]) -> set[tuple[int,int]]:
    directions = [(0,1),(-1,0), (0,-1),(1,0)]
    x,y = pos
    ps = [(x+dx, y+dy) for (dx, dy) in directions]
    ps = filter(lambda p: p[0] >= 0 and p[1] >= 0, ps)
    ps = filter(lambda p: p[0] < len(maze[0]), ps)
    ps = filter(lambda p: p[1] < len(maze), ps)
    ps = filter(lambda p: maze[p[1]][p[0]] != '#', ps)
    return set(ps)


def main(text: str, steps: int) -> int:
    positions: dict[int, set[tuple[int,int]]] = dict()
    seen: set[tuple[int,int]] = set()
    maze, start = parse(text)
    positions[0] = {start}
    seen.add(start)
    for i in range(steps + 1):
        print(f'{i/steps=}')
        current_positions = positions[i]
        positions[i+1] = set()
        for pos in current_positions:
            nexts = next_positions(pos, maze)
            nexts -= seen
            positions[i+1].update(nexts)
            seen.update(nexts)
    reachable = 0
    if steps % 2 == 0:
        for step, poss in positions.items():
            if step % 2 == 0:
                reachable += len(poss)
    if steps % 2 == 1:
        for step, poss in positions.items():
            if step % 2 == 1:
                reachable += len(poss)
    return reachable


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text, 26501365))

class Tests(unittest.TestCase):
    def test(self):
        text = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''
        self.assertIs(16, main(text, 6))
