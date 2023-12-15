import copy
text = '?' * 18 
ints = [1,2,8]
result = set()
questions = set()
result.add(text)
def get_possibilities(line: str) -> set[str]:
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
                dot = line[:i] + '.'
                dot[i] = '.'
                next_set.add(''.join(dot))
                line[i] = '#'
                next_set.add(''.join(line))
        result = next_set
    return result

print(get_possibilities(text))
