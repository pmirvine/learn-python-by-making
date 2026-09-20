from life import PATTERNS, parse

from pixel_life.simulation import Simulation

BLINKER = parse(PATTERNS["blinker"])


def test_a_new_simulation_is_paused():
    simulation = Simulation(BLINKER)
    simulation.update(10.0)
    assert simulation.generation == 0
    assert simulation.live == BLINKER


def test_stepping_by_hand():
    simulation = Simulation(BLINKER)
    simulation.step()
    simulation.step()
    assert simulation.generation == 2
    assert simulation.live == BLINKER


def test_running_at_ten_generations_a_second():
    simulation = Simulation(BLINKER)
    simulation.running = True
    simulation.update(0.25)
    assert simulation.generation == 2
    simulation.update(0.06)
    assert simulation.generation == 3


def test_a_stalled_frame_does_not_mean_a_flood_of_generations():
    simulation = Simulation(BLINKER)
    simulation.running = True
    simulation.update(60.0)
    assert simulation.generation == 5


def test_painting_and_rubbing_out():
    simulation = Simulation()
    simulation.paint((3, 4), alive=True)
    simulation.paint((3, 4), alive=True)
    assert simulation.live == {(3, 4)}
    simulation.paint((3, 4), alive=False)
    simulation.paint((9, 9), alive=False)
    assert simulation.live == set()


def test_loading_a_pattern_somewhere():
    simulation = Simulation(BLINKER)
    simulation.step()
    simulation.load({(0, 0), (1, 0)}, at=(10, -5))
    assert simulation.live == {(10, -5), (11, -5)}
    assert simulation.generation == 0


def test_the_simulation_does_not_keep_hold_of_the_set_it_was_given():
    cells = {(0, 0)}
    simulation = Simulation(cells)
    simulation.paint((5, 5), alive=True)
    assert cells == {(0, 0)}


def test_speed_has_limits():
    simulation = Simulation()
    for _ in range(20):
        simulation.faster(2)
    assert simulation.speed == 240
    for _ in range(20):
        simulation.faster(0.5)
    assert simulation.speed == 1
