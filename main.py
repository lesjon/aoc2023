from typing import Self
import unittest
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    z: int
    def same_xy(self, o: Self) -> bool:
        return self.x == o.x and self.y == o.y

    def __sub__(self, rhs: int) -> Self:
        self.z -= rhs
        return self


@dataclass(unsafe_hash=True)
class Brick:
    id: int
    l: Point
    h: Point

    def points(self: Self) -> list[Point]:
        start, end = self.l, self.h
        result = []
        xs = sorted([start.x, end.x])
        xs[1] += 1
        ys = sorted([start.y, end.y])
        ys[1] += 1
        zs = sorted([start.z, end.z])
        zs[1] += 1
        for x in range(*xs):
            for y in range(*ys):
                for z in range(*zs):
                    result.append(Point(x,y,z))
        return result
    
    def get_by_xy(self: Self, rhs: Point) -> Point | None:
        for p in self.points():
            if p.x == rhs.x and p.y == rhs.y:
                return p
        return None

    def bottom_of_brick(self: Self) -> int:
        return self.l.z

    def overlap(self: Self, rhs: Self) -> list[tuple[Point, Point]]:
        o_points = rhs.points()
        result = [(p, self.get_by_xy(p)) for p in o_points]
        return list(filter(lambda t: t[1] is not None, result))


id = 0
def parse(text: str) -> list[Brick]:
    global id
    result = []
    for line in text.splitlines():
        match line.split(','):
            case (lx,ly,lz_rx, ry,rz):
                lz, rx = lz_rx.split('~')
                lx,ly,lz, rx,ry,rz = int(lx),int(ly),int(lz),int(rx),int(ry),int(rz)
                if lz < rz:
                    brick = Brick(id, Point(lx,ly,lz),Point(rx,ry,rz))
                    id += 1
                else:
                    brick = Brick(id, Point(rx,ry,rz),Point(lx,ly,lz))
                    id += 1
                result.append(brick)
    return result


def main(text: str) -> int:
    bricks = parse(text)
    for brick in bricks:
        print(f'{brick=}')
    print()
    bricks = sorted(bricks, key=Brick.bottom_of_brick)
    fallen_bricks: dict[Brick, set[int]] = {}
    for brick in bricks:
        dist = brick.bottom_of_brick() - 1
        lean_ons = set()
        for fallen in fallen_bricks:
            overlap = fallen.overlap(brick)
            print(f'{overlap=} for {brick.id=} {fallen.id=}')
            distances = list(map(lambda fp_bp: fp_bp[1].z, overlap))
            if len(distances) > 0:
                min_dist = min(distances) - 1
                if min_dist < dist:
                    dist = min_dist
                    lean_ons = {fallen}
                if min_dist == dist:
                    lean_ons.add(fallen)

        for fallen in lean_ons:
            fallen_bricks[fallen].add(brick.id)
        brick = Brick(brick.id, brick.l - dist, brick.h - dist)
        fallen_bricks[brick] = set()

    takeable = 0
    for brick, lean_ons_check in fallen_bricks.items():
        print(f'fallen_brick:{brick} ,{lean_ons_check}, {takeable=}')
        for lean_ons in fallen_bricks.values():
            if brick in lean_ons and len(lean_ons) > 1:
                takeable += 1
    return takeable

if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):
    def test(self):
        text = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''
        self.assertIs(5,main(text))
