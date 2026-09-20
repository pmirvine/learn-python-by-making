"""Pictures of the app, kept in tests/__snapshots__, and compared with every run.

If a picture ought to change, look at the report that the failure points to,
and then: uv run pytest --snapshot-update
"""

SIZE = (60, 30)


def test_the_index(snap_compare, make_viewer):
    assert snap_compare(make_viewer(), terminal_size=SIZE)


def test_the_weather_with_its_graphics(snap_compare, make_viewer):
    assert snap_compare(make_viewer(), press=["3", "0", "1"], terminal_size=SIZE)


def test_a_number_half_typed(snap_compare, make_viewer):
    assert snap_compare(make_viewer(), press=["5", "0"], terminal_size=SIZE)


def test_no_such_page(snap_compare, make_viewer):
    assert snap_compare(make_viewer(), press=["7", "7", "7"], terminal_size=SIZE)
