"""Turning a t-string into markup, with everything that was put into it made safe."""

from html import escape
from string.templatelib import Interpolation, Template, convert


class Safe(str):
    """Markup that's already been made safe, and mustn't be escaped a second time."""

    __slots__ = ()


def render(template: Template) -> Safe:
    """Return a template as text. The fixed parts are trusted, and the rest is escaped."""
    parts: list[str] = []
    for part in template:
        match part:
            case str():
                parts.append(part)
            case Interpolation(value, _, conversion, format_spec):
                parts.append(insert(convert(value, conversion), format_spec))
    return Safe("".join(parts))


type Insertable = Safe | Template | list[Insertable] | str | float


def insert(value: Insertable, format_spec: str) -> str:
    """Return one value, ready to go into markup."""
    match value:
        case Safe():
            return value
        case Template():
            return render(value)
        case list():
            return "".join(insert(item, format_spec) for item in value)
        case _:
            return escape(format(value, format_spec), quote=True)
