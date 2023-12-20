# Advent Of Code 2023, day 20, part 2
# http://adventofcode.com/2023/day/20
# solution by ByteCommander, 2023-12-20
from collections import deque
from itertools import count
from math import lcm
from typing import TextIO, override

from aoc_tools.lib import run

FINAL_NODE = "rx"
BUTTON = "button"
BROADCASTER = "broadcaster"


class PulseModule:
    def __init__(self, name: str, connections: list[str], symbol: str = ""):
        self.name = name
        self.symbol = symbol
        self.connections = connections
        self.dependencies: list[str] = []

    @override
    def __repr__(self):
        return f"{self.symbol}{self.name}({len(self.dependencies)})"

    def trigger(self, pulse: bool, source: str) -> list[(str, bool, str)]:
        # Broadcaster module implementation: simply forward incoming pulse to all connections
        return [(conn, pulse, self.name) for conn in self.connections]

    def register_input(self, input_name: str) -> None:
        self.dependencies.append(input_name)

    @staticmethod
    def new_module(definition: str) -> "PulseModule":
        name, conns_ = definition.split(" -> ")
        conns = conns_.split(", ")
        if name == BROADCASTER:
            return PulseModule(name, conns)
        t, name = name[0], name[1:]
        if t == "%":
            return FlipFlopModule(name, conns)
        elif t == "&":
            return ConjunctionModule(name, conns)
        else:
            raise ValueError(f"Unknown type symbol '{t}' for module '{name}'.")


class FlipFlopModule(PulseModule):
    @override
    def __init__(self, name: str, connections: list[str]):
        super().__init__(name, connections, "%")
        self.state = False

    @override
    def trigger(self, pulse: bool, source: str) -> list[(str, bool, str)]:
        if pulse:  # ignore high pulses
            return []
        else:  # low pulse: flip state, then broadcast new state to all connections
            self.state = not self.state
            return super().trigger(self.state, source)


class ConjunctionModule(PulseModule):
    @override
    def __init__(self, name: str, connections: list[str]):
        super().__init__(name, connections, "&")
        self.inputs: dict[str, bool] = {}

    @override
    def trigger(self, pulse: bool, source: str) -> list[(str, bool, str)]:
        self.inputs[source] = pulse  # update input memory
        # NAND logic: broadcast low pulse if all inputs were high last, else low
        return super().trigger(not all(self.inputs.values()), source)

    @override
    def register_input(self, input_name: str) -> None:
        super().register_input(input_name)
        self.inputs[input_name] = False


class OutputModule(PulseModule):
    @override
    def __init__(self, name: str):
        super().__init__(name, [], "!")

    @override
    def trigger(self, pulse: bool, source: str) -> list[(str, bool, str)]:
        # print(f"OUTPUT at node {self.name} (from {source}): {"high" if pulse else "low"}")
        return []


def main(file: TextIO):
    modules: dict[str, PulseModule] = {}
    for line in file:
        pm = PulseModule.new_module(line.strip())
        modules[pm.name] = pm

    for pm in list(modules.values()):  # copying values for iteration to allow modifying dict in place
        for conn in pm.connections:
            if conn not in modules:
                modules[conn] = OutputModule(conn)
            modules[conn].register_input(pm.name)  # register incoming connections on each module

    # Assume that the FINAL_NODE (rx) is always the result of a conjunction, so we can cut off one step and simplify
    # the problem from "make FINAL_NODE receive low" to "make all inputs of FINAL_NODE's predecessor fire high".
    # Then we analyze independently for each of the final inputs when they end up firing high.

    def recurse_deps(_module: PulseModule, _deps: list[PulseModule]) -> list[PulseModule]:
        for _dep in _module.dependencies:
            if (_m := modules[_dep]) not in _deps:
                _deps.append(_m)
                recurse_deps(_m, _deps)
        return _deps

    final_conjunction: ConjunctionModule = modules[modules[FINAL_NODE].dependencies[0]]
    fin_deps: dict[str, list[PulseModule]] = {
        final_in: recurse_deps(modules[final_in], [])
        for final_in in final_conjunction.dependencies
    }

    # Assume it is enough to look at the states of the flipflops in each dependency sub-graph to determine
    # how long a cycle is, ignoring the cached inputs of the conjunctions.

    flipflop_graphs = {
        fin: [dep for dep in deps if isinstance(dep, FlipFlopModule)] for fin, deps in fin_deps.items()
    }
    # print(*flipflop_graphs.items(), sep="\n")

    # Observation shows that each sub-graph sends the needed high signal to the final conjunction during the same
    # cycle after which all flipflop states are reset back to the original state (all low).
    # Therefore, we just search for the flipflop reset cycle lengths.

    # end of preparations
    cycles: dict[str, int] = {}
    for i in count(1):
        # simulate the signal flow during one full input cycle
        signals: deque[(str, bool, str)] = deque([(BROADCASTER, False, BUTTON)])
        while len(signals):
            module_name, pulse, source = signals.popleft()
            # if module_name == final_conjunction.name and final_conjunction.inputs[source]:
            #     print(f"Final Conjunction input '{source}' is high in cycle {i}")
            pm = modules[module_name]
            signals.extend(pm.trigger(pulse, source))

        # check the individual sub-graph behind each input of the final conjunction for a full cycle,
        # i.e. for all flipflop states to reset back to their original state (all low)
        for fin, deps in flipflop_graphs.items():
            if fin not in cycles and all(d.state is False for d in deps):
                print(f"Flipflop state reset for dependencies of '{fin}' after {i} cycles")
                cycles[fin] = i
        if len(cycles) == len(flipflop_graphs):
            break  # found a cycle for each final conjunction input

    # the total count after which all sub-graphs reset their state at the same time is the lowest common multiple
    total_cycles = lcm(*cycles.values())
    print(f"After {total_cycles} cycles in total, '{FINAL_NODE}' receives the start signal.")


# test case modified to also use "rx" instead of "output" as final node, for simplification
TEST_INPUT = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
