# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable, Mux
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import generate_rtlil
from util import generate_verilog

from amaranth.cli import main


class NextDay(Elaboratable):
    """Logic for NextDay module."""

    def __init__(self):
        # Inputs
        self.day = Signal(range(1, 31 + 1))
        self.month = Signal(range(1, 12 + 1))
        self.year = Signal(range(1, 9999 + 1))

        # Outputs
        self.next_day = Signal.like(self.day)
        self.next_month = Signal.like(self.month)
        self.next_year = Signal.like(self.year)
        self.invalid = Signal(1)

        # Internal signals
        self.leap_year = Signal(1)
        self.day_in_month = Signal.like(self.day)

    @property
    def ports(self):
        return [self.day, self.month, self.year, self.next_day, self.next_month, self.next_year, self.invalid]


    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for NextDay module."""
        m = Module()

        m.d.comb += self.leap_year.eq(((self.year % 4) == 0) &  # year is divisible by 4
                                      ((self.year % 100) != 0))  # year is not divisible by 100

        with m.Switch(self.month):
            with m.Case(1, 3, 5, 7, 8, 10, 12):  # month with 31 days
                m.d.comb += self.day_in_month.eq(31)
            with m.Case(4, 6, 9, 11):  # month with 30 days
                m.d.comb += self.day_in_month.eq(30)
            with m.Case(2):  # February
                m.d.comb += self.day_in_month.eq(Mux(self.leap_year, 29, 28))
            with m.Default():  # invalid month implies invalid day
                m.d.comb += self.day_in_month.eq(0)

        m.d.comb += self.invalid.eq((self.day == 0) | (self.day > self.day_in_month) |
                                    (self.month == 0) | (self.month > 12) |
                                    (self.year == 0) | (self.year > 9999))

        # default outputs values
        m.d.comb += [
            self.next_day.eq(0),
            self.next_month.eq(0),
            self.next_year.eq(0),
        ]
        with m.If(~self.invalid):
            with m.If(self.day == self.day_in_month):  # last day of the month
                m.d.comb += [
                    self.next_day.eq(1),
                    self.next_month.eq(Mux(self.month == 12, 1, self.month + 1)),
                    self.next_year.eq(Mux(self.month == 12, self.year + 1, self.year)),
                ]
            with m.Else():
                m.d.comb += [
                    self.next_day.eq(self.day +1),
                    self.next_month.eq(self.month),
                    self.next_year.eq(self.year),
                ]

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for NextDay module."""
        m = Module()
        m.submodules.next_day = dut = cls()

        null_output = ((dut.next_year == 0) | (dut.next_month == 0) | (dut.next_day == 0))

        # Prove an all zero numeric output always happens with invalid.
        m.d.comb += Assert(dut.invalid == null_output)

        # Either all numeric outputs are zero, or no numeric outputs are.
        m.d.comb += Assert(null_output |
                           ((dut.next_year != 0) & (dut.next_month != 0) & (dut.next_day != 0)))

        with m.If(~dut.invalid):
            # The day after 31 in a valid date is always 1.
            with m.If(dut.day == 31):
                m.d.comb += Assert(dut.next_day == 1)

            # The month after 31 Dec in a valid date is always 1.
            with m.If((dut.day == 31) & (dut.month == 12)):
                m.d.comb += Assert(dut.next_month == 1)

        # 29 Feb in an odd year is always invalid.
        with m.If((dut.day == 29) & (dut.month == 2) & (dut.year & 1)):
            m.d.comb += Assert(dut.invalid)

        # What inputs can lead to an output date of 29 Feb?
        m.d.comb += Cover((dut.next_month == 2) & (dut.next_day == 29))

        return m, dut.ports


if __name__ == "__main__":

    file = Path("02-NextDay.v")
    elaboratable = NextDay()
    name = "next_day"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=elaboratable.ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=elaboratable.ports)



    # main(NextDay)
    elaboratable, inputs = NextDay.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)


    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 02_next_day.sby cover

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 02_next_day.sby bmc
