import unittest
import json

def parse_instr(workflow: str):
    label, steps = workflow.split('{')
    steps = steps[:-1]
    steps = steps.split(',')
    instrs = []
    for step in steps:
        if ':' in step:
            comparison, target = step.split(':')
            if '>' in comparison:
                key, value = comparison.split('>')
                comparison = lambda item, k=key, i=int(value): item[k] > i
            elif '<' in comparison:
                key, value = comparison.split('<')
                comparison = lambda item, k=key, i=int(value): item[k] < i
            else:
                raise
        else:
            comparison, target = lambda i: True, step
        instrs.append((comparison, target))

    return label, instrs

def parse_item(item: str):
    item = item.replace('x', '"x"')
    item = item.replace('a', '"a"')
    item = item.replace('m', '"m"')
    item = item.replace('s', '"s"')
    item = item.replace('=', ':')
    return json.loads(item)


def parse(text: str) -> tuple:
    workflows, items = map(str.splitlines, text.split('\n\n'))
    workflows = map(parse_instr, workflows)
    items = map(parse_item, items)
    return workflows, items


def main(text: str) -> int:
    workflows, items = parse(text)
    workflows = dict(workflows)
    items = list(items)
    print(f'{workflows=}\n{items=}')
    total = 0
    END_STATES = {'R', 'A'}
    for i in items:
        print(f'{i=}')
        current = 'in'
        while not current in END_STATES:
            print(f'{current=}')
            workflow = workflows[current]
            for step in workflow:
                print(f'{step=}')
                if step[0](i):
                    current = step[1]
                    break
        if current == 'A':
            total+= sum(i.values())

    return total


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text))

class Tests(unittest.TestCase):

    def test(self):
        text = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''
        self.assertEqual(19114, main(text))
