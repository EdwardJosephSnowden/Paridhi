import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
import csv
import pyttsx3
import threading
from ttkthemes import ThemedStyle

def load_country_timezones(filename):
    country_timezones = {}
    valid_timezones = set(pytz.all_timezones)

    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            country_name = row.get('Country')
            timezone = row.get('Timezone')
            if country_name and timezone.strip() in valid_timezones:
                country_timezones[country_name] = timezone.strip()
            else:
                print(f"Invalid data in CSV: {row}")

    return country_timezones

def update_clock():
    selected_country = country_var.get()
    try:
        timezone = pytz.timezone(country_timezones[selected_country])
    except KeyError:
        print(f"Error: Timezone not found for {selected_country}")
        return

    current_time = datetime.now(timezone)
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    search_label.config(text=f"Time In {selected_country} is -", anchor="center", justify="center")
    time_label_time.config(text=time_str, anchor="center", justify="center")
    root.after(1000, update_clock)

def on_country_select(event):
    selected_country = country_var.get()
    try:
        timezone = pytz.timezone(country_timezones[selected_country])
    except KeyError:
        print(f"Error: Timezone not found for {selected_country}")
        return

    current_time = datetime.now(timezone)
    tim = current_time.strftime("%Y-%m-%d %H:%M:%S")
    saytime = f"Time in {selected_country} is {tim}"
    update_clock()
    speak_in_thread(saytime)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_in_thread(text):
    # Check if the engine is already running
    if not engine._inLoop:
        # Start the engine only if it's not already running
        engine.runAndWait()
    else:
        print("The engine is already running.")

    thread = threading.Thread(target=speak, args=(text,))
    thread.start()

engine = pyttsx3.init()
zira_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', zira_voice_id)
engine.setProperty('rate', 150)

root = tk.Tk()
root.title("World Clock")
root.geometry("800x400")

style = ThemedStyle(root)
style.set_theme("plastik")

country_var = tk.StringVar(root)
search_label = ttk.Label(root, text="Select a country:", font=("Helvetica", 14))
search_label.pack(pady=10)

country_timezones = load_country_timezones("country.csv")

country_menu = ttk.Combobox(root, textvariable=country_var, values=list(country_timezones.keys()), state="readonly")
country_menu.pack(pady=10)

time_label_time = ttk.Label(root, text="", font=("Helvetica", 36))
time_label_time.pack(pady=20)

country_var.set("India")

initial_country = country_var.get()
initial_timezone = country_timezones.get(initial_country)

if initial_timezone:
    current_time = datetime.now(pytz.timezone(initial_timezone))
    tim = current_time.strftime("%Y-%m-%d %H:%M:%S")
    saytime = f"Time in {initial_country} is {tim}"
    speak_in_thread(saytime)
else:
    print(f"Error: Timezone not found for {initial_country}")

update_clock()
country_menu.bind("<<ComboboxSelected>>", on_country_select)

root.mainloop()
