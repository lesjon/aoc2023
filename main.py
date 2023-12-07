import unittest

JOKER = 'J'


def five_of_a_kind(cards: str) -> bool:
    # Five of a kind, where all five cards have the same label: AAAAA
    faces = set(cards)
    try:
        faces.remove(JOKER)
    except KeyError:
        pass
    return len(faces) <= 1

def four_of_a_kind(cards: str) -> bool:
    # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    jokers = cards.count(JOKER)
    if jokers >= 4:
        return True
    for c in set(cards):
        if c == JOKER:
            continue
        if cards.count(c) + jokers >= 4:
            return True
    return False


def full_house(cards: str) -> bool:
    # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    jokers = cards.count(JOKER)
    if jokers >= 4:
        return True
    counts = []
    for c in set(cards):
        if c == JOKER:
            continue
        counts.append(cards.count(c))
    match jokers:
        case 0:
            return 3 in counts and 2 in counts
        case 1:
            if 1 in counts and 3 in counts:
                return True
            if counts.count(2) == 2:
                return True
            return False
        case 2 | 3:
            if len(counts) <= 2:
                return True
            return False
    raise Exception(f'invalid state: {jokers=}, {cards=}')


def three_of_a_kind(cards: str) -> bool:
    # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    jokers = cards.count(JOKER)
    if jokers >= 3:
        return True
    for c in set(cards):
        if c == JOKER:
            continue
        if cards.count(c) + jokers >= 3:
            return True
    return False

def two_pair(cards: str) -> bool:
    # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    jokers = cards.count(JOKER)
    pairs = 0
    for c in set(cards):
        if c == JOKER:
            continue
        if cards.count(c) + jokers >= 2:
            jokers -= 2- cards.count(c)
            pairs += 1
    if jokers >= 2:
        pairs += 1
    return pairs >= 2


def pair(cards: str) -> bool:
    # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    jokers = cards.count(JOKER)
    if jokers >= 2:
        return True
    for c in set(cards):
        if cards.count(c) + jokers >= 2:
            return True
    return False

    # High card, where all cards' labels are distinct: 23456
FACES = 'AKQT98765432J'
FACE_VALUES = {f: len(FACES)-i for i,f in enumerate(FACES)}
print(f'{FACE_VALUES=}')
def hands_sort(hand: tuple[str, int]) -> int:
    print(f'hands_sort{hand=})')
    val = 0
    factor = len(FACES)
    for c in reversed(hand[0]):
        val += FACE_VALUES[c] * factor
        print(f'{val=} of {c=}')
        factor *= factor
    return val

def main(text: str) -> int:
    hands = text.splitlines()
    hands = list(map(str.split, hands))
    print(f'{hands=}')
    fives = []
    fours = []
    fulls = []
    threes= []
    two_pairs = []
    pairs = []
    highs = []
    for hand in hands:
        if five_of_a_kind(hand[0]):
            hand.append('five')
            fives.append(hand)
        elif four_of_a_kind(hand[0]):
            hand.append('four')
            fours.append(hand)
        elif full_house(hand[0]):
            hand.append('full_house')
            fulls.append(hand)
        elif three_of_a_kind(hand[0]):
            hand.append('three')
            threes.append(hand)
        elif two_pair(hand[0]):
            hand.append('twopair')
            two_pairs.append(hand)
        elif pair(hand[0]):
            hand.append('pair')
            pairs.append(hand)
        else:
            hand.append('high')
            highs.append(hand)
    fives.sort(key=hands_sort, reverse=True)
    fours.sort(key=hands_sort, reverse=True)
    fulls.sort(key=hands_sort, reverse=True)
    threes.sort(key=hands_sort, reverse=True)
    two_pairs.sort(key=hands_sort, reverse=True)
    pairs.sort(key=hands_sort, reverse=True)
    highs.sort(key=hands_sort, reverse=True)
    sorted_hands = [*fives, *fours, *fulls, *threes, *two_pairs, *pairs, *highs]
    print(f'{sorted_hands=}')
    total = 0
    for i, hand in enumerate(sorted_hands):
        value = (len(sorted_hands) - i) * int(hand[1])
        print(f'Value of {hand=} =  {value}')
        total += value

    return total




if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    text = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''
    def test(self):
        self.assertEqual(5905, main(self.text))
