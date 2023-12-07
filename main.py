from dataclasses import dataclass
import unittest

@dataclass
class Hand:
    cards: str
    bid: int
    value: int

FACES = 'AKQJT98765432'
FACE_VALUES = {f:i for i, f in enumerate(reversed(FACES))}
print(f'{FACE_VALUES=}')

def value(cards: str) -> int:
    cards_value = 0
    for i, c in enumerate(reversed(cards)):
        card_value = (len(FACES)**(i+1)) * FACE_VALUES[c]
        print(f'{c} {card_value=}')
        cards_value += card_value

    print(f'highest_card_value = {cards_value}')
    i = len(cards)+2
    rank_value = calc_rank_value(cards) * (len(FACES)**(i+1))
    print(f'{rank_value=}')
    cards_value += rank_value
    return cards_value

def five_of_a_kind(cards: str) -> bool:
    return cards[0] == cards[1] == cards[2] == cards[3] == cards[4]

def four_of_a_kind(cards: str) -> bool:
    for c in set(cards):
        if cards.count(c) == 4:
            return True
    return False

def full_house(cards)-> bool:
    groups = {3,2}
    for c in set(cards):
        try:
            groups.remove(cards.count(c))
        except KeyError:
            return False
    return len(groups) == 0

def three_of_a_kind(cards: str) -> bool:
    for c in set(cards):
        if cards.count(c) == 3:
            return True
    return False

def two_pair(cards: str) -> bool:
    groups = 2
    for c in set(cards):
        if cards.count(c) == 2:
            groups -= 1
    return groups == 0

def one_pair(cards: str) -> bool:
    for c in set(cards):
        if cards.count(c) == 2:
            return True
    return False

def calc_rank_value(cards: str) -> int:

    if five_of_a_kind(cards):
        print(f'{cards} five_of_a_kind')
        return 7
    if four_of_a_kind(cards):
        print(f'{cards} four of a kind')
        return 6
    if full_house(cards):
        print(f'{cards} full house')
        return 5
    if three_of_a_kind(cards):
        print(f'{cards} three of a kind')
        return 4
    if two_pair(cards):
        print(f'{cards} two pair')
        return 3
    if one_pair(cards):
        print(f'{cards} one pair')
        return 2
    return 0


def d7p1(text: str) -> int:
    hands = []
    for line in text.splitlines():
        cards, bid = line.split()
        hand = Hand(cards, int(bid), value(cards))
        hands.append(hand)

    print(f'{hands=}')
    hands = sorted(hands, key=lambda h: h.value)
    print(f'sorted = {hands=}')
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1 ) * hand.bid
    return total

    


def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d7p1(text))

if __name__ == "__main__":
    main()

class Tests(unittest.TestCase):

    text = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
    def test(self):
        self.assertEqual(6440, d7p1(self.text))

