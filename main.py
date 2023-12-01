import unittest


def replace_written(number: str) -> str:
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    written = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',  'nine']
    try:
        index: int = written.index(number)
        return digits[index]
    except ValueError:
        return number
    

def art_sum(text: str) -> int:
    digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',  'nine'}
    total = 0
    for line in text.splitlines():
        if len(line) <= 1:
            continue
        number = []
        for i in range(len(line)):
            for digit in digits:
                if line[i:].startswith(digit):
                    number.append(digit)
                    break
            else:
                continue
            break

        for i in range(len(line)-1, -1, -1):
            for digit in digits:
                if line[i:].startswith(digit):
                    number.append(digit)
                    break
            else:
                continue
            break
        print(f'{number}')
        number = list(map(replace_written, number))

        total += int(''.join(number))
    return total

def main():
    with open('input.txt', 'r') as f:
        text = f.read()
    print(art_sum(text))

if __name__ == "__main__":
    main()


class Tests(unittest.TestCase):
    text = ''' two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen '''
    def test(self):
        self.assertEqual(281, art_sum(self.text))

