import unittest
from typing import Optional
import math


MIN_EXLUSIVE = 0
MAX_INCLUSIVE = 4000

class WorkflowStep:
    def __init__(self, key: str='', limit_type: Optional[str]=None, limit: int=0, target: str='') -> None:
        self.key = key
        self.limit_type = limit_type
        self.limit = limit
        self.target = target

    def __repr__(self) -> str:
        return f'Step ({self.key} {self.limit_type} {self.limit})'

class Workflow:
    def __init__(self, steps: list[WorkflowStep]) -> None:
        self.steps = steps
    def __repr__(self) -> str:
        return f'Workflow ({self.steps})'

def parse_instr(workflow: str) -> tuple[str, Workflow]:
    label, steps = workflow.split('{')
    steps = steps[:-1]
    steps = steps.split(',')
    instrs = []
    for step in steps:
        workflow_step = WorkflowStep()
        if ':' in step:
            key_range, target = step.split(':')
            workflow_step.target = target
            if '>' in key_range:
                key, value = key_range.split('>')
                workflow_step.limit_type = '>'
                workflow_step.key = key
                workflow_step.limit = int(value)
            elif '<' in key_range:
                key, value = key_range.split('<')
                workflow_step.limit_type = '<'
                workflow_step.key = key
                workflow_step.limit = int(value)
            else:
                raise
        else:
            workflow_step.target = step
        instrs.append(workflow_step)
    return label, Workflow(instrs)

pos_id = 0
def get_positions(target: str, workflows: dict[str, Workflow]) -> set[tuple[str, int, int]]:
    global pos_id
    result = set()
    for key, instrs in workflows.items():
        for i, instr in enumerate(instrs.steps):
            if instr.target == target:
                result.add((key, i, pos_id))
                pos_id += 1
    return result



def parse(text: str) -> dict[str, Workflow]:
    workflows, _ = map(str.splitlines, text.split('\n\n'))
    workflows = map(parse_instr, workflows)
    workflows = dict(workflows)
    return workflows

def apply_step_pass(target_step, pos_range: dict[str, list[int]]):
    match target_step.limit_type: 
        case '>':
            pos_range[target_step.key][0] = max(pos_range[target_step.key][0], target_step.limit) 
        case '<':
            pos_range[target_step.key][1] = min(pos_range[target_step.key][1], target_step.limit-1) 
        case None:
            pass

def apply_step_stop(step, pos_range: dict[str,list[int]]):
    match step.limit_type: 
        case '>':
            pos_range[step.key][1] = min(pos_range[step.key][1], step.limit) 
        case '<':
            pos_range[step.key][0] = max(pos_range[step.key][0], step.limit-1) 
        case None:
            pass

def main(text: str) -> int:
    workflows = parse(text)
    print(f'{workflows=}')
    positions = get_positions('A', workflows)
    positions = {p: {"x":[MIN_EXLUSIVE, MAX_INCLUSIVE],"m":[MIN_EXLUSIVE, MAX_INCLUSIVE],"a":[MIN_EXLUSIVE, MAX_INCLUSIVE],"s":[MIN_EXLUSIVE, MAX_INCLUSIVE],} for p in positions}
    print(f'while {len(positions)=} {positions=}')
    print()
    total = 0
    while positions:
        pos = next(iter(positions.keys()))
        print('pos', pos)
        pos_range = positions.pop(pos)
        workflow = workflows[pos[0]]
        target_step = workflow.steps[pos[1]] 
        apply_step_pass(target_step, pos_range)
        print(f'after target step {pos=} {pos_range=}')
        for step in workflow.steps[:pos[1]]:
            print(f'other {step=}')
            apply_step_stop(step, pos_range)
            print(f'after step:{pos_range=}')
        if pos[0] != 'in':
            positions.update({p: {"x":[pos_range["x"][0], pos_range["x"][1]],"m":[pos_range["m"][0], pos_range["m"][1]],"a":[pos_range["a"][0], pos_range["a"][1]],"s":[pos_range["s"][0], pos_range["s"][1]],} for p in get_positions(pos[0], workflows)})
        else:
            range_lens = list(map(lambda r: r[1] - r[0], pos_range.values()))
            print('range_lens', range_lens)
            total += math.prod(range_lens)

        print(f'{len(positions)=} {positions=}')

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
        self.assertEqual(167409079868000, main(text))

    def test_smol(self):
        text = '''pv{a>25:R,A}
hdj{x<40:R,m>5:A,pv}
qqz{s>20:qs,m<15:hdj,R}
in{s<10:px,qqz}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''
        self.assertEqual(20581350160000, main(text))
