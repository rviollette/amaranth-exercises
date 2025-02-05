# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple
from pathlib import Path

from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import main, generate_verilog
from ex03 import MyClass3


class MyClass4(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    def __init__(self):
        # Inputs
        self.input = Signal(16)

        # Outputs
        self.output = Signal(4)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()
        m.submodules.s1 = MyClass3()
        m.submodules.s2 = MyClass3()
        m.submodules.s3 = MyClass3()
        m.submodules.s4 = MyClass3()

        m.d.comb += m.submodules.s1.input[0].eq(self.input[0])
        m.d.comb += m.submodules.s1.input[1].eq(self.input[1])
        m.d.comb += m.submodules.s1.input[2].eq(self.input[2])
        m.d.comb += m.submodules.s1.input[3].eq(self.input[4])
        m.d.comb += m.submodules.s1.input[4].eq(self.input[5])
        m.d.comb += m.submodules.s1.input[5].eq(self.input[6])
        m.d.comb += m.submodules.s1.input[6].eq(self.input[8])
        m.d.comb += m.submodules.s1.input[7].eq(self.input[9])
        m.d.comb += m.submodules.s1.input[8].eq(self.input[10])

        m.d.comb += m.submodules.s2.input[0].eq(self.input[1])
        m.d.comb += m.submodules.s2.input[1].eq(self.input[2])
        m.d.comb += m.submodules.s2.input[2].eq(self.input[3])
        m.d.comb += m.submodules.s2.input[3].eq(self.input[5])
        m.d.comb += m.submodules.s2.input[4].eq(self.input[6])
        m.d.comb += m.submodules.s2.input[5].eq(self.input[7])
        m.d.comb += m.submodules.s2.input[6].eq(self.input[9])
        m.d.comb += m.submodules.s2.input[7].eq(self.input[10])
        m.d.comb += m.submodules.s2.input[8].eq(self.input[11])

        m.d.comb += m.submodules.s3.input[0].eq(self.input[4])
        m.d.comb += m.submodules.s3.input[1].eq(self.input[5])
        m.d.comb += m.submodules.s3.input[2].eq(self.input[6])
        m.d.comb += m.submodules.s3.input[3].eq(self.input[8])
        m.d.comb += m.submodules.s3.input[4].eq(self.input[9])
        m.d.comb += m.submodules.s3.input[5].eq(self.input[10])
        m.d.comb += m.submodules.s3.input[6].eq(self.input[12])
        m.d.comb += m.submodules.s3.input[7].eq(self.input[13])
        m.d.comb += m.submodules.s3.input[8].eq(self.input[14])

        m.d.comb += m.submodules.s4.input[0].eq(self.input[5])
        m.d.comb += m.submodules.s4.input[1].eq(self.input[6])
        m.d.comb += m.submodules.s4.input[2].eq(self.input[7])
        m.d.comb += m.submodules.s4.input[3].eq(self.input[9])
        m.d.comb += m.submodules.s4.input[4].eq(self.input[10])
        m.d.comb += m.submodules.s4.input[5].eq(self.input[11])
        m.d.comb += m.submodules.s4.input[6].eq(self.input[13])
        m.d.comb += m.submodules.s4.input[7].eq(self.input[14])
        m.d.comb += m.submodules.s4.input[8].eq(self.input[15])

        m.d.comb += self.output[0].eq(m.submodules.s1.output)
        m.d.comb += self.output[1].eq(m.submodules.s2.output)
        m.d.comb += self.output[2].eq(m.submodules.s3.output)
        m.d.comb += self.output[3].eq(m.submodules.s4.output)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.my_class = my_class = cls()

        m.d.comb += Assert((my_class.output[0] == my_class.input[5]) &
                           (my_class.output[1] == my_class.input[6]) &
                           (my_class.output[2] == my_class.input[0]) &
                           (my_class.output[3] == my_class.input[10]) &
                           (my_class.output != 0)
                           )

        m.d.comb += Assert((my_class.output ==  0b1111) &
                           (my_class.input[5] == 1) &
                           (my_class.input[6] == 1) &
                           (my_class.input[9] == 1) &
                           (my_class.input[10] == 1) &
                           (my_class.input == 0b0000011001100000)
                           )

        return m, [my_class.input]


if __name__ == "__main__":
    elab = MyClass4()
    ports = (elab.input, elab.output)
    generate_verilog(Path("toplevel.v"), elab, "skelet", ports=ports)

    main(MyClass4)
