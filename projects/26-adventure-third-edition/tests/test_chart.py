from adventure.chart import draw
from adventure.game import Chart, Place

CUPBOARD = Place("Cupboard", 0, 0, 0, "s")
HALL = Place("Hall", 0, 1, 0, "newu")
KITCHEN = Place("Kitchen", 1, 1, 0, "ws")
LANDING = Place("Landing", 0, 1, 1, "ud")


def test_one_room_with_a_door_to_the_south():
    assert draw(Chart((CUPBOARD,), CUPBOARD)) == [
        " ╔════════╗",
        " ║Cupboard║",
        " ╚════╤═══╝",
    ]


def test_the_room_you_are_in_has_double_walls_and_doors_join_up():
    assert draw(Chart((CUPBOARD, HALL, KITCHEN), HALL)) == [
        " ┌────────┐",
        " │Cupboard│",
        " └────┬───┘",
        " ╔════╧═▲═╗ ┌────────┐",
        "─╢  Hall  ╟─┤Kitchen │",
        " ╚════════╝ └────┬───┘",
    ]


def test_an_unexplored_exit_is_a_loose_end():
    lines = draw(Chart((HALL,), HALL))
    assert lines[1] == "─╢  Hall  ╟─"


def test_only_the_floor_you_are_on_is_drawn():
    assert draw(Chart((CUPBOARD, HALL, LANDING), LANDING)) == [
        " ╔══════▲═╗",
        " ║Landing ║",
        " ╚══════▼═╝",
    ]


def test_a_long_name_is_cut_to_fit():
    hall = Place("Conservatory", 0, 0)
    assert draw(Chart((hall,), hall))[1] == " ║Conserva║"
