from email.encoders import encode_quopri
from pathlib import Path

from amaranth import *
from amaranth.sim import Simulator
from amaranth.build import Platform
# from util import generate_verilog, generate_rtlil

from typing import List, Tuple
from amaranth.hdl import Assume, Assert, Cover

from util import main


# Design Block
class the_day_after(Elaboratable):
    # Create the module input/output
    def __init__(self):
        # Inputs
        self.i_day      = Signal(5)     # from 1 to 31
        self.i_month    = Signal(4)     # from 1 to 12
        self.i_year     = Signal(14)    # from 1 to 9999

        # Outputs
        self.o_nxt_day      = Signal(5)
        self.o_nxt_month    = Signal(4)
        self.o_nxt_year     = Signal(14)
        self.o_invalid      = Signal(1)

    def ports(self):
        return [self.i_day, self.i_month, self.i_year,
                self.o_nxt_day, self.o_nxt_month, self.o_nxt_year, self.o_invalid]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        # Internal wire (not an input/output port)
        the_max_day = Signal(5)

        # Check the max day based on the month
        # If the day is not max, then add 1 day for next day, otherwise the next date will become 1st
        with m.Switch(self.i_month):
            with m.Case(1, 3, 5, 7, 8, 10, 12):
                m.d.comb += the_max_day.eq(31)
                m.d.comb += self.o_nxt_day.eq(Mux(self.i_day % 31 != 0, self.i_day + 1, 1))

            with m.Case(4, 6, 9, 11):
                m.d.comb += the_max_day.eq(30)
                m.d.comb += self.o_nxt_day.eq(Mux(self.i_day % 30 != 0, self.i_day + 1, 1))

            with m.Case(2):
                with m.If((self.i_year % 4 == 0) | (self.i_year % 100 == 0) | (self.i_year % 400 == 0) ):
                    m.d.comb += the_max_day.eq(29)
                    m.d.comb += self.o_nxt_day.eq(Mux(self.i_day % 29 != 0, self.i_day + 1, 1))
                with m.Else():
                    m.d.comb += the_max_day.eq(28)
                    m.d.comb += self.o_nxt_day.eq(Mux(self.i_day % 28 != 0, self.i_day + 1, 1))

            with m.Default():
                m.d.comb += the_max_day.eq(31)
                m.d.comb += self.o_nxt_day.eq(Mux(self.i_day % 31 != 0, self.i_day + 1, 1))

        # Set the next month
        with m.Switch(self.i_day == the_max_day):
            with m.Case(0):
                m.d.comb += self.o_nxt_month.eq(self.i_month)
            with m.Case(1):
                m.d.comb += self.o_nxt_month.eq(Mux((self.i_month == 12), 1, self.i_month + 1))

        # Set the next year
        # Only 31st Dec to add 1 for next year.
        m.d.comb += self.o_nxt_year.eq( Mux(( (self.i_month == 12) & (self.i_day == 31) ),self.i_year + 1, self.i_year) )

        m.d.comb += [
            self.o_invalid.eq(
                (self.i_day < 1) | (self.i_day > the_max_day) |
                (self.i_month < 1) | (self.i_month > 12) |
                (self.i_year < 1) | (self.i_year > 9999)
            )
        ]

        with m.If(self.o_invalid):
            m.d.comb += self.o_nxt_year.eq(0)
            m.d.comb += self.o_nxt_month.eq(0)
            m.d.comb += self.o_nxt_day.eq(0)


        return m

# Testbench Block
    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        m = Module()
        m.submodules.nxt_day = nxt_day = cls()

        # Cover the case where the output is 1.
        # m.d.comb += Cover(nxt_day.o_invalid == 1)

        is_zero = ((nxt_day.o_nxt_year == 0) &
                   (nxt_day.o_nxt_month == 0) &
                   (nxt_day.o_nxt_day == 0))
        m.d.comb += Assert(nxt_day.o_invalid == is_zero)

        all_nonzero = ((nxt_day.o_nxt_year != 0) &
                       (nxt_day.o_nxt_month != 0) &
                       (nxt_day.o_nxt_day != 0))

        m.d.comb += Assert(all_nonzero | is_zero)

        with m.If(~nxt_day.o_invalid):
            with m.If(nxt_day.i_day == 31):
                m.d.comb += Assert(nxt_day.o_nxt_day == 1)
            with m.If((nxt_day.i_month == 12) & (nxt_day.i_day == 31)):
                m.d.comb += Assert(nxt_day.o_nxt_month == 1)

        with m.If(((nxt_day.i_year % 2) == 1) & (nxt_day.i_month == 2) & (nxt_day.i_day == 29)):
            m.d.comb += Assert(nxt_day.o_invalid)

        m.d.comb += Cover((nxt_day.o_nxt_month == 2) & (nxt_day.o_nxt_day == 29))

        return m, [nxt_day.i_day, nxt_day.i_month, nxt_day.i_year]


if __name__ == "__main__":
    main(the_day_after)