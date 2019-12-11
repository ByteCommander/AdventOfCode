# Advent Of Code 2019, day 11, part 1)
# http://adventofcode.com/2019/day/11
# solution by ByteCommander, 2019-12-11

import asyncio
import inspect
from asyncio import Queue

BLACK = 0
WHITE = 1


async def main():
    with open("inputs/aoc2019_11.txt") as file:
        mem = [int(x) for x in file.read().split(",")]

    x, y, d = 0, 0, 0
    squares = {(x, y): BLACK}

    comp = IntComputer(mem)
    asyncio.create_task(comp.run())  # start computer asynchronously

    while not comp.terminated:
        await comp.inp.put(squares.get((x, y), BLACK))  # feed color sensor
        squares[(x, y)] = await comp.out.get()  # paint the square
        d = (d + await comp.out.get() * 2 - 1) % 4  # 0: LEFT(-1), 1: RIGHT(+1)
        if d == 0:  # North
            y -= 1
        elif d == 1:  # East
            x += 1
        elif d == 2:  # South
            y += 1
        elif d == 3:  # West
            x -= 1
        else:
            raise RuntimeError("Invalid direction")

    print(f"The paint bot will visit {len(squares)} squares at least once.")


class Instruction:
    OUT = object()  # argument annotation marker

    def __init__(self, func):
        self.func = func
        params = inspect.signature(func).parameters  # note: have to ignore "self"
        self.argc = len(params) - 1
        self.write_arg = next((
            list(params.keys()).index(name) - 1 for name, param in params.items() if param.default is Instruction.OUT
        ), None)


def OPCODE(op):
    def decorator(func):
        func.opcode = op
        return func

    return decorator


class IntComputer:
    def __new__(cls, *args, **kwargs):
        cls.INSTRUCTIONS = {}
        for name, func in inspect.getmembers(cls, inspect.isfunction):
            if (op := getattr(func, "opcode", None)) is not None:
                cls.INSTRUCTIONS[op] = Instruction(func)
        return super().__new__(cls)

    def __init__(self, mem):
        self.mem = mem
        self.inp = Queue()
        self.out = Queue()
        self.i = 0
        self.rel_base = 0
        self.terminated = False

    async def run(self):
        while not self.terminated:
            await self.call_instr()

    async def call_instr(self):
        # print("i:", self.i, self.mem[self.i], end=" ")
        modes, op = divmod(self.mem[self.i], 100)
        arg_modes = map(int, "{:03.0f}".format(modes)[::-1])
        self.i += 1

        if not (instr := self.INSTRUCTIONS.get(op)):
            raise RuntimeError(f"Illegal opcode at pos {self.i}: {op}")

        args = list(zip(self.mem[self.i:self.i + instr.argc], arg_modes))
        self.i += instr.argc
        # print(op, instr.func.__name__, *zip(args, (self.read(x, mode) for x, mode in args)))

        value = await instr.func(self, *(self.read(x, mode) for x, mode in args))
        if instr.write_arg is not None:
            # print("write", value, *args[instr.write_arg])
            self.write(value, *args[instr.write_arg])

    def read(self, xx, mode):
        try:
            if mode == 0:
                return self.mem[xx]
            elif mode == 1:
                return xx
            elif mode == 2:
                return self.mem[self.rel_base + xx]
            else:
                raise RuntimeError(f"Illegal read arg mode {mode}")
        except IndexError:
            return 0

    def write(self, value, xx, mode):
        if mode == 0:
            index = xx
        elif mode == 2:
            index = self.rel_base + xx
        else:
            raise RuntimeError(f"Illegal write arg mode {mode}")

        if index >= len(self.mem):
            self.mem += [0] * (index - len(self.mem) + 1)
        self.mem[index] = value

    @OPCODE(1)
    async def op_add(self, a, b, c=Instruction.OUT):
        return a + b

    @OPCODE(2)
    async def op_mul(self, a, b, c=Instruction.OUT):
        return a * b

    @OPCODE(3)
    async def op_inp(self, a=Instruction.OUT):
        return await self.inp.get()

    @OPCODE(4)
    async def op_out(self, a):
        await self.out.put(a)

    @OPCODE(5)
    async def op_jit(self, a, b):
        if a:
            self.i = b

    @OPCODE(6)
    async def op_jif(self, a, b):
        if not a:
            self.i = b

    @OPCODE(7)
    async def op_low(self, a, b, c=Instruction.OUT):
        return int(a < b)

    @OPCODE(8)
    async def op_eqv(self, a, b, c=Instruction.OUT):
        return int(a == b)

    @OPCODE(9)
    async def op_rel(self, a):
        self.rel_base += a

    @OPCODE(99)
    async def op_trm(self):
        self.terminated = True


if __name__ == "__main__":
    asyncio.run(main())
