import extras
from conftest import Script

from tiny_basic import Machine


def test_new_functions_and_a_new_command_with_no_change_to_the_parser():
    assert extras.instr("BBC MICRO", "MIC") == 5
    console = Script()
    machine = Machine(console)
    machine.enter('PRINT UPPER$("beeb"); INSTR("BBC MICRO", "MIC"); INT(DEG(PI))')
    machine.enter("WAIT 1 : PRINT INT(TAN(0))")
    assert console.text == "BEEB5180\n0\n"
