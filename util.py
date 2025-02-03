# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
"""
This module provides various global utilities.
"""
import sys

from amaranth.back import rtlil
from amaranth.hdl import Fragment

from amaranth.back import verilog as amaranth_verilog

if sys.version_info < (3, 8):
    print("Python 3.8 or above is required")
    sys.exit(1)


def main(cls, filename="toplevel.il"):
    """Runs a file in simulate or generate mode.

    Add this to your file:

        from util import main

        if __name__ == "__main__":
            main(YourClass)

    Then, you can run the file in simulate or generate mode:

    python <file.py> sim will run YourClass.sim and output to whatever vcd
        file you wrote to.
    python <file.py> gen will run YourClass.formal and output in RTLIL format
        to toplevel.il. You can then formally verify using
        sby -f <file.sby>.
    """

    if len(sys.argv) < 2 or (sys.argv[1] != "sim" and sys.argv[1] != "gen"):
        print(f"Usage: python {sys.argv[0]} sim|gen")
        sys.exit(1)

    if sys.argv[1] == "sim":
        cls.sim()
    else:
        design, ports = cls.formal()
        fragment = Fragment.get(design, None)
        output = rtlil.convert(fragment, ports=ports)
        with open(filename, "w") as f:
            f.write(output)



# ----------------------------------------------------------------------------------------------------------------------
# common
# ----------------------------------------------------------------------------------------------------------------------
def generate_verilog(file, elaboratable, name, ports=None, verbose=True):
    """
    Convert Amaranth module into Verilog file, using Yosys toolchain.

    For Verilog port definition, see ``amaranth.hdl._ir.Fragment._prepare_ports``.

    :param file: Verilog file to save the generation to
    :type file: ``Path``
    :param elaboratable: Amaranth elaboratable
    :type elaboratable: ``Elaboratable``
    :param name: Verilog module name
    :type name: ``str``
    :param ports: Verilog port listing, default to None (when Elaboratable has a Signature) - OPTIONAL
    :type ports: ``None or list or tuple or dict``
    """
    verbose and sys.stdout.write(f'{elaboratable.__class__}: {file} ...')

    verilog = amaranth_verilog.convert(elaboratable=elaboratable, name=name, ports=ports,
                                       emit_src=False, strip_internal_attrs=True)
    file.write_text(verilog)

    verbose and (sys.stdout.write(f' OK\n'), sys.stdout.flush())
# end def generate_verilog


def generate_rtlil(file, elaboratable, name, ports=None, verbose=True):
    """
    Convert Amaranth module into RTLIL (RTL Intermediate Language) file, using Yosys toolchain.

    Doc: https://yosyshq.readthedocs.io/projects/yosys/en/latest/yosys_internals/formats/rtlil_rep.html

    For Verilog port definition, see ``amaranth.hdl._ir.Fragment._prepare_ports``.

    :param file: RTLIL file to save the generation to
    :type file: ``Path``
    :param elaboratable: Amaranth elaboratable
    :type elaboratable: ``Elaboratable``
    :param name: Verilog module name
    :type name: ``str``
    :param ports: Verilog port listing, default to None (when Elaboratable has a Signature) - OPTIONAL
    :type ports: ``None or list or tuple or dict``
    """
    verbose and sys.stdout.write(f'{elaboratable.__class__}: {file} ...')

    il = rtlil.convert(elaboratable=elaboratable, name=name, ports=ports,
                       emit_src=False)
    file.write_text(il)

    verbose and (sys.stdout.write(f' OK\n'), sys.stdout.flush())
# end def generate_rtlil
