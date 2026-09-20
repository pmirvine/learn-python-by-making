"""An API for rolling dice. Run it with: uv run fastapi dev dice.py"""

import random
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Dice")


class Roll(BaseModel):
    dice: list[int]
    total: int
    lucky: bool


@app.get("/roll")
def roll(
    dice: Annotated[int, Query(ge=1, le=20)] = 2,
    sides: Annotated[int, Query(ge=2, le=100)] = 6,
) -> Roll:
    """Roll some dice. The limits are in the type hints, and nowhere else."""
    thrown = [random.randint(1, sides) for _ in range(dice)]
    return Roll(dice=thrown, total=sum(thrown), lucky=len(set(thrown)) == 1)
