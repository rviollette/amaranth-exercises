# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable, Mux, Cat, Const
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import generate_rtlil
from util import generate_verilog


class Parts1(Elaboratable):
    """Logic for Parts1 module."""

    def __init__(self):
        # Inputs
        self.cells = Signal(9)

        # Outputs
        self.alive = Signal(1)

        # Internal signals
        self.live_neighbors = Signal(range(9))

    @property
    def ports(self):
        return [self.cells, self.live_neighbors, self.alive]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for Parts1 module."""
        m = Module()

        low = self.cells[:4]
        high = self.cells[-4:]
        # with m.Switch(Cat(low, high)):
        #     for i in range(1 << 8):
        #         with m.Case(i):
        #             alive_neighbors = bin(i).count('1')
        #             m.d.comb += self.live_neighbors.eq(Const(alive_neighbors))
        #     with m.Default():
        #         m.d.comb += self.live_neighbors.eq(Const(0))
        with m.Switch(Cat(low, high)):
            for i in range(1 << 8):
                alive_neighbors = bin(i).count('1')
                if alive_neighbors in (2, 3):
                    with m.Case(i):
                        m.d.comb += self.live_neighbors.eq(Const(alive_neighbors))
            with m.Default():
                m.d.comb += self.live_neighbors.eq(Const(0))

        with m.If(self.cells[4]):
            m.d.comb += self.alive.eq((self.live_neighbors == 2) | (self.live_neighbors == 3))
        with m.Else():
            m.d.comb += self.alive.eq(self.live_neighbors == 3)


        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for Parts1 module."""
        m = Module()
        m.submodules.parts1 = dut = cls()

        s = 0
        for i in range(9):
            if i == 4:
                continue
            s += dut.cells[i]

        with m.If(s == 3):
            m.d.comb += Assert(dut.alive)

        with m.If(s == 2):
            m.d.comb += Assert(dut.alive == dut.cells[4])


        return m, dut.ports


if __name__ == "__main__":

    file = Path("03-Parts1.v")
    elaboratable = Parts1()
    name = "parts1"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)



    # main(Parts1)
    elaboratable, inputs = Parts1.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)


    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 03_cell4x4.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 03_cell4x4.sby bmc
