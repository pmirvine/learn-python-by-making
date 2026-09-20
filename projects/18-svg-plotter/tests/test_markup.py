from plotter.markup import Safe, render


def test_the_fixed_parts_are_trusted_and_the_values_are_escaped():
    words = 'Fish & <Chips> "to go"'
    assert render(t"<text>{words}</text>") == (
        "<text>Fish &amp; &lt;Chips&gt; &quot;to go&quot;</text>"
    )


def test_a_value_cannot_break_out_of_an_attribute():
    colour = 'red" onload="alert(1)'
    markup = render(t'<path stroke="{colour}"/>')
    assert markup == '<path stroke="red&quot; onload=&quot;alert(1)"/>'
    assert markup.count('"') == 2


def test_format_specs_and_conversions_still_work():
    x, name = 3.14159, "pi"
    assert render(t"<text x='{x:.1f}'>{name!r}</text>") == (
        "<text x='3.1'>&#x27;pi&#x27;</text>"
    )


def test_a_template_inside_a_template_is_not_escaped_twice():
    words = "R&D"
    inner = t"<tspan>{words}</tspan>"
    assert render(t"<text>{inner}</text>") == "<text><tspan>R&amp;D</tspan></text>"


def test_a_list_of_templates():
    rows = [t"<li>{name}</li>" for name in ("Ant", "Bee & Co")]
    assert render(t"<ul>{rows}</ul>") == "<ul><li>Ant</li><li>Bee &amp; Co</li></ul>"


def test_what_has_been_rendered_is_safe_to_put_into_something_else():
    done = render(t"<b>{'<'}</b>")
    assert isinstance(done, Safe)
    assert render(t"<p>{done}</p>") == "<p><b>&lt;</b></p>"
