import json
import os
import tkinter.ttk
import turtle
import json
from tkinter import messagebox

import requests
import datetime as dt
from tkinter import *

APP_ID = os.environ.get("ENV_APP_ID")
APP_API = os.environ.get("ENV_APP_API")
NUTRITIONIX_API_ENDPOINT = os.environ.get("ENV_NUTRI_API_ENDPOINT")

#SHEET_API_ENDPOINT = os.environ.get("ENV_SHEET_API_ENDPOINT")
#AUTHENTICATION_TOKEN = f"Bearer {os.environ.get('ENV_AUTH_TOKEN')}"

# New sheety account (with available requests)
SHEET_API_ENDPOINT = "https://api.sheety.co/234adb1f96af1d240319a4266ba2a280/workoutTracking/workouts"
AUTHENTICATION_TOKEN = "dzfgd56231dgr651grd123dgr654gr"

# -----------------------------------------Place into class---------------------------------------------
header = {
    "x-app-id":  APP_ID,
    "x-app-key": APP_API,
}

signin_params = {
    "password": "redfern1155@gmail.com",
    "email": "!Allnewfern2678!"
}

def add_workout():
    exercise = input_box.get()

    gender = gender_selection.get()
    weight = weight_input_box.get()
    height = height_input_box.get()
    age = age_input_box.get()

    if gender == "" or weight == "" or weight == "0" or height == "" or height == "0" or age == "" or height == "0":
        messagebox.showinfo(title=f"Missing personal data", message="All personal data is required")
        return
    if input_box.get() == "":
        messagebox.showinfo(title=f"Missing workout", message="Invalid workout")
        return

    exercise_config = {
        "query": exercise,
        "gender": gender,
        "weight_kg": weight,
        "height_cm":  height,
        "age": age
    }

    try:
        response = requests.post(url=NUTRITIONIX_API_ENDPOINT, json=exercise_config, headers=header)
        print(response.raise_for_status())
    except requests.exceptions.HTTPError as err:
        messagebox.showinfo(title=f"Error", message="Invalid workout")
        raise SystemExit(err)
    except requests.RequestException as err:
        messagebox.showinfo(title=f"Error", message="Invalid workout")
        raise SystemExit(err)
    else:
        result = response.json()

        today = dt.datetime.now()
        date = today.strftime("%d/%m/%Y")
        time = today.strftime("%H:%M:%S")

        # Basic Authentication (Alternative)
        # auth_data = (YOUR_USERNAME, YOUR_PASSWORD)
        #    response = requests.post(url=SHEETY_ENDPOINT, json=workout_params, auth=auth_data)

        #-----------------------------------------Place into class---------------------------------------------
        sheet_header = {
            "Authorization": AUTHENTICATION_TOKEN
        }

        for exercise in result.get("exercises"):
            workout_params = {
                "workout": {
                    "date": date,
                    "time": time,
                    "exercise": exercise["name"].title(),
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"]
                }
            }
            try:
                response = requests.post(url=SHEET_API_ENDPOINT, json=workout_params, headers=sheet_header)
                print(response.raise_for_status())
            except requests.exceptions.HTTPError as err:
                messagebox.showinfo(title="Error", message=f"{err}")
                set_notification_color(False)
                return
                # raise SystemExit(err)
            except requests.RequestException as err:
                messagebox.showinfo(title="Error", message=f"{err}")
                set_notification_color(False)
                return
                # raise SystemExit(err)
            else:
                set_notification_color(True)
                messagebox.showinfo(title="Workout saved", message=f"Date: {date}\nTime: {time}\nExercise: {exercise['name'].title()}\nDuration: {exercise['duration_min']}\n Calories: {exercise['nf_calories']}")
                input_box.delete(0, END)


def load_personal_stats():
    try:
        with open("personal_data.json", "r") as save_data:
            try:
                result = json.load(save_data)
            except:
                result = get_save_structure()
                save_stats()

    except FileNotFoundError:
        with open("personal_data.json", "w") as save_data:
            json.dump(get_save_structure(), save_data, indent=4)
    else:
        data = result["data"]
        set_personal_data(data["gender"], data["weight"], data["height"], data["age"])


def save_stats():
    try:
        with open("personal_data.json", "w") as save_data:
            temp_data = get_save_structure(_gender=gender_selection.get(),
                                           _weight=weight_input_box.get(),
                                           _height=height_input_box.get(),
                                           _age=age_input_box.get())
            json.dump(temp_data, save_data, indent=4)
    except FileNotFoundError:
        print("Error: File not found")
    else:
        print("Data saved")


def get_save_structure(_gender="~", _weight="", _height="", _age=""):
    save_structure = {
        "data": {
            "gender": _gender,
            "weight": _weight,
            "height": _height,
            "age": _age
        }
    }
    return save_structure


def set_personal_data(_gender, _weight, _height, _age):
    global gender_selection, weight_input_box, height_input_box, age_input_box

    if _gender == "":
        gender_selection.current(0)
    elif _gender == "male":
        gender_selection.current(1)
    else:
        gender_selection.current(2)

    weight_input_box.insert(0, _weight)
    height_input_box.insert(0, _height)
    age_input_box.insert(0, _age)


def set_notification_color(was_added):
    if was_added:
        added_notification_label.config(text="Workout added", fg="black")

    else:
        added_notification_label.config(text="Failed to add workout", fg="black")


window = Tk()
window.title("Exercise Record")
window.config(pady=5, padx=5, bg="light blue")

title_label = Label(text="Enter workout/s:", bg="light blue")
title_label.grid(row=1, column=0)

input_box = Entry(width=35)
input_box.grid(row=2, column=0, pady=10)

confirm_button = Button(text="Add workouts", command=add_workout)
confirm_button.grid(row=3, column=0)

added_notification_label = Label(text="Success", bg="light blue", fg="light blue")
added_notification_label.grid(row=4, column=0, columnspan=2)

note_label = Label(text="Write workouts naturally: I have ran 20 minutes and/or walked 13km.", bg="light blue", wraplength=280, justify="center")
note_label.grid(row=5, column=0, columnspan=2, pady=5)

canvas = Canvas(height=50, width=250)
nutrition_image = PhotoImage(file="NutritionixAPI_hires_flat.png")
nutrition_image = nutrition_image.subsample(10)
canvas.create_image(120, 25, image=nutrition_image)
# canvas.scale(nutrition_image, 1, 1, 0.3, 0.3)
canvas.grid(row=8, column=0, columnspan=3, rowspan=2)

# User personal data
gender_label = Label(text="Gender:", bg="light blue")
gender_label.grid(row=1, column=3)

gender_selection = tkinter.ttk.Combobox(width=10, state="readonly")
gender_selection["values"] = ("~", "male", "female")
gender_selection.current(0)
gender_selection.grid(row=2, column=3)

weight_label = Label(text="Weight (KG):", bg="light blue")
weight_label.grid(row=3, column=3)

weight_input_box = Entry(width=10)
weight_input_box.grid(row=4, column=3)

height_label = Label(text="Height (CM):", bg="light blue")
height_label.grid(row=5, column=3)

height_input_box = Entry(width=10)
height_input_box.grid(row=6, column=3)

age_label = Label(text="Age:", bg="light blue")
age_label.grid(row=7, column=3)

age_input_box = Entry(width=10)
age_input_box.grid(row=8, column=3)

confirm_button = Button(text="Save", command=save_stats)
confirm_button.grid(row=9, column=3)

load_personal_stats()

window.mainloop()

# exercise = input("Tell me what exercise you did: ")
#
# #-----------------------------------------Place into class---------------------------------------------
# header = {
#     "x-app-id":  APP_ID,
#     "x-app-key": APP_API,
# }
#
# signin_params = {
#     "password": "redfern1155@gmail.com",
#     "email": "!Allnewfern2678!"
# }
#
# exercise_config = {
#     "query": exercise,
#     "gender": GENDER,
#     "weight_kg": WEIGHT_KG,
#     "height_cm": HEIGHT_CM,
#     "age": AGE
# }
#
# response = requests.post(url=NUTRITIONIX_API_ENDPOINT, json=exercise_config, headers=header)
# result = response.json()
#
# today = dt.datetime.now()
# date = today.strftime("%d/%m/%Y")
# time = today.strftime("%H:%M:%S")
#
# # Basic Authentication (Alternative)
# # auth_data = (YOUR_USERNAME, YOUR_PASSWORD)
# #    response = requests.post(url=SHEETY_ENDPOINT, json=workout_params, auth=auth_data)
#
# #-----------------------------------------Place into class---------------------------------------------
# sheet_header = {
#     "Authorization": AUTHENTICATION_TOKEN
# }
#
# for exercise in result.get("exercises"):
#     workout_params = {
#         "workout": {
#             "date": date,
#             "time": time,
#             "exercise": exercise["name"].title(),
#             "duration": exercise["duration_min"],
#             "calories": exercise["nf_calories"]
#         }
#     }
#
#     response = requests.post(url=SHEET_API_ENDPOINT, json=workout_params, headers=sheet_header)
#     result = response.json()
