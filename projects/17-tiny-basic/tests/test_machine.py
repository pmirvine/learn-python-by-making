import pytest
from conftest import Script, run

from tiny_basic import BasicError, Machine


def test_the_oldest_program_there_is(machine):
    assert run(machine, '10 PRINT "HELLO"') == "HELLO\n"


def test_lines_are_kept_in_order_and_can_be_replaced_and_deleted(machine):
    for line in ["30 PRINT 3", "10 PRINT 1", "20 PRINT 2", "20 print 22", "30"]:
        machine.enter(line)
    assert machine.listing() == ["   10 PRINT 1", "   20 print 22"]
    machine.enter("LIST")
    assert machine.console.text == "   10 PRINT 1\n   20 print 22\n"


@pytest.mark.parametrize(
    ("expression", "printed"),
    [
        ("2 + 3 * 4", "14"),
        ("10 - 4 - 3", "3"),
        ("2 ^ 3 ^ 2", "512"),
        ("-2 ^ 2", "-4"),
        ("7 / 2", "3.5"),
        ("7 DIV 2", "3"),
        ("-7 DIV 2", "-3"),
        ("7 MOD 2", "1"),
        ("1 / 3", "0.333333333"),
        ("1 = 1", "-1"),
        ("1 = 2", "0"),
        ("NOT 0", "-1"),
        ("3 > 2 AND 2 > 1", "-1"),
        ("6 AND 3", "2"),
        ("6 OR 3", "7"),
        ('"AB" + "CD"', "ABCD"),
        ('"APPLE" < "BANANA"', "-1"),
        ('LEFT$("MICRO", 2) + RIGHT$("MICRO", 2)', "MIRO"),
        ('MID$("MICRO", 2, 3)', "ICR"),
        ('LEN("BBC") * 2', "6"),
        ("INT(-2.5)", "-3"),
        ("SQR(16) + ABS(-1) + SGN(-9)", "4"),
        ('ASC("A")', "65"),
        ("CHR$(66)", "B"),
        ('VAL("12.5") + VAL("pardon?")', "12.5"),
        ('STR$(42) + "!"', "42!"),
        ("INT(PI * 100)", "314"),
    ],
)
def test_sums(machine, expression, printed):
    machine.enter(f"PRINT {expression}")
    assert machine.console.text == printed + "\n"


def test_print_with_semicolons_commas_and_nothing(machine):
    assert (
        run(
            machine,
            """
        10 PRINT "A"; "B", "C"
        20 PRINT "no new line";
        30 PRINT
        40 PRINT 1, 22, 333
    """,
        )
        == "AB        C\nno new line\n1         22        333\n"
    )


def test_for_next_with_a_step_and_a_loop_inside_a_loop(machine):
    assert (
        run(
            machine,
            """
        10 FOR I = 1 TO 2
        20   FOR J = 10 TO 0 STEP -5 : PRINT I * J; " "; : NEXT J
        30 NEXT
        40 PRINT "done"; I
    """,
        )
        == "10 5 0 20 10 0 done3\n"
    )


def test_a_for_loop_always_goes_round_once_as_on_the_bbc(machine):
    assert run(machine, '10 FOR I = 5 TO 1 : PRINT "once" : NEXT') == "once\n"


def test_repeat_until(machine):
    assert (
        run(
            machine,
            """
        10 N = 0
        20 REPEAT
        30   N = N + 1
        40 UNTIL N * N > 50
        50 PRINT N
    """,
        )
        == "8\n"
    )


def test_goto_gosub_and_end(machine):
    assert (
        run(
            machine,
            """
        10 GOSUB 100
        20 GOSUB 100
        30 GOTO 50
        40 PRINT "never"
        50 PRINT "end"
        60 END
        100 PRINT "sub ";
        110 RETURN
    """,
        )
        == "sub sub end\n"
    )


def test_if_then_else(machine):
    assert (
        run(
            machine,
            """
        10 FOR N = 1 TO 3
        20   IF N = 2 THEN PRINT "two"; : PRINT "!" ELSE PRINT N
        30 NEXT
        40 IF N > 3 THEN 60
        50 PRINT "skipped"
        60 PRINT "here"
    """,
        )
        == "1\ntwo!\n3\nhere\n"
    )


def test_input_into_numbers_and_strings():
    machine = Machine(Script("Ada", "36"))
    text = run(
        machine,
        """
        10 INPUT "Name? ", N$
        20 INPUT AGE
        30 PRINT N$; " is "; AGE + 1
    """,
    )
    assert text == "Name? ? Ada is 37\n"


def test_run_starts_afresh_but_immediate_statements_keep_the_variables(machine):
    machine.enter("10 PRINT X")
    machine.enter("X = 5")
    machine.enter("PRINT X * 2")
    assert machine.console.text == "10\n"
    with pytest.raises(BasicError, match="No such variable: X at line 10"):
        machine.enter("RUN")


def test_goto_from_the_keyboard_jumps_into_the_program(machine):
    machine.enter('10 PRINT "ten"')
    machine.enter('20 PRINT "twenty"')
    machine.enter("GOTO 20")
    assert machine.console.text == "twenty\n"


def test_the_machine_can_be_stepped_one_statement_at_a_time(machine):
    machine.enter("10 PRINT 1 : PRINT 2")
    machine.enter("20 PRINT 3")
    machine.load()
    assert machine.step()
    assert machine.console.text == "1\n"
    assert machine.step()
    assert machine.step()
    assert machine.step()  # the END that's put after every program
    assert not machine.step()
    assert machine.console.text == "1\n2\n3\n"


@pytest.mark.parametrize(
    ("program", "complaint"),
    [
        ("10 GOTO 55", "No such line at line 10"),
        ("10 PRINT 1 / 0", "Division by zero at line 10"),
        ("10 PRINT 7 MOD 0", "Division by zero at line 10"),
        ('10 PRINT "A" + 1', "Type mismatch at line 10"),
        ('10 PRINT "A" < 1', "Type mismatch at line 10"),
        ('10 X = "A"', "Type mismatch at line 10"),
        ("10 X$ = 5", "Type mismatch at line 10"),
        ("10 PRINT LEN(5)", "Type mismatch at line 10"),
        ("10 PRINT Q", "No such variable: Q at line 10"),
        ("10 NEXT", "No FOR at line 10"),
        ("10 FOR I = 1 TO 2\n20 NEXT J", "Can't match FOR"),
        ("10 UNTIL 1", "No REPEAT at line 10"),
        ("10 RETURN", "No GOSUB at line 10"),
        ("10 PRINT RND(1, 2)", "Wrong number of values for RND at line 10"),
        ("10 CLS 5", "Wrong number of values for CLS at line 10"),
        ("10 PRINT 10 ^ 400", "Too big at line 10"),
        ("10 PRINT SQR(-1)", "-ve root at line 10"),
        ("10 PRINT (-8) ^ 0.5", "-ve root at line 10"),
        ("10 INPUT X", "Escape at line 10"),
    ],
)
def test_things_that_go_wrong_while_running(machine, program, complaint):
    with pytest.raises(BasicError, match=complaint):
        run(machine, program)


def test_a_mistake_typed_at_the_prompt_has_no_line_number(machine):
    with pytest.raises(BasicError) as caught:
        machine.enter("PRINT 1 / 0")
    assert str(caught.value) == "Division by zero"


def test_a_bad_line_is_refused_when_it_is_typed_and_not_kept(machine):
    with pytest.raises(BasicError, match="Missing THEN"):
        machine.enter("10 IF X PRINT 1")
    assert machine.listing() == []


def test_random_numbers(machine):
    text = run(machine, "10 FOR I = 1 TO 50 : PRINT RND(6); : NEXT")
    assert set(text.strip()) <= set("123456")
    machine.enter("PRINT RND(1) < 1")
    assert machine.console.text.endswith("-1\n")


def test_cls_and_time(machine):
    machine.enter("CLS")
    assert machine.console.text == "\x1b[2J\x1b[H"
    machine.enter("PRINT TIME >= 0")
    assert machine.console.text.endswith("-1\n")


def test_new_save_and_load(machine, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    machine.enter('10 PRINT "saved"')
    machine.enter('SAVE "hello"')
    assert (tmp_path / "hello.bas").read_text(encoding="utf-8") == '10 PRINT "saved"\n'
    machine.enter("NEW")
    assert machine.listing() == []
    machine.enter('LOAD "hello"')
    machine.enter("RUN")
    assert machine.console.text == "saved\n"
    with pytest.raises(BasicError, match="File not found"):
        machine.enter('LOAD "goodbye"')


def test_remarks_and_empty_lines_do_nothing(machine):
    machine.enter("")
    machine.enter("   ")
    assert run(machine, "10 REM nothing to see\n20 PRINT 1 : REM or here") == "1\n"


def test_a_file_with_a_line_that_has_no_number_is_refused(machine, tmp_path):
    program = tmp_path / "bad.bas"
    program.write_text('10 PRINT "ok"\nPRINT "no number"\n', encoding="utf-8")
    with pytest.raises(BasicError, match="has a line with no number"):
        machine.load_file(program)


def test_trig_and_string(machine):
    machine.enter('PRINT INT(SIN(PI / 2) + COS(0)); STRING$(3, "ab")')
    assert machine.console.text == "2ababab\n"
