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


def execute(instr: str, boxes: list[list[str]], lenses: dict[str,int]):
    if instr.endswith('-'):
        id = instr.rstrip('-')
        i = _hash(id)
        l = boxes[i]
        if id in l:
            l.remove(id)
            lenses.pop(id)
    elif '=' in instr:
        id, f = instr.split('=')
        lenses[id] = int(f)
        i = _hash(id)
        box = boxes[i]
        if not id in box:
            box.append(id)
    else:
        raise Exception(f"Unknown execution '{instr}'")


def run(text: str) -> int:
    parts = parse(text)
    boxes = [[] for _ in range(256)]
    lenses: dict[str, int] = {}
    for instr in parts:
        execute(instr, boxes, lenses)

    focal_power = 0
    for i, box in enumerate(boxes):
        for j, lens_id in enumerate(box):
            focal_power += (1+i) * (1+j) * lenses[lens_id]
    return focal_power


# To confirm that all of the lenses are installed correctly, add up the focusing power of all of the lenses. The focusing power of a single lens is the result of multiplying together:
#     One plus the box number of the lens in question.
#     The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
#     The focal length of the lens.



if __name__ == "__main__":
    with open('input.txt') as f:
        print(run(f.read()))

class Tests(unittest.TestCase):
    def test(self):
        text = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n'
        self.assertEqual(145, run(text))
