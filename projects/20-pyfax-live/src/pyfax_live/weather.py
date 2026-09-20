"""The weather, from Open-Meteo, which is free and wants no key."""

from dataclasses import dataclass
from datetime import date
from typing import Any

import httpx
from pyfax import Colour, Page
from pyfax.content import frame

URL = "https://api.open-meteo.com/v1/forecast"
NUMBER = 301

SUN = [
    "...#..#..#..",
    "....####....",
    ".#.######.#.",
    "...######...",
    "....####....",
    "..#..#..#...",
]
CLOUD = [
    "............",
    "....####....",
    "..########..",
    ".##########.",
    ".##########.",
    "............",
]
RAIN = [
    "....####....",
    "..########..",
    ".##########.",
    "............",
    "..#..#..#...",
    ".#..#..#....",
]
SNOW = [
    "....####....",
    "..########..",
    ".##########.",
    "............",
    ".#...#...#..",
    "...#...#....",
]
STORM = [
    "....####....",
    "..########..",
    ".##########.",
    ".....##.....",
    "....##......",
    "...#........",
]


class WeatherError(Exception):
    """The forecast couldn't be fetched, or made no sense when it arrived."""


@dataclass(frozen=True, slots=True)
class Place:
    name: str
    latitude: float
    longitude: float


@dataclass(frozen=True, slots=True)
class Day:
    day: date
    code: int
    high: float
    low: float


@dataclass(frozen=True, slots=True)
class Forecast:
    temperature: float
    wind: float
    code: int
    days: tuple[Day, ...]


def describe(code: int) -> tuple[str, list[str], Colour]:
    """Turn one of the World Meteorological Organization's codes into words and a picture."""
    match code:
        case 0 | 1:
            return "Sunny", SUN, Colour.YELLOW
        case 2 | 3:
            return "Cloudy", CLOUD, Colour.WHITE
        case 45 | 48:
            return "Foggy", CLOUD, Colour.WHITE
        case 71 | 73 | 75 | 77 | 85 | 86:
            return "Snow", SNOW, Colour.WHITE
        case 95 | 96 | 99:
            return "Thunder", STORM, Colour.YELLOW
        case _ if 51 <= code <= 82:
            return "Rain", RAIN, Colour.CYAN
        case _:
            return "Who knows", CLOUD, Colour.MAGENTA


def parse(data: Any) -> Forecast:
    """Pick what we want out of Open-Meteo's reply, and check that it's all there."""
    match data:
        case {
            "current": {
                "temperature_2m": float() | int() as temperature,
                "wind_speed_10m": float() | int() as wind,
                "weather_code": int(code),
            },
            "daily": {
                "time": [*days],
                "weather_code": [*codes],
                "temperature_2m_max": [*highs],
                "temperature_2m_min": [*lows],
            },
        }:
            pass
        case _:
            raise WeatherError("The forecast wasn't in the shape that was expected")
    try:
        forecast = tuple(
            Day(date.fromisoformat(day), int(code), float(high), float(low))
            for day, code, high, low in zip(days, codes, highs, lows, strict=True)
        )
    except (TypeError, ValueError) as error:
        raise WeatherError(f"The forecast had something odd in it: {error}") from error
    return Forecast(float(temperature), float(wind), code, forecast)


def fetch(place: Place, client: httpx.Client) -> Forecast:
    """Ask Open-Meteo for the weather at a place."""
    wanted = {
        "latitude": place.latitude,
        "longitude": place.longitude,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": 3,
    }
    try:
        response = client.get(URL, params=wanted, timeout=5)
        response.raise_for_status()
        return parse(response.json())
    except (httpx.HTTPError, ValueError) as error:
        raise WeatherError(f"Couldn't fetch the forecast: {error}") from error


def page(place: Place, forecast: Forecast | None, today: date) -> Page:
    """Make the weather page. With no forecast, it says so, and is still a page."""
    sheet = Page(NUMBER, f"Weather for {place.name}", "weather")
    frame(sheet, today, "weather", Colour.CYAN)
    sheet.write(4, 1, f"Weather for {place.name}", Colour.YELLOW)
    if forecast is None:
        sheet.write(8, 1, "There's no forecast at the moment.", Colour.WHITE)
        sheet.write(10, 1, "Try looking out of the window.", Colour.CYAN)
        return sheet

    words, _picture, _colour = describe(forecast.code)
    now = f"Now: {forecast.temperature:.0f}C, {words.lower()}, wind {forecast.wind:.0f} km/h"
    sheet.write(6, 1, now, Colour.WHITE)
    for number, day in enumerate(forecast.days):
        column = 1 + number * 13
        words, picture, colour = describe(day.code)
        sheet.picture(9, column, picture, colour)
        sheet.write(12, column, f"{day.day:%A}"[:12], Colour.YELLOW)
        sheet.write(13, column, words, Colour.WHITE)
        sheet.write(14, column, f"{day.high:.0f}C / {day.low:.0f}C", Colour.CYAN)
    sheet.write(20, 1, "Forecast from open-meteo.com", Colour.BLUE)
    return sheet
