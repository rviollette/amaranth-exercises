from queue import SimpleQueue
from typing import List, Tuple
from pathlib import Path

from amaranth import *
from amaranth import ClockSignal, ResetSignal
# from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover
from amaranth.asserts import Initial

from amaranth.sim import Simulator

from util import main
from util import generate_rtlil
from util import generate_verilog

# There is no this library anymore
# from amaranth.lib.coding import PriorityEncoder

# Design Block
class past(Elaboratable):

    # Create the module input/output
    def __init__(self):
        # Input
        # self.i_signed_num = Signal(4)  # 64 bits,

        # Outputs
        self.o_cnt_out = Signal(4, reset=1)      # Bitwise complement (invert) it and add 1.
        # self.o_cal_1 = Signal(64)     # Arithmetically negate it.
        # self.o_cal_2 = Signal(64)     # Starting from the least significant bit, copy up to and including the first 1, then invert the remaining bits.

    def ports(self):
        return [self.o_cnt_out]


    def elaborate(self, _: Platform) -> Module:
        m = Module()

        with m.If(self.o_cnt_out == 9):
            m.d.sync += self.o_cnt_out.eq(1)
        with m.Else():
            m.d.sync += self.o_cnt_out.eq(self.o_cnt_out + 1)

        return m

    # For the formal test
    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        m = Module()
        m.submodules.cnt = cnt = cls()

        clk = ClockSignal("sync")
        rst = ResetSignal("sync")

        # Formal Assumptions
        # m.d.comb += [
        #     Assume(cnt.o_cnt_out == 1),  # Assume counter starts at 1
        #     Assume(clk == 1)  # Assume clock is toggling
        # ]

        # Make sure the clock is clocking
        # m.d.comb += Assume(clk == ~clk)

        # Include this only if you don't want to test resets
        # m.d.comb += Assume(~rst)

        # If reset is active, count must be 1 in the next cycle
        # m.d.comb += Assert(rst == 1)

        # with m.If(rst):
        # # with m.If(ResetSignal()):
        #     m.d.sync += Assert(cnt.o_cnt_out == 1)

        # If reset is NOT active and enable is high, count should increase by 1
        # with m.If(~rst):
        #     m.d.comb += Assert(cnt.o_cnt_out ==  1 )

        m.d.comb += Assert(cnt.o_cnt_out != 0)
        m.d.comb += Assert((cnt.o_cnt_out >= 1) & (cnt.o_cnt_out <= 9))

        m.d.comb += Cover(cnt.o_cnt_out == 3)

        return m, []
        # return m, []
# Testbench Block
# async def sync_tb(ctx):


if __name__ == "__main__":
    # Generate the *.il file
    main(past)

    # Generate the verilog and formal test file.
    file = Path("06-past.v")
    elaboratable = past()
    ports = (elaboratable.o_cnt_out, elaboratable.o_cnt_out)
    name = "past"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)

    elaboratable, inputs = past.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)

