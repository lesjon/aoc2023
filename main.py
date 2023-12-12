import unittest

def parse(text: str) -> list[tuple[str, list[int]]]:
    result = map(str.split, text.splitlines())
    result = ((s, i.split(',')) for s, i in result)
    result = [(s, list(map(int, i))) for s, i in result]
    return result

def partial_valid(solution: str, ints: list[int]) -> bool:
    count = 0
    result = []
    for c in solution:
        match c:
            case '#':
                count += 1
            case '.':
                if count > 0: 
                    result.append(count)
                count = 0
            case '?':
                break
    if count > 0: 
        result.append(count)
    for i,c in enumerate(result):
        if i >= len(ints):
            return False
        elif i == len(result) and c > ints[i]:
            return False
        elif c != ints[i]:
            return False
    needed_space = 0
    for i in ints[len(result):]:
        needed_space += 1+i
    first_unknown = solution.find('?')
    if first_unknown == -1 and needed_space > 0:
        return False
    elif len(solution) - first_unknown < needed_space:
        return False
    return True

def valid(solution: str, ints: list[int]) -> bool:
    count = 0
    result = []
    for c in solution:
        match c:
            case '#':
                count += 1
            case '.':
                if count > 0: 
                    result.append(count)
                count = 0
    if count > 0: 
        result.append(count)
    return result == ints

def get_possibilities(line: str, ints: list[int]) -> set[str]:
    result = set()
    result.add(line)
    while any(map(lambda l: '?' in l, result)):
        next_set = set()
        for line in result:
            if not  '?' in line:
                continue
            for i, c in enumerate(line):
                if c != '?':
                    continue
                dot = line[:i] + '.' + line[i+1:]
                if partial_valid(dot, ints):
                    next_set.add(dot)
                broken = line[:i] + '#' + line[i+1:]
                if partial_valid(broken , ints):
                    next_set.add(broken)
        result = next_set
    return result


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

