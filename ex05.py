# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable
from amaranth import ClockSignal, ResetSignal
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import main, generate_verilog


class MyClass(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    def __init__(self):
        # Outputs
        self.my_output = Signal(4, reset=1)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        counter = Signal(4, reset=1)

        m.d.sync += counter.eq(counter + 1)
        with m.If(counter == 0):
            m.d.sync += counter.eq(1)
        with m.If(counter > 9):
            m.d.sync += counter.eq(1)

        m.d.sync += self.my_output.eq(counter)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.my_class = my_class = cls()

        # Make sure that the output is always the same as the input
        m.d.comb += Assert((my_class.my_output >= 1) & (my_class.my_output <= 9))

        # Cover the case where the output is 3.
        m.d.comb += Cover(my_class.my_output == 3)


        # Ensure sync's clock and reset signals are manipulable.
        return m, []


if __name__ == "__main__":
    elab = MyClass()
    ports = [elab.my_output]
    generate_verilog(Path("toplevel.v"), elab, "skelet", ports=ports)
    main(MyClass)
