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
        self.year = Signal(range(1,9999))
        self.month = Signal(range(1,12))
        self.day = Signal(range(1,31))

        # Outputs
        self.next_day = Signal(range(1,31))
        self.next_month = Signal(range(1,12))
        self.next_year = Signal(range(1,9999))

        self.invalid = Signal()

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        last_day = Signal.like(self.day)
        is_bissextile = Signal()

        m.d.comb += self.invalid.eq(0)

        # Leap year
        with m.If(self.year % 4 == 0):
            # Still leap year
            with m.If(self.year % 100 == 0):
                # Not leap year
                with m.If(self.year % 400):
                    m.d.comb += is_bissextile.eq(1)
                with m.Else():
                    m.d.comb += is_bissextile.eq(0)
        with m.Else():
            m.d.comb += is_bissextile.eq(0)

        # Last day eval
        with m.Switch(self.month):
            with m.Case(1, 3, 5, 7, 8, 10, 12):
                m.d.comb += last_day.eq(31)
            with m.Case(4, 6, 9, 11):
                m.d.comb += last_day.eq(30)
            with m.Case(2):
                with m.If(is_bissextile):
                    m.d.comb += last_day.eq(29)
                with m.Else():
                    m.d.comb += last_day.eq(28)

        with m.If(self.day == last_day):
            m.d.comb += self.next_day.eq(1)
        with m.Else():
            m.d.comb += self.next_day.eq(self.day + 1)

        with m.If(self.month == 12):
            m.d.comb += self.next_month.eq(1)
        with m.Else():
            m.d.comb += self.next_month.eq(self.month + 1)

        with m.If(self.year == 9999):
            m.d.comb += self.next_year.eq(1)
        with m.Else():
            m.d.comb += self.next_year.eq(self.year + 1)

        with m.If((self.year < 1) | (self.year > 9999) |
                  (self.month < 1) | (self.month > 12) |
                  (self.day < 1) | (self.day > last_day)):
            m.d.comb += self.invalid.eq(1)

        with m.If(self.invalid == 1):
            m.d.comb += self.next_month.eq(0)
            m.d.comb += self.next_year.eq(0)
            m.d.comb += self.next_day.eq(0)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.my_class = my_class = cls()

        # Make sure that the output is always the same as the input
        m.d.comb += Cover((my_class.day == 0) &
                           (my_class.month == 0) &
                           (my_class.year == 0) &
                           (my_class.invalid == 1)
                           )

        # Cover the case where the output is 1.
        m.d.comb += Cover((my_class.next_day == 0) &
                          (my_class.next_month == 0) &
                          (my_class.next_year == 0)
                          )

        m.d.comb += Cover((my_class.day == 31) &
                          (my_class.next_day == 1) &
                          (my_class.invalid == 0))

        m.d.comb += Cover((my_class.day == 31) &
                          (my_class.month == 12) &
                          (my_class.next_month == 1)
                          )


        m.d.comb += Cover((my_class.day == 29) &
                          (my_class.month == 2) &
                          (my_class.invalid == 1)
                          )

        return m, [my_class.day, my_class.month, my_class.year]


if __name__ == "__main__":
    main(MyClass)
