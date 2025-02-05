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
        self.live_neighbors_2_3 = Signal(range(4))

    @property
    def ports(self):
        return [self.cells, self.live_neighbors_2_3, self.alive]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for Parts1 module."""
        m = Module()

        with m.Switch(Cat(self.cells[:4], self.cells[-4:])):
            for i in range(1 << 8):
                alive_neighbors = bin(i).count('1')
                if alive_neighbors in (2, 3):
                    with m.Case(i):
                        m.d.comb += self.live_neighbors_2_3.eq(Const(alive_neighbors))  # value can be only 2 or 3
            with m.Default():
                m.d.comb += self.live_neighbors_2_3.eq(Const(0))

        with m.If(self.cells[4]):
            m.d.comb += self.alive.eq((self.live_neighbors_2_3 == 2) | (self.live_neighbors_2_3 == 3))
        with m.Else():
            m.d.comb += self.alive.eq(self.live_neighbors_2_3 == 3)


        return m


class Parts2(Elaboratable):
    """Logic for Parts2 module."""

    def __init__(self):
        # Inputs
        self.cells = Signal(16)

        # Outputs
        self.alive = Signal(4)

        # Internal signals
        self.cell3x3 = [Parts1(), Parts1(), Parts1(), Parts1()]

    @property
    def ports(self):
        return [self.cells, self.alive]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for Parts2 module."""
        m = Module()

        c = self.cell3x3
        m.submodules += c

        # Inputs
        m.d.comb += [
            # top left
            c[0].cells[0:3].eq(self.cells[0:3]),
            c[0].cells[3:6].eq(self.cells[4:7]),
            c[0].cells[6:9].eq(self.cells[8:11]),

            # top right
            c[1].cells[0:3].eq(self.cells[1:4]),
            c[1].cells[3:6].eq(self.cells[5:8]),
            c[1].cells[6:9].eq(self.cells[9:12]),

            # bottom left
            c[2].cells[0:3].eq(self.cells[4:7]),
            c[2].cells[3:6].eq(self.cells[8:11]),
            c[2].cells[6:9].eq(self.cells[12:15]),

            # bottom right
            c[3].cells[0:3].eq(self.cells[5:8]),
            c[3].cells[3:6].eq(self.cells[9:12]),
            c[3].cells[6:9].eq(self.cells[13:16]),
        ]

        # Outputs
        m.d.comb += [
            self.alive.eq(Cat(c[0].alive, c[1].alive, c[2].alive, c[3].alive))
        ]
        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for Parts2 module."""
        m = Module()
        m.submodules.parts2 = dut = cls()

        neighbors = Cat(dut.cells[i]
                        for i in range(16)
                        if i not in (5, 6, 9, 10))
        center = Cat(dut.cells[5:7], dut.cells[9:11])

        m.d.comb += Cover((dut.alive == center) & (dut.alive > 0))

        with m.If((dut.alive.all()) & center.all()):
            m.d.comb += Assert(neighbors == 0)

        return m, dut.ports


if __name__ == "__main__":

    file = Path("03-Parts2.v")
    elaboratable = Parts2()
    name = "parts2"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)



    # main(Parts2)
    elaboratable, inputs = Parts2.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)


    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 03_cell4x4.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 03_cell4x4.sby bmc
