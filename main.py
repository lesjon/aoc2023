import unittest

    
def d4p1(text: str) -> int:
    blocks = text.split('\n\n')
    seeds = blocks[0].split()[1:]
    seeds = list(map(int,seeds))
    print(f'{seeds=}')
    resource_map = dict()
    for block in blocks[1:]:
        print(f'{block=}')
        lines = block.splitlines()
        from_to, _ = lines[0].split()
        map_from, _, map_to = from_to.split('-')
        resource_map.update({(map_from, map_to):dict()})
        for line in lines[1:]:
            dest_start, src_start, count = line.split()
            dest_start, src_start, count = int(dest_start), int(src_start), int(count)
            resource_map[(map_from, map_to)].update({range(src_start, src_start + count): (src_start, dest_start)})
        print(resource_map)
    lowest_location = 999999999999999
    for seed in seeds:
        value = seed
        resource = 'seed'
        while resource != 'location':
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
        lowest_location = min(lowest_location, value)

    return lowest_location



def main():
    with open('input.txt', 'r') as f:
        text = f.read()

    print(d4p1(text))

if __name__ == "__main__":
    main()
# The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:
#
#     Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
#     Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
#     Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
#     Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
#
# So, the lowest location number in this example is 35.
#
# What is the lowest location number that corresponds to any of the initial seed numbers?

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
        self.assertEqual(35, d4p1(self.text))

