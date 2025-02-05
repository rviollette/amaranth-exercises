from pathlib import Path
from typing import List
from typing import Tuple

from amaranth import *
from amaranth.build import Platform
from amaranth.hdl import Cover

from util import generate_rtlil
from util import generate_verilog


class NextDay(Elaboratable):

    def __init__(self):
        # Inputs
        self.day = Signal(range(1, 31 + 1))
        self.month = Signal(range(1, 12 + 1))
        self.year = Signal(range(1, 9999 + 1))

        # Outputs
        self.next_year = Signal(range(1, 10001))
        self.next_month = Signal.like(self.month)
        self.next_day = Signal.like(self.day)
        self.invalid = Signal()

    @property
    def ports(self):
        return [self.day, self.month, self.year, self.next_day, self.next_month, self.next_year, self.invalid]

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        m.d.comb += self.next_year.eq(self.year)
        m.d.comb += self.next_month.eq(self.month)
        m.d.comb += self.next_day.eq(self.day)

        ### Is leap year
        is_leap_year = Signal()
        m.d.comb += is_leap_year.eq(((self.year % 4) == 0) &
                                    ((self.year % 100) == 0) &
                                    ((self.year % 400) != 0))

        ### Max days in month
        max_days_in_month = Signal.like(self.day)
        with m.Switch(self.month):
            with m.Case(1,3,5,7,8,10,12): # month with 31 days
                m.d.comb += max_days_in_month.eq(31)
            with m.Case(4,6,9,11): # month with 30 days
                m.d.comb += max_days_in_month.eq(30)
            with m.Case(2): # February
                m.d.comb += max_days_in_month.eq(28 + is_leap_year)
            with m.Default():
                m.d.comb += max_days_in_month.eq(0)

        ### Invalid signal
        m.d.comb += self.invalid.eq(0)
        with m.If((self.day < 1) | (self.day > max_days_in_month) |
                  (self.month < 1) | (self.month > 12) |
                  (self.year < 1) | (self.year > 9999)):
            m.d.comb += self.invalid.eq(1)

        with m.If(self.invalid):
            m.d.comb += self.next_year.eq(0)
            m.d.comb += self.next_month.eq(0)
            m.d.comb += self.next_day.eq(0)

        ### Compute next day, month, year
        with m.If(~self.invalid):
            with m.If(self.day == max_days_in_month):  # current day is the last day of the month
                with m.If(self.month == 12):    # current month is the last month of the year
                    m.d.comb += self.next_year.eq(self.year + 1)
                    m.d.comb += self.next_month.eq(1)
                m.d.comb += self.next_day.eq(1)
            with m.Else():  # current day is not the last day of the month
                m.d.comb += self.next_day.eq(self.day + 1)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.nd = dut = cls()

        # Rule 1: An all zero numeric output always happens with invalid.
        null_output = ((dut.next_year == 0) | (dut.next_month == 0) | (dut.next_day == 0))
        m.d.comb += Assert(dut.invalid == null_output)

        # Rule 2: Either all numeric outputs are zero, or no numeric outputs are.
        m.d.comb += Assert(null_output |
                           ((dut.next_year != 0) & (dut.next_month != 0) & (dut.next_day != 0)))

        # Rule 3: The day after 31 in a valid date is always 1
        with m.If(~dut.invalid):
            with m.If(dut.day == 31):
                m.d.comb += Assert(dut.next_day == 1)

        # Rule 4: The month after 31 Dec in a valid date is always 1.
        with m.If(~dut.invalid):
            with m.If((dut.month == 12) & (dut.day == 31)):
                m.d.comb += Assert(dut.next_month == 1)

        # Rule 5: 29 Feb in an odd year is always invalid.
        with m.If((dut.day == 29) & ((dut.year % 2) == 1) & (dut.month == 2)):
            m.d.comb += Assert(dut.invalid)

        # Rule 6: What inputs can lead to an output date of 29 Feb
        m.d.comb += Cover((dut.next_day == 29) & (dut.next_month == 2))

        return m, dut.ports

if __name__ == "__main__":
    file = Path("02-next_day.v")
    elaboratable = NextDay()
    ports = ()
    name = "to_pennies"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)

    # main()
    elaboratable, inputs = NextDay.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)