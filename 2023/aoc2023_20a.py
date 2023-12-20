# Advent Of Code 2023, day 20, part 1
# http://adventofcode.com/2023/day/20
# solution by ByteCommander, 2023-12-20
from collections import deque
from typing import TextIO, override

from aoc_tools.lib import run

BUTTON_PRESSES = 1000
BUTTON = "button"
BROADCASTER = "broadcaster"


class PulseModule:
    def __init__(self, name: str, connections: list[str]):
        self.name = name
        self.connections = connections

    def trigger(self, pulse: bool, source: str) -> list[(str, bool, str)]:
        # Broadcaster module implementation: simply forward incoming pulse to all connections
        return [(conn, pulse, self.name) for conn in self.connections]

    def register_input(self, input_name: str) -> None:
        pass  # only needed by some implementations

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
        super().__init__(name, connections)
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
        super().__init__(name, connections)
        self.inputs: dict[str, bool] = {}

    @override
    def trigger(self, pulse: bool, source: str) -> list[(str, bool, str)]:
        self.inputs[source] = pulse  # update input memory
        # NAND logic: broadcast low pulse if all inputs were high last, else low
        return super().trigger(not all(self.inputs.values()), source)

    @override
    def register_input(self, input_name: str) -> None:
        self.inputs[input_name] = False


class OutputModule(PulseModule):
    @override
    def __init__(self, name: str):
        super().__init__(name, [])

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

    counts: list[int] = [0, 0]  # low, high
    for i in range(BUTTON_PRESSES):
        # print("Cycle", i+1)
        signals: deque[(str, bool, str)] = deque([(BROADCASTER, False, BUTTON)])
        while len(signals):
            module_name, pulse, source = signals.popleft()
            counts[pulse] += 1
            # print(f"{source} -{"high" if pulse else "low"}-> {module_name}")
            pm = modules[module_name]
            signals.extend(pm.trigger(pulse, source))
        # print("FlipFlops:", {m.name: [0, 1][m.state] for m in modules.values() if isinstance(m, FlipFlopModule)})
        # print("Conjunctions:", {
        #     m.name: "".join("01"[v] for v in m.inputs.values())
        #     for m in modules.values() if isinstance(m, ConjunctionModule)
        # })

    low_count, high_count = counts
    print(f"After pressing the button {BUTTON_PRESSES} times, {low_count} low and {high_count} high pulses were sent.")
    print(f"The signal product is {low_count * high_count}.")


TEST_INPUT = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

if __name__ == "__main__":
    run(main, TEST_INPUT, test_only=False)
