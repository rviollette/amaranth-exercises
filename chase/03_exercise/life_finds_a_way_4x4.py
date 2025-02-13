from queue import SimpleQueue
from pathlib import Path
from amaranth import *
from typing import List, Tuple

# from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import main
from util import generate_rtlil
from util import generate_verilog

# Call the instantiate module
from life_finds_a_way import life_finds_a_way

# Design Block
class life_finds_a_way_4x4(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    # Create the module input/output
    def __init__(self):
        # Input
        self.i_position = Signal(16)  # 16 bits,

        # Outputs
        self.o_middle_cell_status = Signal(4)  # 4 bit,0 is dead, 1 is alive

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        # Instantiate the module
        uut = [life_finds_a_way(), life_finds_a_way(), life_finds_a_way(), life_finds_a_way() ]
        m.submodules += uut

        # Internal wire connection
        m.d.comb += uut[0].i_position[0].eq(self.i_position[0])
        m.d.comb += uut[0].i_position[1].eq(self.i_position[1])
        m.d.comb += uut[0].i_position[2].eq(self.i_position[2])
        m.d.comb += uut[0].i_position[3].eq(self.i_position[4])
        m.d.comb += uut[0].i_position[4].eq(self.i_position[5])
        m.d.comb += uut[0].i_position[5].eq(self.i_position[6])
        m.d.comb += uut[0].i_position[6].eq(self.i_position[8])
        m.d.comb += uut[0].i_position[7].eq(self.i_position[9])
        m.d.comb += uut[0].i_position[8].eq(self.i_position[10])

        m.d.comb += uut[1].i_position[0].eq(self.i_position[1])
        m.d.comb += uut[1].i_position[1].eq(self.i_position[2])
        m.d.comb += uut[1].i_position[2].eq(self.i_position[3])
        m.d.comb += uut[1].i_position[3].eq(self.i_position[5])
        m.d.comb += uut[1].i_position[4].eq(self.i_position[6])
        m.d.comb += uut[1].i_position[5].eq(self.i_position[7])
        m.d.comb += uut[1].i_position[6].eq(self.i_position[9])
        m.d.comb += uut[1].i_position[7].eq(self.i_position[10])
        m.d.comb += uut[1].i_position[8].eq(self.i_position[11])

        m.d.comb += uut[2].i_position[0].eq(self.i_position[4])
        m.d.comb += uut[2].i_position[1].eq(self.i_position[5])
        m.d.comb += uut[2].i_position[2].eq(self.i_position[6])
        m.d.comb += uut[2].i_position[3].eq(self.i_position[8])
        m.d.comb += uut[2].i_position[4].eq(self.i_position[9])
        m.d.comb += uut[2].i_position[5].eq(self.i_position[10])
        m.d.comb += uut[2].i_position[6].eq(self.i_position[12])
        m.d.comb += uut[2].i_position[7].eq(self.i_position[13])
        m.d.comb += uut[2].i_position[8].eq(self.i_position[14])

        m.d.comb += uut[3].i_position[0].eq(self.i_position[5])
        m.d.comb += uut[3].i_position[1].eq(self.i_position[6])
        m.d.comb += uut[3].i_position[2].eq(self.i_position[7])
        m.d.comb += uut[3].i_position[3].eq(self.i_position[9])
        m.d.comb += uut[3].i_position[4].eq(self.i_position[10])
        m.d.comb += uut[3].i_position[5].eq(self.i_position[11])
        m.d.comb += uut[3].i_position[6].eq(self.i_position[13])
        m.d.comb += uut[3].i_position[7].eq(self.i_position[14])
        m.d.comb += uut[3].i_position[8].eq(self.i_position[15])

        # Logic is from here
        m.d.comb += [
            self.o_middle_cell_status[0].eq(uut[0].o_middle_cell_status),
            self.o_middle_cell_status[1].eq(uut[1].o_middle_cell_status),
            self.o_middle_cell_status[2].eq(uut[2].o_middle_cell_status),
            self.o_middle_cell_status[3].eq(uut[3].o_middle_cell_status),
            ]

        return m

    # Testbench Block
    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        m = Module()
        m.submodules.life_finds_a_way_4x4 = dut = cls()

        m.d.comb += Cover(
            (dut.o_middle_cell_status[0] == dut.i_position[5]) &
            (dut.o_middle_cell_status[1] == dut.i_position[6]) &
            (dut.o_middle_cell_status[2] == dut.i_position[9]) &
            (dut.o_middle_cell_status[3] == dut.i_position[10]) &
            (dut.o_middle_cell_status != 0)
        )

        with m.If((dut.o_middle_cell_status == 0b1111) &
                  (dut.i_position[5:7] == 0b11) &
                  (dut.i_position[9:11] == 0b11)):
            m.d.comb += Assert(dut.i_position == 0b0000011001100000)

        return m, [dut.i_position]


if __name__ == "__main__":
    # Generate the *.il file
    main(life_finds_a_way_4x4)

    # Generate the verilog and formal test file.
    file = Path("03-LifeFindsAWay_4x4.v")
    elaboratable = life_finds_a_way_4x4()
    ports = (elaboratable.i_position, elaboratable.o_middle_cell_status)
    name = "life_finds_a_way_4x4"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)

    elaboratable, inputs = life_finds_a_way_4x4.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)
