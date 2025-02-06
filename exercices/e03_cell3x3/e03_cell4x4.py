from pathlib import Path
from typing import List
from typing import Tuple

from amaranth import *
from amaranth.build import Platform
from amaranth.hdl import Cover

from util import generate_rtlil
from util import generate_verilog

from e03_cell3x3 import Cell3x3

class Cell4x4(Elaboratable):

    def __init__(self):
        # Inputs
        self.module_input = Signal(16)

        # Outputs
        self.module_output = Signal(4)

    @property
    def ports(self):
        return [self.module_output]

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        c = [Cell3x3(), Cell3x3(), Cell3x3(), Cell3x3()]
        m.submodules += c

        m.d.comb += [
            # Top left
            c[0].module_input[0:3].eq(self.module_input[0:3]),
            c[0].module_input[3:6].eq(self.module_input[4:7]),
            c[0].module_input[6:9].eq(self.module_input[8:11]),

            # Top right
            c[1].module_input[0:3].eq(self.module_input[1:4]),
            c[1].module_input[3:6].eq(self.module_input[5:8]),
            c[1].module_input[6:9].eq(self.module_input[9:12]),

            # Bottom left
            c[2].module_input[0:3].eq(self.module_input[4:7]),
            c[2].module_input[3:6].eq(self.module_input[8:11]),
            c[2].module_input[6:9].eq(self.module_input[12:15]),

            # Bottom right
            c[3].module_input[0:3].eq(self.module_input[5:8]),
            c[3].module_input[3:6].eq(self.module_input[9:12]),
            c[3].module_input[6:9].eq(self.module_input[13:16]),
        ]

        # Combine outputs
        m.d.comb += [
            self.module_output[0].eq(c[0].alive_nDead),
            self.module_output[1].eq(c[1].alive_nDead),
            self.module_output[2].eq(c[2].alive_nDead),
            self.module_output[3].eq(c[3].alive_nDead),
        ]

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.nd = dut = cls()

        # Cover the case where the middle four cells don't change state, and at least one of the cells ends up alive.
        # middle four are 5,6,9,10
        # module_output[0:4] == 1


        # prove that if the outputs are all ones, and the four middle inputs are all ones, then all the other inputs must be zero.
        with m.If((dut.module_output == 0b1111) &
                  (dut.module_input[5:7] == 0b11) &
                  (dut.module_input[9:11] == 0b11)):
                  m.d.comb += Assert(dut.module_input == 0b0000011001100000)

        return m, dut.ports

if __name__ == "__main__":
    file = Path("e03_cell4x4.v")
    elaboratable = Cell4x4()
    ports = ()
    name = "cell4x4"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)

    # main()
    elaboratable, inputs = Cell4x4.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)