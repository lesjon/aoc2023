import unittest


def main(text: str) -> int:
    total = 0
    for line in text.splitlines():
        nums = list(map(int, line.split()))
        prevs = []
        while not all(map(lambda x: x == 0, nums)):
            print(f'{len(nums)=}')
            next_nums = []
            for i in range(len(nums)):
                print(f'{i=} {nums=} {prevs=}')
                if i == len(nums)-1:
                    continue
                elif i == 0:
                    prevs.append(nums[0])
                next_nums.append(nums[i+1] - nums[i])
            nums = next_nums
        current = 0
        for prev in reversed(prevs):
            print(f'{prev=} {current=}')
            current = prev - current
        total += current
        print(f'{total=}')
    return total



if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    text = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''
    def test(self):
        self.assertEqual(2, main(self.text))
