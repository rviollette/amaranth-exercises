# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable, Mux
from amaranth import ClockSignal, ResetSignal
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import generate_rtlil
from util import generate_verilog


class Sync(Elaboratable):
    """Logic for my module.

    """

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
        m.submodules.counter = c = cls()

        # Formally verify that the output can never be greater than 9 and can never be 0
        m.d.comb += Assert((0 < c.counter) & (c.counter < 10))

        # Cover the case where the output is 3
        m.d.comb += Cover(c.counter == 3)

        return m, []


if __name__ == "__main__":
    file = Path("05-Sync.v")
    elaboratable = Sync()
    name = "sync"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)

    elaboratable, inputs = Sync.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)

    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 05_counter.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 05_counter.sby bmc
