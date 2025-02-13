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
class sync(Elaboratable):

    # Create the module input/output
    def __init__(self):
        # Input
        self.i_signed_num = Signal(4)  # 64 bits,

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
        m.submodules.sync = sync = cls()

        m.d.comb += Assert(sync.o_cnt_out != 0)
        m.d.comb += Assert((sync.o_cnt_out >= 1) & (sync.o_cnt_out <= 9))

        m.d.comb += Cover(sync.o_cnt_out == 3)

        return m, []

# Testbench Block
# async def sync_tb(ctx):


if __name__ == "__main__":
    # Generate the *.il file
    main(sync)

    # Generate the verilog and formal test file.
    file = Path("05-Synchronicity.v")
    elaboratable = sync()
    ports = (elaboratable.o_cnt_out, elaboratable.o_cnt_out)
    name = "sync"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)

    elaboratable, inputs = sync.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)

