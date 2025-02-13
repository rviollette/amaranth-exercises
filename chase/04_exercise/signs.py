from queue import SimpleQueue
from pathlib import Path
from amaranth import *
from typing import List, Tuple

# from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover
from amaranth.sim import Simulator

from util import main
from util import generate_rtlil
from util import generate_verilog

# There is no this library anymore
# from amaranth.lib.coding import PriorityEncoder

# Design Block

# Priority Encoder from LSB
class PriorityEncoderLSB(Elaboratable):
    def __init__(self, width):
        self.width = width
        self.i_bus = Signal(width)
        self.found_flag = Signal(1)
        self.bit_position = Signal(range(width))

    def elaborate(self, _: Platform) -> Module:
        m = Module()
        # m.d.comb += [self.i_bus.eq(2)]
        with m.If(self.i_bus == 0):
            m.d.comb += [
                self.found_flag.eq(0),
                self.bit_position.eq(0)
            ]
        with m.Else():
            # for i in reversed(range(self.width)):
            for i in range(self.width):
                # with m.If( (self.i_bus << 1) ):
                with m.If(self.i_bus[i] == 1):
                    m.d.comb += [
                        self.found_flag.eq(1),
                        self.bit_position.eq(self.i_bus[i])
                    ]
                    # print("for loop:")
                    # print([i])
                    # print(self.i_bus)
                    # break

        return m

class Decoder(Elaboratable):
    """Decode binary to one-hot.

    If ``n`` is low, only the ``i``-th bit in ``o`` is asserted.
    If ``n`` is high, ``o`` is ``0``.

    Parameters
    ----------
    width : int
        Bit width of the output.

    Attributes
    ----------
    i : Signal(range(width)), in
        Input binary.
    o : Signal(width), out
        Decoded one-hot.
    n : Signal, in
        Invalid, no output bits are to be asserted.
    """
    def __init__(self, width):
        self.width = width

        self.i = Signal(range(width))
        self.n = Signal()
        self.o = Signal(width)

    def elaborate(self, platform):
        m = Module()
        with m.Switch(self.i):
            for j in range(len(self.o)):
                with m.Case(j):
                    m.d.comb += self.o.eq(1 << j)
        with m.If(self.n):
            m.d.comb += self.o.eq(0)
        return m

class signs(Elaboratable):

    # Create the module input/output
    def __init__(self):
        # Input
        self.i_signed_num = Signal(8)  # 64 bits,

        # Outputs
        self.o_cal_0 = Signal(8)   # Bitwise complement (invert) it and add 1.
        self.o_cal_1 = Signal(8)   # Arithmetically negate it.
        self.o_cal_2 = Signal(8)   # Starting from the least significant bit, copy up to and including the first 1, then invert the remaining bits.

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        # Internal wire
        w_temp_one = Signal(64)
        w_first_one_in_bus = Signal(64)

        w_temp_0 = Signal(64)

        m.submodules.uut = uut = PriorityEncoderLSB(64)
        m.submodules.uut2 = uut2 = Decoder(64)

        # m.d.comb += uut.i_bus.eq(self.i_signed_num)
        m.d.comb += uut2.i.eq(self.i_signed_num)

        m.d.comb += self.o_cal_0.eq((~self.i_signed_num) + 1)
        m.d.comb += self.o_cal_1.eq(-self.i_signed_num)
        # m.d.comb += self.o_cal_2.eq(uut.found_flag)
        m.d.comb += self.o_cal_2.eq(((~self.i_signed_num) & w_temp_0 ) | w_first_one_in_bus)

        # (w_temp_0 | w_first_one_in_bus) & (~self.i_signed_num)
        # ((~self.i_signed_num) & w_temp_0 ) | w_first_one_in_bus

        m.d.comb += w_temp_one.eq(0)
        m.d.comb += w_first_one_in_bus.eq(0)

        with m.If(self.i_signed_num[0] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 0)
            m.d.comb += w_temp_0.eq(-1 << 1)
        with m.Elif(self.i_signed_num[1] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 1)
            m.d.comb += w_temp_0.eq(-1 << 2)
        with m.Elif(self.i_signed_num[2] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 2)
            m.d.comb += w_temp_0.eq(-1 << 3)
        with m.Elif(self.i_signed_num[3] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 3)
            m.d.comb += w_temp_0.eq(-1 << 4)

        with m.Elif(self.i_signed_num[4] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 4)
            m.d.comb += w_temp_0.eq(-1 << 5)
        with m.Elif(self.i_signed_num[5] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 5)
            m.d.comb += w_temp_0.eq(-1 << 6)
        with m.Elif(self.i_signed_num[6] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 6)
            m.d.comb += w_temp_0.eq(-1 << 7)
        with m.Elif(self.i_signed_num[7] == 1):
            m.d.comb += w_first_one_in_bus.eq(1 << 7)
            m.d.comb += w_temp_0.eq(-1 << 8)
        with m.Else():
            m.d.comb += w_first_one_in_bus.eq(0)
            m.d.comb += w_temp_0.eq(0)

        # for i in range(len(w_first_one_in_bus)):
            # m.d.comb += w_temp_one.eq(1 << i)
            # with m.Switch(Cat(self.i_signed_num[i])):
            #     with m.Case(0b0):
            #         m.d.comb += w_first_one_in_bus[i].eq(0)
            #         m.d.comb += w_temp_one.eq(0)
            #     with m.Case(0b1):
            #         m.d.comb += w_first_one_in_bus[i].eq(1)
            #         m.d.comb += w_temp_one.eq(1)
            #     with m.Default():
            #         m.d.comb += w_first_one_in_bus[i].eq(0)

            # with m.If(self.i_signed_num[i] == 1):
            #     m.d.comb += w_first_one_in_bus[i].eq(1)


        return m

    # Testbench Block
    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        m = Module()
        m.submodules.signs = dut = cls()

        m.d.comb += Assert(dut.o_cal_0 == dut.o_cal_1)
        m.d.comb += Assert(dut.o_cal_1 == dut.o_cal_2)
        m.d.comb += Assert(dut.o_cal_0[7] == (dut.o_cal_0.as_signed() < 0))

        return m, [dut.i_signed_num]

# Testbench Block
async def signs_tb(ctx):
    ctx.set(dut.i_signed_num, 0)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 1)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 2)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 3)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 4)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 5)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 6)

    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 9)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 10)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 12)
    await ctx.delay(1e-6)
    ctx.set(dut.i_signed_num, 15)

    print("All tests passed!")

dut = signs()   # Create the instance.
sim = Simulator(dut)    # Create the simulator.
sim.add_testbench(signs_tb)
# Enable VCD waveform dumping
with sim.write_vcd("signs.vcd", "signs.gtkw",
                   traces=[dut.i_signed_num]):
    sim.run()


if __name__ == "__main__":
    # from amaranth.cli import main
    # m = Module()
    # m.submodules.signs = dev = signs()
    # Generate the *.il file
    # main(m)
    main(signs)

    # Generate the verilog and formal test file.
    file = Path("04-Signs.v")
    elaboratable = signs()
    ports = (elaboratable.i_signed_num, elaboratable.o_cal_0, elaboratable.o_cal_1, elaboratable.o_cal_2)
    name = "signs"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)

    elaboratable, inputs = signs.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)

