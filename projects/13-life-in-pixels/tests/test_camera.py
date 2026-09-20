import pytest

from pixel_life.camera import MAX_ZOOM, MIN_ZOOM, Camera


def test_at_the_start_the_origin_is_the_top_left_pixel():
    camera = Camera()
    assert camera.cell_at((0, 0)) == (0, 0)
    assert camera.cell_at((7, 7)) == (0, 0)
    assert camera.cell_at((8, 16)) == (1, 2)


@pytest.mark.parametrize(
    ("pixel", "cell"),
    [((0, 0), (-3, -2)), ((7, 7), (-3, -2)), ((8, 8), (-2, -1)), ((24, 16), (0, 0))],
)
def test_cells_left_of_and_above_the_origin(pixel, cell):
    camera = Camera(x=-3, y=-2)
    assert camera.cell_at(pixel) == cell


def test_pixel_of_is_the_way_back():
    camera = Camera(x=-3.5, y=2.25, zoom=16)
    for cell in [(0, 0), (-7, 5), (12, -4)]:
        assert camera.cell_at(camera.pixel_of(cell)) == cell


def test_panning_drags_the_universe_with_the_mouse():
    camera = Camera()
    under_the_pointer = camera.cell_at((100, 100))
    camera.pan(40, -24)
    assert camera.cell_at((140, 76)) == under_the_pointer


@pytest.mark.parametrize("factor", [2, 0.5, 1.25])
def test_zooming_keeps_the_cell_under_the_pointer_where_it_is(factor):
    camera = Camera(x=10, y=-10)
    pointer = (301, 199)
    before = camera.cell_at(pointer)
    camera.zoom_about(pointer, factor)
    assert camera.cell_at(pointer) == before
    assert camera.zoom == 8 * factor


def test_zoom_has_limits():
    camera = Camera()
    for _ in range(20):
        camera.zoom_about((0, 0), 2)
    assert camera.zoom == MAX_ZOOM
    for _ in range(20):
        camera.zoom_about((0, 0), 0.5)
    assert camera.zoom == MIN_ZOOM


def test_centring():
    camera = Camera(zoom=10)
    camera.centre_on((50, 20), (800, 600))
    assert camera.cell_at((400, 300)) == (50, 20)
