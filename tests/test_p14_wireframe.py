"""Repo-level checks for Project 14: the ships themselves, the stage, and the extras.

The reader's own tests are in the project's tests/ folder.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("wireframe", reason="needs the Project 14 environment")

from wireframe.matrix import rotation_x
from wireframe.model import hangar, load
from wireframe.projection import faces_the_eye, normal

P14 = Path(__file__).parent.parent / "projects" / "14-wireframe"
HEADLESS = Path(__file__).parent / "headless.py"


def test_stage1_is_a_vector_that_has_not_met_a_matrix():
    spec = importlib.util.spec_from_file_location(
        "stage1_vec3", P14 / "stages" / "stage1_vec3.py"
    )
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    assert stage.Vec3(1, 0, 0).cross(stage.Vec3(0, 1, 0)) == stage.Vec3(0, 0, 1)
    assert not hasattr(stage.Vec3, "__rmatmul__")


@pytest.mark.parametrize("ship", hangar(), ids=lambda ship: ship.name)
def test_every_ship_is_flat_faced_and_has_no_dents_and_faces_outwards(ship):
    """Hidden lines by back-face culling alone are only right for such a ship."""
    for face in ship.faces:
        corners = [ship.points[number] for number in face.points]
        outwards = normal(corners)
        for point in ship.points:
            height = outwards.dot(point - corners[0])
            if point in corners:
                assert height == pytest.approx(0, abs=1e-6), f"{face} isn't flat"
            else:
                assert height < 0, f"{face} has something in front of it"


def test_every_point_of_every_ship_is_used():
    for ship in hangar():
        used = {number for face in ship.faces for number in face.points}
        assert used == set(range(len(ship.points))), ship.name


def test_the_bug_hunt_ship_loads_and_shows_its_symptom():
    skiff = load(P14 / "bughunt" / "skiff.toml")
    # Look down on it from above: the sloping top ought to be in plain view.
    tipped = [rotation_x(60) @ point for point in skiff.points]
    top = [tipped[number] for number in skiff.faces[4].points]
    assert not faces_the_eye(top, 3 * skiff.radius)

    mended = load(P14 / "solutions" / "bughunt" / "skiff.toml")
    tipped = [rotation_x(60) @ point for point in mended.points]
    top = [tipped[number] for number in mended.faces[4].points]
    assert faces_the_eye(top, 3 * mended.radius)


def test_stage4_draws_the_same_wires_as_the_finished_view():
    import pygame
    from wireframe.view import Style, View

    spec = importlib.util.spec_from_file_location(
        "stage4_view", P14 / "stages" / "stage4_view.py"
    )
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)

    pygame.init()
    ship = hangar()[0]
    turn = rotation_x(30)
    pictures = []
    for view, style in ((stage.View, stage.Style.WIRES), (View, Style.WIRES)):
        window = pygame.Surface((320, 240))
        view(window).draw(ship, turn, 3 * ship.radius, style)
        pictures.append(pygame.image.tobytes(window, "RGB"))
    pygame.quit()
    assert pictures[0] == pictures[1]


def run_headless(program: Path, frames: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, HEADLESS, program, str(frames)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_the_cube_runs():
    result = run_headless(P14 / "cube.py", 30)
    assert result.returncode == 0, result.stderr


def test_the_program_itself_runs(tmp_path):
    program = tmp_path / "play.py"
    program.write_text("from wireframe.app import main\n\nmain()\n", encoding="utf-8")
    result = run_headless(program, 30)
    assert result.returncode == 0, result.stderr


def test_slots_save_what_the_chapter_says():
    result = subprocess.run(
        [sys.executable, P14 / "measure_slots.py"],
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )
    roomy, slotted = (int(line.split()[1]) for line in result.stdout.splitlines())
    assert slotted < roomy
    assert 30 <= roomy - slotted <= 60


def test_the_tasks_and_the_snippets_are_sound():
    tasks = json.loads((P14 / ".vscode" / "tasks.json").read_text(encoding="utf-8"))
    labels = {task["label"] for task in tasks["tasks"]}
    for task in tasks["tasks"]:
        assert set(task.get("dependsOn", [])) <= labels
    defaults = [
        task["label"]
        for task in tasks["tasks"]
        if isinstance(task.get("group"), dict) and task["group"].get("isDefault")
    ]
    assert defaults == ["Test", "Check everything"]

    snippets = json.loads(
        (P14 / ".vscode" / "wireframe.code-snippets").read_text(encoding="utf-8")
    )
    assert {snippet["prefix"] for snippet in snippets.values()} == {"face", "ptest"}
    face = "\n".join(snippets["A face of a ship"]["body"])
    assert face.startswith("[[faces]]\npoints = [")
