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


class Meal:
    def __init__(self, name, carb, meat, freq, n_meals, cuisine, complexity):
        # Explicitly define and validate attributes
        self.name = str(name)
        self.carb = str(carb)
        self.meat = str(meat)
        self.freq = int(freq)
        self.n_meals = int(n_meals)
        self.cuisine = str(cuisine)
        self.complexity = int(complexity)

        # Additional validation (if needed)
        if self.freq < 0:
            raise ValueError("Frequency must be non-negative")
        if self.n_meals < 1:
            raise ValueError("Number of meals must be at least 1")


CARB_LIMIT = 3  # max acceptable same carb in a week
MEAT_LIMIT = 3  # max acceptable same meat in a week
COMPLEXITY_LIMIT = 21
START_DT = datetime(2023, 12, 11, 19, 0, 0)  # The first meal to be planned
N_MEALS = 30 * 3  # number of meals to plan


def plan(meals: List[Meal], days: int):
    """
    make a meal plan for `days` days from the meals in `meals`
    """
    plan = []
    while len(plan) < days:

        # for m in plan[-7:]:
        #    print(m)
        # print("----------------")

        candidate = random.choice(meals)

        # print(candidate)
        # print("----------------")
        print(sum([m.complexity for m in plan[-7:]]))

        if candidate in plan[-candidate.freq :]:  # Frequency limit
            # print("frequency limit")
            pass
        elif (
            sum([m.carb == candidate.carb for m in plan[-7:]]) + candidate.n_meals
            > CARB_LIMIT
        ):  # consecutive carb limit
            # print('carb limit')
            pass
        elif (candidate.meat != "") and (
            sum([m.meat == candidate.meat for m in plan[-7:]]) + candidate.n_meals
            > MEAT_LIMIT
        ):  # consecutive meat limit
            # print('meat limit')
            pass
        elif (
            sum([m.complexity for m in plan[-7 + candidate.n_meals :]])
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
