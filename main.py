import json
import random
import string
from dataclasses import dataclass
from typing import List

from meals import meals_list


@dataclass
class Meal:
    name: string
    carb: string
    meat: string
    freq: int
    n_meals: int


CARB_LIMIT = 2  # max acceptable same carb in a week
MEAT_LIMIT = 2  # max acceptable same meat in a week


def plan(meals: List[Meal], days: int):
    """
    make a meal plan for `days` days from the meals in `meals`
    """

    plan = []
    while len(plan) < days:

        candidate = random.choice(meals)

        if candidate in plan[-candidate.freq :]:  # Frequency limit
            pass
        elif (
            sum([m.carb == candidate.carb for m in plan[-7:]]) > CARB_LIMIT
        ):  # consecutive carb limit
            pass
        elif (
            sum([m.meat == candidate.meat for m in plan[-7:]]) > MEAT_LIMIT
        ):  # consecutive meat limit
            pass
        else:
            plan += candidate.n_meals * [candidate]

    return plan


def main():

    meals: List[Meal] = [Meal(**obj) for obj in meals_list]

    for p in plan(meals, 10):
        print(f"{p.name} ({p.meat}, {p.carb})")


if __name__ == "__main__":
    main()
