import unittest
import itertools

def parse(text: str) -> list[tuple[str, list[int]]]:
    result = map(str.split, text.splitlines())
    result = ((s, i.split(',')) for s, i in result)
    result = [(s, list(map(int, i))) for s, i in result]
    return result

def get_space_needed(ints: list[int]) -> int:
    result = -1
    for i in ints:
        result += 1 + i
    return result


def get_possibilities(length: int, ints: list[int]) -> set[str]:
    brokens = ['#' * i for i in ints]

    working = ['.' for _ in range(length-sum(ints))]
    minimal = [[b,w] for b,w in zip(brokens[:-1],working)].flatten()
    minimal.append(brokens[-1])
    result = []
    for w in working[len(brokens)-1:]:


    return set(possibilities)


def main(text: str) -> int:
    line_nums = parse(text)
    total = 0
    for i, (line, nums) in enumerate(line_nums):
        print(f'{i}/{len(line_nums)}')
        possibilities = get_possibilities(line, nums)
        total += len(list(filter(lambda p: valid(p, nums), possibilities)))

    return total


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    def test_short(self):
        text = '???.### 1,1,3'
        self.assertEqual(1, main(text))
        text = '.??..??...?##. 1,1,3'
        self.assertEqual(4, main(text))  
        text = '?###???????? 3,2,1'
        self.assertEqual(10, main(text))  


    def test(self):
        text = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
        self.assertEqual(21, main(text))
    
    def test_possibilities(self):
        lines = '?#?.'
        expected = { '.#..', }
        self.assertEqual(expected, get_possibilities(lines, [1]))
        expected = {  '.##.', '##..'}
        self.assertEqual(expected, get_possibilities(lines, [2]))
        expected = {  '###.'}
        self.assertEqual(expected, get_possibilities(lines, [3]))

    def test_row_2(self):
        text = '???????##?????' 
        ints = [1,2,8]
        expecteds = {
'#.##..########',
'#..##.########',
'.#.##.########',
'#.##.########.',
        }
        self.assertEqual(expecteds, get_possibilities(text, ints))

