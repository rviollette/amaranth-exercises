from pathlib import Path
from typing import List
from typing import Tuple

from amaranth import *
from amaranth.build import Platform
from amaranth.hdl import Cover

from util import generate_rtlil
from util import generate_verilog


class Neg(Elaboratable):

    def __init__(self):
        # Inputs
        self.module_input = Signal(64)

        # Output
        self.module_outputA = Signal(64)
        self.module_outputB = Signal(64)
        self.module_outputC = Signal(64)

    @property
    def ports(self):
        return [self.module_outputA, self.module_outputB, self.module_outputC]

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        # Bitwise complement (invert) it and add 1.
        m.d.comb += self.module_outputA.eq(~self.module_input + 1)

        # Arithmetically negate it
        m.d.comb += self.module_outputB.eq(-self.module_input)

        # Starting from the least significant bit, copy up to and including the first 1, then invert the remaining bits.


        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.nd = dut = cls()

        m.d.comb += Assert(dut.module_outputA == dut.module_outputB)
        m.d.comb += Assert(dut.module_outputB == dut.module_outputC)

        # The most significant bit of the number being set always means it is less than 0.
       # m.d.comb += Assert()

        return m, dut.ports

if __name__ == "__main__":
    file = Path("e04_negate.v")
    elaboratable = Neg()
    ports = ()
    name = "neg"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)

    # main()
    elaboratable, inputs = Neg.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)