# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable, Mux, Cat, Const, signed
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import generate_rtlil
from util import generate_verilog




class Signs(Elaboratable):
    """Logic for Signs module."""

    def __init__(self):
        # Inputs
        self.input = Signal(signed(64))

        # Outputs
        self.out0 = Signal.like(self.input)
        self.out1 = Signal.like(self.input)
        self.out2 = Signal.like(self.input)

    @property
    def ports(self):
        return [self.input, self.out0, self.out1, self.out2]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for Signs module."""
        m = Module()
        m.d.comb += self.out0.eq((~self.input) + 1)
        m.d.comb += self.out1.eq(-self.input)

        # Option 1: If/Else
        with m.If(self.input == 0):
            m.d.comb += self.out2.eq(0)
        for i in range(len(self.input)):
            with m.Elif(self.input[i]):
                m.d.comb += self.out2.eq(Cat(self.input[:i+1], ~self.input[i+1:]))

        # Option 2: Switch with pattern
        # with m.Switch(self.input):
        #     for i in range(len(self.input)):
        #         pattern = ''.join('1' if j == i else '-'
        #                           for j in reversed(range(len(self.input))))
        #         with m.Case(pattern):
        #             m.d.comb += self.out2.eq(Cat(self.input[:i+1], ~self.input[i+1:]))
        #     with m.Default():
        #         m.d.comb += self.out2.eq(0)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for Signs module."""
        m = Module()
        m.submodules.signs = dut = cls()

        m.d.comb += [
            Assert(dut.out0 == dut.out1),
            Assert(dut.out1 == dut.out2),
            Assert(dut.input[-1] == (dut.input < 0)),
        ]


        return m, dut.ports


if __name__ == "__main__":

    file = Path("04-Signs.v")
    elaboratable = Signs()
    name = "signs"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)



    # main(Signs)
    elaboratable, inputs = Signs.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)


    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 04_negate.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 04_negate.sby bmc
