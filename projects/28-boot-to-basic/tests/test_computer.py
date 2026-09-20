import beeb
import pygame
from conftest import lines, run

from micro.computer import Micro


def test_it_boots_to_a_prompt(micro: Micro):
    assert lines(micro) == ["Python Micro 64K", "Tiny BASIC", ">"]
    assert not micro.running


def test_a_statement_with_no_number_is_done_at_once(micro: Micro):
    micro.type_in("PRINT 6*7\n")
    micro.frame()
    assert lines(micro)[-3:] == [">PRINT 6*7", "42", ">"]


def test_a_program_is_kept_listed_and_run(micro: Micro):
    run(micro, "20 PRINT I*I;", "10 FOR I=1 TO 4", "30 NEXT")
    assert lines(micro)[-2:] == ["14916", ">"]
    micro.type_in("LIST\n")
    assert lines(micro)[-4:-1] == [
        "   10 FOR I=1 TO 4",
        "   20 PRINT I*I;",
        "   30 NEXT",
    ]


def test_a_mistake_is_reported_and_the_computer_carries_on(micro: Micro):
    micro.type_in("FROG\n")
    assert "Mistake: I don't know what to do with FROG" in "".join(lines(micro))
    run(micro, "10 PRINT 1/0")
    assert lines(micro)[-2:] == ["Division by zero at line 10", ">"]


def test_a_program_that_never_ends_does_not_freeze_the_computer(micro: Micro):
    run(micro, "10 GOTO 10", frames=3)
    assert micro.running
    assert micro.frames >= 3


def test_escape_stops_a_program(micro: Micro):
    run(micro, "10 GOTO 10", frames=3)
    micro.press(pygame.K_ESCAPE)
    micro.frame()
    assert not micro.running
    assert lines(micro)[-2:] == ["Escape at line 10", ">"]


def test_wait_gives_up_the_rest_of_the_frame(micro: Micro):
    run(micro, "10 N=0", "20 N=N+1: WAIT: GOTO 20", frames=2)
    before = micro.machine.variables["N"]
    for _ in range(10):
        micro.frame()
    assert micro.machine.variables["N"] == before + 10


def test_input_takes_what_was_typed_ahead(micro: Micro):
    run(micro, '10 INPUT "NAME? ", N$', '20 PRINT "HELLO ";N$', frames=0)
    micro.type_in("BBC\n")  # typed while the program runs, before it has asked
    assert lines(micro)[-3:] == ["NAME? BBC", "HELLO BBC", ">"]
    assert not micro.reading


def test_input_waits_for_a_line_while_the_frames_go_by(micro: Micro, monkeypatch):
    """Here the keys arrive late: one in each frame, once the INPUT is waiting."""
    keys = [
        pygame.event.Event(pygame.KEYDOWN, key=key, unicode=character)
        for key, character in [(pygame.K_7, "7"), (pygame.K_RETURN, "\r")]
    ]
    monkeypatch.setattr(
        pygame.event, "get", lambda: [keys.pop(0)] if micro.reading and keys else []
    )
    frames = micro.frames
    run(micro, "10 INPUT A", "20 PRINT A*6")
    assert lines(micro)[-3:] == ["? 7", "42", ">"]
    assert micro.frames >= frames + 2


def test_escape_during_an_input(micro: Micro, monkeypatch):
    escape = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, unicode="\x1b")
    monkeypatch.setattr(pygame.event, "get", lambda: [escape] if micro.reading else [])
    run(micro, "10 INPUT A", "20 PRINT 99")
    assert lines(micro)[-2:] == ["Escape at line 10", ">"]
    assert not micro.reading


def test_graphics_from_basic(micro: Micro):
    run(micro, "10 MODE 1", "20 GCOL 0,1", "30 MOVE 0,0: DRAW 1279,1023")
    assert beeb.point(0, 0) == 1
    assert beeb.point(1279, 0) == 0
    assert lines(micro) == [">"]


def test_a_bad_value_stops_the_program_and_not_the_computer(micro: Micro):
    run(micro, "10 PLOT 999,0,0")
    assert lines(micro)[-2:] == ["PLOT 999 isn't supported at line 10", ">"]
    run(micro, "10 MODE 9")
    assert lines(micro)[-2:] == ["Bad MODE at line 10", ">"]


def test_tab_and_colour(micro: Micro):
    run(micro, "10 CLS", '20 COLOUR 3: PRINT TAB(10,5);"HERE"')
    cell = micro.screen.page.rows[5][10]
    assert (cell.text, int(cell.ink)) == ("H", 3)


def test_keys_that_are_held_down(micro: Micro):
    micro.press(pygame.K_z)
    run(micro, "10 PRINT INKEY(-98); INKEY(-67)")
    assert lines(micro)[-2] == "-10"
    micro.release(pygame.K_z)
    run(micro, "10 PRINT INKEY(-98)")
    assert lines(micro)[-2] == "0"


def test_keys_that_were_typed_while_the_program_ran(micro: Micro):
    run(micro, "10 K=INKEY(0): WAIT", "20 IF K=-1 THEN GOTO 10", "30 PRINT K", frames=3)
    assert micro.running
    micro.press(ord("a"), "A")
    run_on = [micro.frame() for _ in range(3)]
    assert len(run_on) == 3
    assert lines(micro)[-2:] == ["65", ">"]


def test_sprites_from_basic(micro: Micro):
    run(
        micro,
        '10 SPRITE 1,"ship": SPRITE 2,"alien"',
        "20 PUT 1,600,32: PUT 2,600,900: PRINT COLLIDE(1,2);",
        "30 PUT 2,604,40: PRINT COLLIDE(1,2);",
        "40 PUT 2,-8,500: PRINT EDGE(2)",
    )
    assert lines(micro)[-2:] == ["0-11", ">"]
    assert micro.sprites.slot(1).showing


def test_sprites_are_drawn_over_the_picture_and_leave_it_alone(micro: Micro):
    run(micro, '10 SPRITE 1,"alien": PUT 1,600,500')
    window = pygame.display.get_surface()
    assert window is not None
    box = micro.sprites.box(1)
    green = [
        (x, y)
        for x in range(box.left * 2, box.right * 2)
        for y in range(box.top * 2, box.bottom * 2)
        if window.get_at((x, y))[:3] == (0, 255, 0)
    ]
    assert green
    assert all(
        beeb.point(x, y) == 0 for x in range(580, 680, 4) for y in range(480, 580, 4)
    )


def test_a_sprite_that_is_not_on_the_disc(micro: Micro):
    run(micro, '10 SPRITE 1,"frog"')
    assert lines(micro)[-2:] == ["Sprite not found: frog at line 10", ">"]


def test_the_disc(micro: Micro):
    micro.type_in('NEW\n10 PRINT "KEPT"\nSAVE "keeper"\nNEW\nLOAD "keeper"\nRUN\n')
    micro.frame()
    assert lines(micro)[-2:] == ["KEPT", ">"]
    assert (micro.disc / "keeper.bas").read_text(
        encoding="utf-8"
    ) == '10 PRINT "KEPT"\n'
    micro.type_in("CLS\n")
    micro.frame()
    micro.type_in("CAT\n")
    assert "keeper.bas" in lines(micro)
    assert "alien.sprite" in lines(micro)


def test_a_program_that_is_not_on_the_disc(micro: Micro):
    micro.type_in('LOAD "nothing"\n')
    assert any("File not found" in line for line in lines(micro))


def test_sound_from_basic(micro: Micro):
    run(micro, "10 ENVELOPE 1,1,2,0.5,3", "20 SOUND 1,1,53,2: SOUND 0,-10,4,1")
    assert lines(micro)[-1] == ">"
    run(micro, "10 SOUND 9,-15,53,2")
    assert "at line 10" in lines(micro)[-2]
