import unittest

def reflection_from(n: int, line: str) -> bool:
    print(f'reflection_from({n}, {line})')
    assert n > 0
    for i in range(n):
        left = n-i-1
        right = n+i
        if left < 0 or right >= len(line):
            break
        if line[left] != line[right]:
            return False
    return True

def run(text: str) -> int:
    total = 0
    for block in text.split('\n\n'):
        lines = block.splitlines()
        print(f'{lines=}')
        hori_reflections = {i for i in range(1, block.index('\n'))}
        for line in lines:
            to_remove = []
            for i in hori_reflections:
                if not reflection_from(i, line):
                    to_remove.append(i)
            hori_reflections = hori_reflections.difference(to_remove)
        print(f'{hori_reflections=}')
        if len(hori_reflections) == 1:
            total += next(iter(hori_reflections))
            continue
        lines = list(map(lambda t: ''.join(t), zip(*lines)))
        vert_reflections = {i for i in range(1, len(lines[0]))}
        print(f'flipped {lines=}')
        for line in lines:
            to_remove = []
            for i in vert_reflections:
                if not reflection_from(i, line):
                    to_remove.append(i)
            vert_reflections = vert_reflections.difference(to_remove)
        print(f'{vert_reflections=}')
        assert len(vert_reflections) == 1
        total += 100 * next(iter(vert_reflections))
    return total

if __name__ == "__main__":
    with open('input.txt') as f:
        print(run(f.read()))

class Tests(unittest.TestCase):
    def test(self):
        text = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
        self.assertEqual(405, run(text))
