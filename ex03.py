# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple
from pathlib import Path

from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import main, generate_verilog


class MyClass3(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    def __init__(self):
        # Inputs
        self.input = Signal(9)

        # Outputs
        self.output = Signal(1)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        # middle_neighbours = [1, 3, 5, 7] # So every odd one basically
        num_of_neighbour_alive_cells = Signal(3)

        m.d.comb += num_of_neighbour_alive_cells.eq(sum(self.input) - self.input[4])

        with m.Switch(num_of_neighbour_alive_cells):
            with m.Case(2):
                with m.If(self.input[4]):
                    m.d.comb += self.output.eq(1)
                with m.Else():
                    m.d.comb += self.output.eq(0)
            with m.Case(3):
                m.d.comb += self.output.eq(1)
            with m.Default():
                m.d.comb += self.output.eq(0)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.my_class = my_class = cls()

        # Check state stays the same for two alive neighbours case is alive as start
        m.d.comb += Cover((sum(my_class.input) == 2) &
                           (my_class.output == my_class.input[4]))

        # Check state become alive if dead at first
        m.d.comb += Cover((sum(my_class.input) == 3) &
                           (my_class.output == 1) &
                           (my_class.input[4] == 0))

        return m, [my_class.input]


if __name__ == "__main__":
    elab = MyClass3()
    ports = (elab.input, elab.output)
    generate_verilog(Path("toplevel.v"), elab, "skelet", ports=ports)

    main(MyClass3)
