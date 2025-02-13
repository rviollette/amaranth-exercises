from queue import SimpleQueue
from pathlib import Path
from amaranth import *
from typing import List, Tuple

#from amaranth import Signal, Module, Elaboratable
from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

from util import main
from util import generate_rtlil
from util import generate_verilog

# Design Block
class life_finds_a_way(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """
    # Create the module input/output
    def __init__(self):
        # Input
        self.i_position = Signal(9)  # 9 bits,

        # Outputs
        self.o_middle_cell_status = Signal(1)  # 1 bit, 0 is dead, 1 is alive

    def elaborate(self, _: Platform) -> Module:
        m = Module()

        # Internal wire
        w_position          = Signal(9)
        w_live_dead_status  = Signal(1)

        # Logic is from here
        """ TO DO
        1. Check the middle of the cell status is live or dead
        2. Process the dead cell status first. Using the case statement.
            a. If there are 3 live neighbors, it stays alive. Otherwise, it stays dead. ( != 3 )
            
        3. Then process the live cell
            a. If there are 2 or 3 live neighbors, it stays alive. Otherwise it stays dead.
        
        4. Output the status of the middle cell.
        
        """
        w_position_1 = Signal(1)
        w_alive_sum  = Signal(4)

        m.d.comb += w_position.eq(self.i_position)
        m.d.comb += w_position_1.eq(w_position[4])
        m.d.comb += w_alive_sum.eq( w_position[0] + w_position[1] +
                                    w_position[2] + w_position[3] +
                                    w_position[5] + w_position[6] +
                                    w_position[7] + w_position[8] )
        m.d.comb += self.o_middle_cell_status.eq(w_live_dead_status)

        # 3:0, (w_position[:4] % 4) = 0, 1, 2, 3
        # 8:5, (w_position[5:] % 4) = 0, 1, 2, 3
        # bus = Cat(a, b)  # 'b' is MSB, 'a' is LSB
        # bus = Cat(b, a)  # 'b' is LSB, 'a' is MSB
        with m.Switch(w_position_1):
            with m.Case(0): # dead
                #with m.If(( (w_position[:4] % 0xF) + (w_position[5:] % 0xF) ) == 2):
                with m.If(w_alive_sum == 2):
                    m.d.comb += w_live_dead_status.eq(w_position_1)
                with m.Elif(w_alive_sum == 3):
                    m.d.comb += w_live_dead_status.eq(1)
                with m.Else():
                    m.d.comb += w_live_dead_status.eq(0)


                # with m.Switch( ( (w_position[:4] % 0xF) + (w_position[5:] % 0xF) ) == 3 ):
                #     with m.Case(0b0):
                #         m.d.comb += w_live_dead_status.eq(0)
                #     with m.Case(0b1):
                #         m.d.comb += w_live_dead_status.eq(1)
                #     with m.Default():
                #         m.d.comb += w_live_dead_status.eq(0)

            with m.Case(1): # live
                with m.Switch( ( w_alive_sum  == 2 ) |
                               ( w_alive_sum  == 3 ) ):
                    with m.Case(0b0):
                        m.d.comb += w_live_dead_status.eq(0)
                    with m.Case(0b1):
                        m.d.comb += w_live_dead_status.eq(1)
                    with m.Default():
                        m.d.comb += w_live_dead_status.eq(0)
            with m.Default():
                m.d.comb += w_live_dead_status.eq(0)


        # m.d.comb += self.w_live_dead_status.eq(1)

        # with m.Switch(w_position_1):
        #     with m.Case(0): # live
        #         m.d.comb += self.w_live_dead_status.eq(0)
        #         m.d.comb += self.o_middle_cell_status.eq(self.w_live_dead_status)
        #         # m.d.comb += self.o_middle_cell_status.eq(0)
        #     with m.Case(1): # dead
        #         m.d.comb += self.w_live_dead_status.eq(1)
        #         m.d.comb += self.o_middle_cell_status.eq(self.w_live_dead_status)
        #         # m.d.comb += self.o_middle_cell_status.eq(1)
        #     with m.Default():
        #         m.d.comb += self.w_live_dead_status.eq(0)
        #         m.d.comb += self.o_middle_cell_status.eq(self.w_live_dead_status)
        #         # m.d.comb += self.o_middle_cell_status.eq(0)

        # with m.If(w_position_1):
        #     m.d.comb += self.w_live_dead_status.eq(0)
        # with m.Else():
        #     m.d.comb += self.w_live_dead_status.eq(1)
        #
            # m.d.comb += self.o_middle_cell_status.eq(self.w_live_dead_status)

        return m

    # Testbench Block
    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        m = Module()
        m.submodules.life_finds_a_way = dut = cls()

        # m.d.comb += Assert(dut.o_middle_cell_status == 1)

        s = 0
        for n in range(9):
            if n != 4:
                s += dut.i_position[n]

        with m.If(s == 3):
            m.d.comb += Assert(dut.o_middle_cell_status)
        with m.If(s == 2):
            m.d.comb += Assert(dut.o_middle_cell_status == dut.i_position[4])

        return m, [dut.i_position]


if __name__ == "__main__":
    # Generate the *.il file
    main(life_finds_a_way)

    # Generate the verilog and formal test file.
    file = Path("03-LifeFindsAWay.v")
    elaboratable = life_finds_a_way()
    ports = (elaboratable.i_position, elaboratable.o_middle_cell_status)
    name = "life_finds_a_way"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)

    elaboratable, inputs = life_finds_a_way.formal()
    generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
                   elaboratable=elaboratable, name='top', ports=inputs)
