from pathlib import Path
from typing import List
from typing import Tuple

from amaranth import *
from amaranth.build import Platform
from amaranth.hdl import Cover

from util import generate_rtlil
from util import generate_verilog


class Cell3x3(Elaboratable):

    def __init__(self):
        # Inputs
        self.module_input = Signal(9)

        # Outputs
        self.alive_nDead = Signal(1)

    @property
    def ports(self):
        return [self.alive_nDead]

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        neighbors = Signal.like(self.module_input)
        c = self.module_input
        m.d.comb += neighbors.eq(c[0] + c[1] + c[2] +
                                 c[3] + c[5] +
                                 c[6] + c[7] + c[8])

        m.d.comb += self.alive_nDead.eq(0)
        with m.If(c[4] == 1):
            with m.If((neighbors == 2) | (neighbors == 3)):
                m.d.comb += self.alive_nDead.eq(1)
        with m.Else():
            with m.If(neighbors == 3):
                m.d.comb += self.alive_nDead.eq(1)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.nd = dut = cls()

        sum_of_neighbors = 0
        for cell_idx in range(9):
            if cell_idx != 4:
                sum_of_neighbors += dut.module_input[cell_idx]

        with m.If(sum_of_neighbors == 3):
            m.d.comb += Assert(dut.alive_nDead == 1)
        with m.If(sum_of_neighbors == 2):
            m.d.comb += Assert(dut.alive_nDead == dut.module_input[4])

        return m, dut.ports

if __name__ == "__main__":
    file = Path("03_cell3x3.v")
    elaboratable = Cell3x3()
    ports = ()
    name = "cell3x3"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)

    # main()
    elaboratable, inputs = Cell3x3.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)