import unittest
from typing import Optional

def flip_flop(state: tuple[str, list[str], dict[str, int]| int], signal: int) -> tuple[tuple[str, list[str], dict[str, int] | int], Optional[int]]:
# Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
    assert state[0] == '%'
    assert isinstance(state[2], int)
    if signal == 1:
        return state, None
    elif signal == 0:
        return (*state[:2], 1-state[2]), 1-state[2]
    raise

def conjunction(state: tuple[str, list[str], dict[str, int]| int], signal: tuple[str, int]) -> tuple[tuple[str, list[str], dict[str, int]| int], int]:
# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    assert state[0] == '&'
    assert isinstance(state[2], dict)
    state[2][signal[0]] = signal[1]
    return state, 1 if sum(state[2].values()) == len(state[2]) else 0


def parse(text: str) -> dict[str, tuple[str, list[str], dict[str, int]| int]]:
    modules = {}
    connections = []
    for line in text.splitlines():
        match line.split():
            case ('broadcaster', '->', *targets):
                targets = list(map(lambda t: t.rstrip(',') , targets))
                for t in targets:
                    connections.append(('broadcaster', t))
                modules['broadcaster'] = (None, targets, None)
            case (id, '->', *targets):
                ty, label = id[0], id[1:]
                targets = list(map(lambda t: t.rstrip(',') , targets))
                for t in targets:
                    connections.append((label, t))
                state = dict() if ty == '&' else 0
                modules[label] = (ty, targets, state)
            case other:
                raise Exception(f'Parse error: {other}')
    print(f'{connections=}')
    print(f'{modules=}')
    for label, target in connections:
        if target == 'output':
            continue
        if isinstance( modules[target][2], dict):
            modules[target][2][label] = 0
    return modules

def main(text: str, presses: int) -> int:
    modules = parse(text)
    low_pulses = high_pulses = 0
    print(f'{modules=}')
    for i in range(presses):
        print('for', i)
        signals: list[tuple[str, int]] = [('broadcaster', 0)]
        print('while')
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
            print(f'{signal=}')
            module = modules[signal[0]]
            print(f'\n{module=} -{{', end='')
            match module[0]:
                case '&':
                    modules[signal[0]], output = conjunction(module, signal)
                    for t in module[1]:
                        if output == 0:
                            low_pulses += 1
                        else:
                            high_pulses += 1
                        if t != 'output':
                            print(f'{output=}}}-> {t}')
                            signals.append((t, output))
                case '%':
                    modules[signal[0]], output = flip_flop(module, signal[1])
                    if not output is None:
                        for t in module[1]:
                            if t == 0:
                                low_pulses += 1
                            else:
                                high_pulses += 1
                            if t != 'output':
                                signals.append((t, output))
                    print(output)
                case None:
                    output = signal[1]
                    for t in module[1]:
                        if output == 0:
                            low_pulses += 1
                        else:
                            high_pulses += 1
                        if t != 'output':
                            print(f'{output=}}}-> {t}')
                            signals.append((t, output))
                case other:
                    raise Exception(f'Unknown module: {other}')
            print(f'{modules=}')
        print(modules)
    print(low_pulses, high_pulses)
    return low_pulses * high_pulses


    


if __name__ == "__main__":
    with open('input.txt', 'r') as f:
        text = f.read()
    print(main(text), 1000)

class Tests(unittest.TestCase):
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
