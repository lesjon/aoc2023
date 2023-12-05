import unittest

    
def d4p2(text: str) -> int:
    blocks = text.split('\n\n')
    seeds = blocks[0].split()[1:]
    seeds = list(map(int,seeds))
    seed_ranges = []
    seed_num = 0
    for i in range(len(seeds)):
        if i % 2 == 1:
            continue
        seed_ranges.append(range(seeds[i], seeds[i]+seeds[i+1]))
        seed_num  += seeds[i+1]

    del seeds

    print(f'{seed_ranges=} {seed_num=}')
    resource_map = dict()
    for block in blocks[1:]:
        print(f'{block=}')
        lines = block.splitlines()
        from_to, _ = lines[0].split()
        map_from, _, map_to = from_to.split('-')
        resource_map.update({(map_to, map_from):dict()})
        for line in lines[1:]:
            dest_start, src_start, count = line.split()
            dest_start, src_start, count = int(dest_start), int(src_start), int(count)
            resource_map[(map_to, map_from)].update({range(dest_start, dest_start + count): (dest_start, src_start)})
        print(resource_map)
    lowest_location = 999999999999999
    for i, location in enumerate(range(lowest_location)):
        if i % 10000 == 0:
            print(f'test location:{i}')
        value = location
        resource = 'location'
        while resource != 'seed':
            for key in resource_map:
                if key[0] != resource:
                    continue
                try:
                    ranges = resource_map[key]
                    for r in ranges:
                        if value in r:
                            value = ranges[r][1] + (value - ranges[r][0])
                            break
                except KeyError:
                    pass  # value maps to itself
                resource = key[1]
        for seed_range in seed_ranges:
            if value in seed_range:
                return location



def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d4p2(text))

if __name__ == "__main__":
    main()

class Tests(unittest.TestCase):
    text = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
    def test(self):
        self.assertEqual(46, d4p2(self.text))

