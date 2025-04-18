import streamlit as st
import requests
from io import BytesIO
from main import plan, Meal
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import json

# Streamlit app
st.title("Meal Plan Generator")

# User inputs
start_date = st.date_input("Select the start date:", value=datetime(2025, 4, 18))
number_of_meals = st.number_input("Enter the number of meals to plan:", min_value=1, value=21)

# Input for JSON file URL with default value
meals_url = st.text_input(
    "Enter the URL of the meals JSON file:",
    value="https://raw.githubusercontent.com/tjperr/mealplan/refs/heads/streamlit/meals.json"
)

# Add a "Generate" button
if st.button("Generate Meal Plan"):
    if meals_url:
        try:
            response = requests.get(meals_url)
            response.raise_for_status()
            meals_list = response.json()

            # Convert JSON to Meal objects
            meals = [Meal(**meal) for meal in meals_list]

            # Generate meal plan
            meal_plan = plan(meals, number_of_meals)

            # Create calendar
            cal = Calendar()
            date = datetime.combine(start_date, datetime.min.time())

            for meal in meal_plan:
                event = Event()
                event.add("summary", meal.name)
                event.add("dtstart", date)
                event.add("dtend", date + timedelta(hours=1))
                cal.add_component(event)
                date += timedelta(days=1)

            # Save calendar to a BytesIO object
            ics_file = BytesIO()
            ics_file.write(cal.to_ical())
            ics_file.seek(0)

            # Allow user to download the .ics file
            st.download_button(
                label="Download Meal Plan (.ics)",
                data=ics_file,
                file_name="mealplan.ics",
                mime="text/calendar",
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the meals JSON file: {e}")
        except json.JSONDecodeError:
            st.error("Invalid JSON format in the meals file.")
