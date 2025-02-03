# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from pathlib import Path
from typing import List, Tuple

from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import generate_rtlil
from util import generate_verilog


class ToPennies(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    def __init__(self):
        # Inputs
        self.pennies = Signal(range(255+1))
        self.nickels = Signal(range(15+1))
        self.dimes = Signal(range(15+1))
        self.quarters = Signal(range(15+1))
        self.dollars = Signal(range(15+1))

        # Outputs
        out_val_max = 255 + 5*15 + 10*15 + 25*15 + 100*15
        self.pennies_sum = Signal(range(out_val_max + 1))

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        nickels_to_pennies = 5 * self.nickels
        dimes_to_pennies = 10 * self.dimes
        quarters_to_pennies = 25 * self.quarters
        dollars_to_pennies = 100 * self.dollars

        m.d.comb += self.pennies_sum.eq(self.pennies +
                                        nickels_to_pennies +
                                        dimes_to_pennies +
                                        quarters_to_pennies +
                                        dollars_to_pennies)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for ToPennies module."""
        m = Module()
        m.submodules.to_pennies = dut = cls()

        # Cover the case where the inputs are: 37 pennies, 3 nickels, 10 dimes, 5 quarters, and 2 dollars.
        m.d.comb += Cover((dut.pennies == 37) &
                          (dut.nickels == 3) &
                          (dut.dimes == 10) &
                          (dut.quarters == 5) &
                          (dut.dollars == 2))

        # Cover the case where the output is 548 pennies.
        m.d.comb += Cover(dut.pennies_sum == 548)

        # Cover the case where the output is 64 pennies, and there are twice as many nickels as there are dimes,
        # and there is at least one dime.
        m.d.comb += Cover((dut.pennies_sum == 64) &
                          (dut.nickels == (2 * dut.dimes)) &
                          (dut.dimes > 0))

        # Prove that if there are no input pennies, then the number of output pennies is always a multiple of 5.
        with m.If(dut.pennies == 0):
            m.d.comb += Assert((dut.pennies_sum % 5) == 0)

        # Prove that the number of output pennies, modulo 5, will always equal the number of input pennies, modulo 5,
        # regardless of the other inputs.
        m.d.comb += Assert((dut.pennies_sum % 5) == (dut.pennies % 5))

        return m, [dut.pennies, dut.nickels, dut.dimes, dut.quarters, dut.dollars]


if __name__ == "__main__":

    file = Path("01-ToPennies.v")
    elaboratable = ToPennies()
    ports = (elaboratable.pennies, elaboratable.nickels, elaboratable.dimes, elaboratable.quarters,
             elaboratable.dollars, elaboratable.pennies_sum)
    name = "to_pennies"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)



    # main(ToPennies)
    elaboratable, inputs = ToPennies.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)


    # in Bash, in folder amaranth-exercises/lila :
    #   source ~/Downloads/oss-cad-suite/oss-cad-suite-linux-x64-20241104/oss-cad-suite/environment

    # Run the formal verification engine for covers
    #   amaranth-exercises/lila$ sby -f 01_to_pennies.sby

    # Run the formal verification engine for bounded model checking
    #   amaranth-exercises/lila$ sby -f 01_to_pennies.sby bmc
