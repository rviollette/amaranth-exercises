from queue import SimpleQueue
from pathlib import Path
from amaranth import *
from amaranth.sim import Simulator
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from typing import List, Tuple, Any, Generator

from amaranth.build import Platform
from amaranth.hdl import Assume, Assert, Cover

# from answers.e01_to_pennies import ToPennies
from util import generate_verilog, generate_rtlil


#from amaranth.asserts import Past, Initial

#from util import main

# Design Block
class counting_coin(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """
    # Create the module input/output
    def __init__(self):
        # Inputs
        self.i_pennies    = Signal(8)     # 8 bits, from 0 to 255
        self.i_nickels    = Signal(4)     # 4 bits, from 0 to 15, 5-penny pieces,     75 pennies
        self.i_dimes      = Signal(4)     # 4 bits, from 0 to 15, 10-penny pieces,    150 pennies
        self.i_quarters   = Signal(4)     # 4 bits, from 0 to 15, 25-penny pieces,    375 pennies
        self.i_dollars    = Signal(4)     # 4 bits, from 0 to 15, 100-penny pieces,   1500 pennies

        # Outputs
        self.o_all_pennies    = Signal(12)    # 12 bits, from 0 to 255

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        # Internal wire (not an input/output port)
        pennies_for_pennies     = Signal(8)
        pennies_for_nickels     = Signal(8)
        pennies_for_dimes       = Signal(8)
        pennies_for_quarters    = Signal(9)
        pennies_for_dollars     = Signal(11)

        # Assign combination block
        m.d.comb += [
            pennies_for_pennies.eq(self.i_pennies),
            pennies_for_nickels.eq(self.i_nickels * 5),     # 75 pennies
            pennies_for_dimes.eq(self.i_dimes * 10),        # 150 pennies
            pennies_for_quarters.eq(self.i_quarters * 25),  # 375 pennies
            pennies_for_dollars.eq(self.i_dollars * 100),   # 1500 pennies

        ]

        # Combination for the output.
        m.d.comb += [
            self.o_all_pennies.eq(
                pennies_for_pennies +
                pennies_for_nickels +
                pennies_for_dimes +
                pennies_for_quarters +
                pennies_for_dollars
            )
        ]

        return m

# Testbench Block
async def test_counting_coin_tb(ctx):

    await ctx.delay(1e-6)
    # Test case 1: Simple case
    ctx.set(dut.i_pennies, 1)
    ctx.set(dut.i_nickels, 1)
    ctx.set(dut.i_dimes, 1)
    ctx.set(dut.i_quarters, 1)
    ctx.set(dut.i_dollars, 1)
    assert (ctx.get(dut.o_all_pennies)) == (1 + 5 + 10 + 25 + 100), "Test case 1 failed!"

    await ctx.delay(2e-6)
    # Test case 2: Max values
    ctx.set(dut.i_pennies, 255)
    ctx.set(dut.i_nickels, 15)
    ctx.set(dut.i_dimes, 15)
    ctx.set(dut.i_quarters, 15)
    ctx.set(dut.i_dollars, 15)
    assert (ctx.get(dut.o_all_pennies)) == (255 + 75 + 150 + 375 + 1500), "Test case 2 failed!"

    print("All tests passed!")

dut = counting_coin()   # Create the instance.
sim = Simulator(dut)    # Create the simulator.
sim.add_testbench(test_counting_coin_tb)
# Enable VCD waveform dumping
with sim.write_vcd("counting_coin.vcd", "counting_coin.gtkw",
                   traces=[dut.i_nickels, dut.i_dimes, dut.i_quarters, dut.i_dollars, dut.o_all_pennies]):
    sim.run()


if __name__ == "__main__":

    file = Path("01-counting_coin.v")
    elaboratable = counting_coin()
    ports = (elaboratable.i_pennies, elaboratable.i_nickels, elaboratable.i_dimes, elaboratable.i_quarters,
             elaboratable.i_dollars, elaboratable.o_all_pennies)
    name = "counting_coin"

    generate_verilog(file=file, elaboratable=elaboratable, name=name, ports=ports)
    generate_rtlil(file=file.with_suffix('.rtlil'), elaboratable=elaboratable, name=name, ports=ports)



    # main(ToPennies)
    # elaboratable, inputs = ToPennies.formal()
    # generate_rtlil(file=file.parent / (file.stem + '_formal.rtlil'),
    #                elaboratable=elaboratable, name='top', ports=inputs)



# sim.add_clock(1e-6)  # Simulate a clock with a 1MHz period
#     await ctx.delay(1e-6)
    # with sim.write_vcd("counting_coin.vcd", "counting_coin.gtkw",
    #     traces=[dut.i_nickels, dut.i_dimes, dut.i_quarters, dut.i_dollars, dut.o_all_pennies]):

    #     sim.run_until(1e-6 * 15)  # 15 periods of the clock

#         def process():
#             # Test case 1: Simple case
#             yield dut.i_nickels.eq(1)
#             yield dut.i_dimes.eq(1)
#             yield dut.i_quarters.eq(1)
#             yield dut.i_dollars.eq(1)
#             yield Tick()
#             assert (yield dut.o_all_pennies) == (5 + 10 + 25 + 100), "Test case 1 failed!"
#
#             # Test case 2: Max values
#             yield dut.i_nickels.eq(15)
#             yield dut.i_dimes.eq(15)
#             yield dut.i_quarters.eq(15)
#             yield dut.i_dollars.eq(15)
#             yield Tick()
#             assert (yield dut.o_all_pennies) == (75 + 150 + 375 + 1500), "Test case 2 failed!"
#
#             print("All tests passed!")
#
#
#             # sim.add_clock(1e-6)
#             # sim.add_testbench(test_counting_coin_tb)
#             sim.add_sync_process(process)
#             sim.run()
#
# # with sim.write_vcd("counting_coin.vcd"):
#
#     # sim.run()
#     # return sim
#
# # Run the testbench
# test_counting_coin_tb()

# Formal Testbench Block
#     @classmethod
#     def formal(cls) -> Tuple[Module, List[Signal]]:
#         """Formal verification for my module."""
#         m = Module()
#         m.submodules.my_class = my_class = cls()
#
#         return m, [my_class.my_input]


# if __name__ == "__main__":
#     main(counting_coin)