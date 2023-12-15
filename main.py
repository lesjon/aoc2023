import unittest

def reflection_from(n: int, line: str) -> int:
    print(f'reflection_from({n}, {line})')
    assert n > 0
    smudges = 0
    for i in range(n):
        left = n-i-1
        right = n+i
        if left < 0 or right >= len(line):
            break
        if line[left] != line[right]:
            smudges += 1
    return smudges 

def run(text: str) -> int:
    total = 0
    for block in text.split('\n\n'):
        lines = block.splitlines()
        print(f'{lines=}')
        hori_reflections = {i: 0 for i in range(1, block.index('\n'))}
        for line in lines:
            for i in hori_reflections:
                hori_reflections[i] += reflection_from(i, line)
        hori_reflections = dict(filter(lambda e: e[1] == 1, hori_reflections.items()))
        print(f'{hori_reflections=}')
        if len(hori_reflections) == 1:
            total += next(iter(hori_reflections))
            continue
        lines = list(map(lambda t: ''.join(t), zip(*lines)))
        vert_reflections = {i: 0 for i in range(1, len(lines[0]))}
        print(f'flipped:')
        for line in lines:
            print(line)
        for line in lines:
            for i in vert_reflections:
                vert_reflections[i] += reflection_from(i, line)
        vert_reflections = dict(filter(lambda e: e[1] == 1, vert_reflections .items()))
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
        self.assertEqual(400, run(text))


