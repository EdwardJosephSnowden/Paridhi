import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
from ttkthemes import ThemedStyle
import csv
import pyttsx3

def load_country_timezones(filename):
    country_timezones = {}
    valid_timezones = set(pytz.all_timezones)
    
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 2:
                country_name, timezone = row
                if timezone in valid_timezones:
                    country_timezones[country_name] = timezone
                else:
                    print(f"Invalid timezone '{timezone}' for country '{country_name}'")
   
    return country_timezones

def update_clock():
    selected_country = country_var.get()
    timezone = pytz.timezone(country_timezones[selected_country])
    current_time = datetime.now(timezone)
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    search_label.config(text=f"Time In {selected_country} is -", anchor="center", justify="center")
    time_label_time.config(text=time_str, anchor="center", justify="center")
    root.after(1000, update_clock)

def on_country_select(event):
    selected_country = country_var.get()
    timezone = pytz.timezone(country_timezones[selected_country])
    current_time = datetime.now(timezone)
    tim = current_time.strftime("%Y-%m-%d %H:%M:%S")
    saytime = f"Time in {selected_country} is {tim}"
    update_clock()
    speak(saytime)

def speak(text):
    engine.say(text)
    engine.runAndWait()

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
update_clock()
country_menu.bind("<<ComboboxSelected>>", on_country_select)

current_time = datetime.now(pytz.timezone(country_timezones[country_var.get()]))
tim = current_time.strftime("%Y-%m-%d %H:%M:%S")
saytime = f"Time in {country_var.get()} is {tim}"

speak(saytime)
root.mainloop()