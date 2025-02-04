from pathlib import Path
from typing import List
from typing import Tuple

from amaranth import *
from amaranth.build import Platform
from amaranth.hdl import Cover

from util import generate_rtlil
from util import generate_verilog


class CountingCoins(Elaboratable):

    def __init__(self):
        # Inputs
        self.pennies = Signal(range(255+1))
        self.nickels = Signal(range(15+1))
        self.dimes = Signal(range(15+1))
        self.quarters = Signal(range(15+1))
        self.dollars = Signal(range(15+1))

        # Outputs
        out_val_max = 15*100 + 15*25 + 15*10 + 15*5 + 255
        self.pennies_out = Signal(range(out_val_max))

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        m.d.comb += self.pennies_out.eq(self.pennies +
                                        5 * self.nickels +
                                        10 * self.dimes +
                                        25 * self.quarters +
                                        100 * self.dollars)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        print("Formal verification for my module.")
        m = Module()
        m.submodules.to_pennies = dut = cls()

        # Cover the case where the inputs are: 37 pennies, 3 nickels, 10 dimes, 5 quarters, and 2 dollars.
        m.d.comb += Cover((dut.pennies == 37) &
                          (dut.nickels == 3) &
                          (dut.dimes == 10) &
                          (dut.quarters == 5) &
                          (dut.dollars == 2))

        return m, [dut.pennies, dut.nickels, dut.dimes, dut.quarters, dut.dollars]

if __name__ == "__main__":
    file = Path("01-ToPennies.v")
    elaboratable = CountingCoins()
    ports = (elaboratable.pennies, elaboratable.nickels, elaboratable.dimes, elaboratable.quarters,
             elaboratable.dollars, elaboratable.pennies_out)
    name = "to_pennies"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)

    # main(ToPennies)
    elaboratable, inputs = CountingCoins.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)