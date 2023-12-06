import unittest

    
def distance(time:int, hold: int) -> int:
    return (time - hold) * hold


def d5p1(text: str) -> int:
    times, records = text.splitlines()
    times, records = times.split()[1:], records.split()[1:]
    times, records = map(int, times), map(int, records)
    total = 1
    for time, record in zip(times, records):
        low = 0
        for lo in range(time):
            if distance(time, lo) > record:
                break
            low = lo
        high = time
        for hi in reversed(range(time)):
            if distance(time, hi) > record:
                break
            high = hi
        print(f'{low=} {high=}')
        options =high - low - 1
        print(f'{options=}')
        total *= options
    return total


def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d5p1(text))

if __name__ == "__main__":
    main()

class Tests(unittest.TestCase):
# This document describes three races:
#
#     The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
#     The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
#     The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.
#
# Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.
#
# So, because the first race lasts 7 milliseconds, you only have a few options:
#
#     Don't hold the button at all (that is, hold it for 0 milliseconds) at the start of the race. The boat won't move; it will have traveled 0 millimeters by the end of the race.
#     Hold the button for 1 millisecond at the start of the race. Then, the boat will travel at a speed of 1 millimeter per millisecond for 6 milliseconds, reaching a total distance traveled of 6 millimeters.
#     Hold the button for 2 milliseconds, giving the boat a speed of 2 millimeters per millisecond. It will then get 5 milliseconds to move, reaching a total distance of 10 millimeters.
#     Hold the button for 3 milliseconds. After its remaining 4 milliseconds of travel time, the boat will have gone 12 millimeters.
#     Hold the button for 4 milliseconds. After its remaining 3 milliseconds of travel time, the boat will have gone 12 millimeters.
#     Hold the button for 5 milliseconds, causing the boat to travel a total of 10 millimeters.
#     Hold the button for 6 milliseconds, causing the boat to travel a total of 6 millimeters.
#     Hold the button for 7 milliseconds. That's the entire duration of the race. You never let go of the button. The boat can't move until you let go of the button. Please make sure you let go of the button so the boat gets to move. 0 millimeters.
#
# Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.
#
# In the second race, you could hold the button for at least 4 milliseconds and at most 11 milliseconds and beat the record, a total of 8 different ways to win.
#
# In the third race, you could hold the button for at least 11 milliseconds and no more than 19 milliseconds and still beat the record, a total of 9 ways you could win.
#
# To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).
#
# Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?
    text = ''' Time:      7  15   30
Distance:  9  40  200
'''
    def test(self):
        self.assertEqual(288, d5p1(self.text))

