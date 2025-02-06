# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import ClockDomain
from amaranth import Signal, Module, Elaboratable, Mux
from amaranth import ClockSignal, ResetSignal
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover
from amaranth.asserts import Initial

from util import generate_rtlil
from util import generate_verilog


class Past(Elaboratable):
    """Logic for my module."""

    def __init__(self):
        # Inputs

        # Outputs
        self.counter = Signal(range(1, 9 + 1), init=1)

    @property
    def ports(self):
        return [self.counter]

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()
        m.d.sync += self.counter.eq(Mux(self.counter == 9, 1, self.counter + 1))
        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""

        m = Module()

        # Define test clock & reset domain
        m.domains.sync = cd_sync = ClockDomain()
        # Assume reset is always cleared
        m.d.comb += Assume(~cd_sync.rst)
        # Make sure the clock is clocking
        clk_past = Signal()
        m.d.sync += clk_past.eq(cd_sync.clk)
        m.d.comb += Assume(cd_sync.clk == ~clk_past)


        m.submodules.counter = c = cls()

        # Formally verify that the output can never be greater than 9 and can never be 0
        m.d.comb += Assert((0 < c.counter) & (c.counter < 10))

        # Cover the case where the output is 3
        m.d.comb += Cover(c.counter == 3)

        # Verify each positive edge of the clock increments the counter by one, and that the counter goes from 9 back to 1.
        counter_past = Signal.like(c.counter, init=0)
        m.d.sync += counter_past.eq(c.counter)
        with m.If(~Initial() & cd_sync.clk):
            with m.If(counter_past == 9):
                m.d.comb += Assert(c.counter == 1)
            with m.Else():
                m.d.comb += Assert(c.counter == (counter_past + 1))
        return m, [cd_sync.rst, cd_sync.clk, c.counter]


if __name__ == "__main__":
    file = Path("06-Past.v")
    elaboratable = Past()
    name = "past"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)

    elaboratable, inputs = Past.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)

    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 06_past.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 06_past.sby bmc
