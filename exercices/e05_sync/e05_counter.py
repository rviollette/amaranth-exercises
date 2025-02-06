from pathlib import Path
from typing import List
from typing import Tuple

from amaranth import *
from amaranth.build import Platform
from amaranth.hdl import Cover

from util import generate_rtlil
from util import generate_verilog

class Counter(Elaboratable):

    def __init__(self):
        # Inputs
        #self.module_input = Signal(16)

        # Outputs
        self.count_output = Signal(4, reset=1)

    @property
    def ports(self):
        return [self.count_output]

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        with m.If(self.count_output == 9):
            m.d.sync += self.count_output.eq(1)
        with m.Else():
            m.d.sync += self.count_output.eq(self.count_output + 1)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.c = dut = cls()

        # Count can never be greater than 9 and can never be 0
        m.d.comb += Assert((dut.count_output > 0) & (dut.count_output < 10))

        # Cover the case where output is 3
        m.d.comb += Cover(dut.count_output == 3)

        return m, dut.ports

if __name__ == "__main__":
    file = Path("e05_counter.v")
    elaboratable = Counter()
    ports = ()
    name = "counter"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)

    # main()
    elaboratable, inputs = Counter.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)