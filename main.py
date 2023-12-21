import unittest
from typing import Optional

class Module:
    def __init__(self, name: str, version: str, targets: list[str], state: None | dict[str,int] | int) -> None:
        self.name = name
        self.targets = targets
        self.state = state
        self.version = version

    def __repr__(self) -> str:
        return f'{self.version}{self.name} [ {self.state} ] -> {self.targets}'

def flip_flop(module: Module, signal: int) -> tuple[Module, Optional[int]]:
# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    assert module.version == '%'
    assert isinstance(module.state, int)
    if signal == 1:
        return module, None
    elif signal == 0:
        module.state = 1-module.state
        return module, module.state
    raise

def conjunction(module: Module, signal: tuple[str, int]) -> tuple[Module, int]:
# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    assert module.version == '&'
    assert isinstance(module.state, dict)
    module.state[signal[0]] = signal[1]
    return module, 0 if sum(module.state.values()) == len(module.state) else 1


def parse(text: str) -> tuple[dict[str, Module], set[str]]:
    modules = {}
    outputs = set()
    connections = []
    for line in text.splitlines():
        match line.split():
            case ('broadcaster', '->', *targets):
                targets = list(map(lambda t: t.rstrip(',') , targets))
                for t in targets:
                    connections.append(('broadcaster', t))
                modules['broadcaster'] = Module('broadcaster', "", targets, None)
            case (id, '->', *targets):
                ty, label = id[0], id[1:]
                targets = list(map(lambda t: t.rstrip(',') , targets))
                for t in targets:
                    connections.append((label, t))
                state = dict() if ty == '&' else 0
                modules[label] = Module(label, ty, targets, state)
            case other:
                raise Exception(f'Parse error: {other}')
    # print(f'{connections=}')
    # print(f'{modules=}')
    for label, target in connections:
        if target in outputs:
            continue
        if target in modules:
            if isinstance( modules[target].state, dict):
                modules[target].state[label] = 0
        else:
            outputs.add(target)
    return modules, outputs

def main(text: str, max_presses: int) -> int:
    modules, outputs = parse(text)
    low_pulses = high_pulses = 0
    print(f'{modules=}')
    i = 0
    while True:
        i += 1
        print('for', i)
        # button press
        low_pulses += 1
        signals: list[tuple[str, int]] = [('broadcaster', 0)]
        while signals:
            signal = signals.pop(0)
# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -high-> output
# b -high-> con
# con -low-> output

            source_module = modules[signal[0]]
            # print(f'\n{signal[0]} -[{signal[1]}]', end='')
            for t in source_module.targets:
                # print(f'\t-> {t}')
                # print(f'{signal[1]=} {low_pulses=} {high_pulses=}') 
                low_pulses += 1 - signal[1]
                high_pulses += signal[1]
                if t == 'rx' and signal[1] == 0:
                    return i
                if t in outputs:
                    continue
                output = None
                target_module = modules[t]
                match target_module.version:
                    case '&':
                        modules[t], output = conjunction(target_module, signal)
                    case '%':
                        modules[t], output = flip_flop(target_module, signal[1])
                    case '':
                        output = signal[1]
                if output is not None:
                    signals.append((t, output))


    


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text, 1000))

class Tests(unittest.TestCase):
    def test_short(self):
        text = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''
        self.assertEqual(4*8, main(text, 1))

    def test(self):
        text = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''
        self.assertEqual(11687500, main(text, 1000))
# Here's what happens if you push the button once:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -high-> output
# b -high-> con
# con -low-> output
#
# Both flip-flops turn on and a low pulse is sent to output! However,
#   now that both flip-flops are on and con remembers a high pulse from each of its two inputs, pushing the button a second time does something different:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
#
# Flip-flop a turns off! Now, con remembers a low pulse from module a, and so it sends only a high pulse to output.
#
# Push the button a third time:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -high-> inv
# a -high-> con
# inv -low-> b
# con -low-> output
# b -low-> con
# con -high-> output
#
# This time, flip-flop a turns on, then flip-flop b turns off. However, before b can turn off,
#   the pulse sent to con is handled first, so it briefly remembers all high pulses for its inputs and sends a low pulse to output. After that,
#   flip-flop b turns off, which causes con to update its state and send a high pulse to output.
#
# Finally, with a on and b off, push the button a fourth time:
#
# button -low-> broadcaster
# broadcaster -low-> a
# a -low-> inv
# a -low-> con
# inv -high-> b
# con -high-> output
#
# This completes the cycle: a turns off, causing con to remember only low pulses and restoring all modules to their original states.
