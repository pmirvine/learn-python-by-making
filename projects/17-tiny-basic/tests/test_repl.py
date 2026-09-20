import pytest

from tiny_basic import Machine
from tiny_basic.repl import Terminal, converse, main, timed


def type_in(monkeypatch, *lines: str) -> None:
    replies = iter(lines)

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        try:
            return next(replies)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr("builtins.input", fake_input)


def test_a_conversation(monkeypatch, capsys):
    type_in(monkeypatch, '10 PRINT "HELLO"', "20 GOTO 5", "RUN", "PRINT 2 + 2", "QUIT")
    converse(Machine(Terminal()))
    out = capsys.readouterr().out
    assert out == "Tiny BASIC\n\n>>>HELLO\n\nNo such line at line 20\n>4\n>"


def test_the_end_of_the_input_ends_the_conversation(monkeypatch, capsys):
    type_in(monkeypatch, "PRINT 1")
    converse(Machine(Terminal()))
    assert capsys.readouterr().out.endswith(">1\n>\n")


def test_running_a_file(monkeypatch, capsys, tmp_path):
    program = tmp_path / "count.bas"
    program.write_text("10 FOR I = 1 TO 3\n20 PRINT I;\n30 NEXT\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["basic", str(program), "--time"])
    main()
    captured = capsys.readouterr()
    assert captured.out == "123"
    assert "[loading: 0.0" in captured.err
    assert "[running: 0.0" in captured.err


def test_a_file_that_goes_wrong(monkeypatch, tmp_path):
    program = tmp_path / "bad.bas"
    program.write_text("10 PRINT 1 / 0\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["basic", str(program)])
    with pytest.raises(SystemExit, match="Division by zero at line 10"):
        main()


def test_timed_reports_even_when_something_goes_wrong(capsys):
    with pytest.raises(ZeroDivisionError), timed("dividing"):
        print(1 / 0)
    assert "[dividing: 0.0" in capsys.readouterr().err
