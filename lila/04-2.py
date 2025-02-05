# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable, Mux, Cat, Const, signed, unsigned
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import generate_rtlil
from util import generate_verilog




class UnsignedComparator(Elaboratable):
    """Logic for UnsignedComparator module."""

    def __init__(self):
        # Inputs
        self.a = Signal(unsigned(16))
        self.b = Signal.like(self.a)

        # Outputs:
        self.lt = Signal(1)  # Set if a less than b

    @property
    def ports(self):
        return [self.a, self.b, self.lt]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for UnsignedComparator module."""
        m = Module()
        m.d.comb += self.lt.eq(self.a < self.b)
        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for UnsignedComparator module."""
        m = Module()
        m.submodules.SignedComparator = dut = cls()

        return m, dut.ports


class SignedComparator(Elaboratable):
    """Logic for SignedComparator module."""

    def __init__(self):
        # Inputs
        self.a = Signal(unsigned(16))
        self.b = Signal.like(self.a)

        # Outputs
        self.lt = Signal(1)  # Set if a < b

        self.unsigned_cmp = UnsignedComparator()

    @property
    def ports(self):
        return [self.a, self.b, self.lt]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for SignedComparator module."""
        m = Module()

        ucmp = self.unsigned_cmp
        m.submodules += ucmp

        m.d.comb += [
            ucmp.a.eq(self.a),
            ucmp.b.eq(self.b),
        ]

        with m.Switch(Cat(self.a[-1], self.b[-1])):
            with m.Case(0b00): # a and b positive
                m.d.comb += self.lt.eq(ucmp.lt)
            with m.Case(0b01): # a negative and b positive
                m.d.comb += self.lt.eq(1)
            with m.Case(0b10): # a positive and b negative
                m.d.comb += self.lt.eq(0)
            with m.Case(0b11): # a and b negative
                m.d.comb += self.lt.eq(ucmp.lt)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for SignedComparator module."""
        m = Module()
        m.submodules.scmp = dut = cls()

        m.d.comb += Assert(dut.lt == (dut.a.as_signed() < dut.b.as_signed()))


        return m, dut.ports

if __name__ == "__main__":

    file = Path("04-SignedComparator.v")
    elaboratable = SignedComparator()
    name = "SignedComparator"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)



    # main(SignedComparator)
    elaboratable, inputs = SignedComparator.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)


    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 04_negate.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 04_negate.sby bmc
