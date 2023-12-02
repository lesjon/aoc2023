import unittest
import math


def sum_possible_ids(text: str) -> int:
    games = text.splitlines()
    result = 0
    for game in games:
        color_counts = {"red": 0, 'green': 0, 'blue': 0}
        match game.split():
            case ('Game', id, *counts):
                id = id[:-1]
                for i in range(0, len(counts),2):
                    color = counts[i+1]
                    color = color.rstrip(',;')
                    color_counts[color] = max(color_counts[color], int(counts[i]))
            case other:
                print('COULD NOT PARSE:', other)
        power = math.prod(color_counts.values())
        result += power
    return result


def main():
    with open('input.txt', 'r') as f:
        text = f.read()
    print(sum_possible_ids(text))

if __name__ == "__main__":
    main()


class Tests(unittest.TestCase):
    text = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''
    def test(self):
        self.assertEqual(2286, sum_possible_ids(self.text))

