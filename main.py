import unittest

def parse(text: str) -> list[str]:
    text = text.replace('\n', '')
    return text.split(',')

def _hash(s: str) -> int:
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current

def run(text: str) -> int:
    parts = parse(text)
    return sum(map(_hash, parts))

if __name__ == "__main__":
    with open('input.txt') as f:
        print(run(f.read()))

class Tests(unittest.TestCase):
    def test(self):
        text = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n'
        self.assertEqual(1320, run(text))

    def test_hash(self):
        text = 'HASH'
        self.assertEqual(52, _hash(text))

    def test_rn(self):
        text = '''rn=1'''
        self.assertEqual(30, run(text))

    def test_cm(self):
        text = '''cm-'''
        self.assertEqual(253, run(text))
        
    def test_qp(self):
        text = 'qp=3'
        self.assertEqual(97, run(text))

    def test_cm2(self):
        text = 'cm=2'
        self.assertEqual(47, run(text))

    def test_qpminus(self):
        text = 'qp-'
        self.assertEqual(14, run(text))

    def test_pc4(self):
        text = 'pc=4'
        self.assertEqual(180, run(text))

    def test_ot9(self):
        text = 'ot=9'
        self.assertEqual( 9, run(text))

    def test_ab(self):
        text = 'ab=5'
        self.assertEqual( 197, run(text))

    def test_pcminus(self):
        text = 'pc-'
        self.assertEqual( 48, run(text))

    def test_pc6(self):
        text = 'pc=6'
        self.assertEqual( 214, run(text))

    def test_ot7(self):
        text = 'ot=7'
        self.assertEqual( 231, run(text))



