# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import main


class MyClass(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    def __init__(self):
        # Inputs
        self.pennies = Signal(8)
        self.nickels = Signal(4)
        self.dimes = Signal(4)
        self.quarters = Signal(4)
        self.dollars = Signal(4)

        # Outputs
        self.pennies_out = Signal(12)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        m.d.comb += self.pennies_out.eq(self.pennies +
                                        self.nickels * 5 +
                                        self.dimes * 10 +
                                        self.quarters * 25 +
                                        self.dollars * 100)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.my_class = my_class = cls()

        # Make sure that the output is always the same as the input
        m.d.comb += Assert(my_class.pennies_out == (my_class.pennies +
                                                    my_class.nickels * 5 +
                                                    my_class.dimes * 10 +
                                                    my_class.quarters * 25 +
                                                    my_class.dollars * 100))

        # Cover the case where the input are 
        m.d.comb += Cover((my_class.pennies == 37) &
                          (my_class.nickels == 3 ) &
                          (my_class.dimes   == 10) &
                          (my_class.quarters == 5) &
                          (my_class.dollars == 2))

        m.d.comb += Cover((my_class.pennies_out == 64) &
                          (my_class.nickels == my_class.dimes * 2) &
                          (my_class.dimes >= 1))

        m.d.comb += Cover((my_class.pennies == 0) &
                          (my_class.pennies_out % 5 == 0))

        m.d.comb += Cover((my_class.pennies_out % 5 == my_class.pennies % 5))

        # Cover the case where the output is 548.
        m.d.comb += Cover(my_class.pennies_out == 548)

        return m, [my_class.pennies, my_class.nickels, my_class.dimes, my_class.quarters, my_class.dollars]


if __name__ == "__main__":
    main(MyClass)
