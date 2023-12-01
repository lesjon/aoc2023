import unittest

def art_sum(text: str) -> int:
    total = 0
    for line in text.splitlines():
        if len(line) <= 1:
            continue
        first = ''
        last = ''
        for c in line:
            if c in '0123456789':
                first = c

        for c in reversed(line):
            if c in '0123456789':
                last = c
        total += int(last + first)
    return total

def main():
    with open('input.txt', 'r') as f:
        text = f.read()
    print(art_sum(text))

if __name__ == "__main__":
    main()


class Tests(unittest.TestCase):
    text = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''
    def test(self):
        self.assertEqual(142, art_sum(self.text))

