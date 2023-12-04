import unittest

    
def d4p1(text: str) -> int:
    total = 0
    lines = text.splitlines()
    counts = [1 for _ in lines]
    for i, line in enumerate(lines):
        print(line)
        card, game = line.split('|')
        print(f'{card=}, {game=}')
        winning = {int(s) for s in game.split()}
        id, card = card.split(':')
        print(f'{winning=}, {card=}')
        numbers = [int(c) for c in card.split()]
        print(numbers)
        correct = 0
        for n in numbers:
            if n in winning:
                correct += 1
        print(f'{correct=}')
        for j in range(i+1, i+correct+1):
            print(f'{j=}')
            counts[j] += counts[i]
    return sum(counts)


    
    




def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d4p1(text))

if __name__ == "__main__":
    main()


class Tests(unittest.TestCase):
    text = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''
    def test(self):
        self.assertEqual(30, d4p1(self.text))

