import json
import os
import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from icalendar import Calendar, Event

from meals import meals_list


@dataclass
class Meal:
    name: string
    carb: string
    meat: string
    freq: int
    n_meals: int
    cuisine: string
    complexity: int


CARB_LIMIT = 2  # max acceptable same carb in a week
MEAT_LIMIT = 2  # max acceptable same meat in a week
COMPLEXITY_LIMIT = 14
START_DT = datetime(2023, 1, 17, 19, 0, 0)  # The first meal to be planned
N_MEALS = 3*30  # number of meals to plan


def plan(meals: List[Meal], days: int):
    """
    make a meal plan for `days` days from the meals in `meals`
    """
    plan = []
    while len(plan) < days:

        print(len(plan) / days)

        # for m in plan[-7:]:
        #    print(m)
        # print("----------------")

        candidate = random.choice(meals)

        # print(candidate)
        # print("----------------")

        if candidate in plan[-candidate.freq :]:  # Frequency limit
            # print("frequency limit")
            pass
        elif (
            sum([m.carb == candidate.carb for m in plan[-7:]]) > CARB_LIMIT
        ):  # consecutive carb limit
            # print('carb limit')
            pass
        elif (
            sum([m.meat == candidate.meat for m in plan[-7:]]) > MEAT_LIMIT
        ):  # consecutive meat limit
            # print('meat limit')
            pass
        elif (
            sum([m.complexity for m in plan[-7:]])
            + (candidate.n_meals * candidate.complexity)
            > COMPLEXITY_LIMIT
        ):
            # print('complexity limit')
            pass
        else:
            plan += candidate.n_meals * [candidate]

    return plan


def main():

    meals: List[Meal] = [Meal(**obj) for obj in meals_list]

    cal = Calendar()
    date = START_DT

    for meal in plan(meals, N_MEALS):
        print(f"{meal.name} ({meal.meat}, {meal.carb})")

        event = Event()
        event.add("summary", meal.name)
        event.add("dtstart", date)
        event.add("dtend", date + timedelta(hours=1))
        cal.add_component(event)

        date = date + timedelta(days=1)

    directory = str(Path(__file__).parent) + "/"
    print("ics file will be generated at ", directory)
    f = open(os.path.join(directory, "mealplan.ics"), "wb")
    f.write(cal.to_ical())
    f.close()


if __name__ == "__main__":
    main()
