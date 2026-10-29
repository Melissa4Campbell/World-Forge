import json
import os
import tkinter as tk
from tkinter import messagebox

# The save file lives in the same folder as this program, so it is always found.
FOLDER = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(FOLDER, "worldkeeper_data.json")
DAMAGED_FILE = os.path.join(FOLDER, "worldkeeper_data_damaged.json")

# The list of characters lives here. Each character is a small record with a name and a description.
characters = []

window = tk.Tk()
window.title("Worldkeeper")
window.geometry("700x500")

# The menu bar sits at the top of every screen.
menu_bar = tk.Frame(window, bg="#e8e8e8")
menu_bar.pack(fill="x")

# The status bar sits at the bottom of every screen and shows the save status and character count.
status_bar = tk.Label(window, text="", anchor="w", bg="#e8e8e8")
status_bar.pack(side="bottom", fill="x")

# The area between the two bars where screens get swapped in and out.
content = tk.Frame(window)
content.pack(fill="both", expand=True)


def update_status(saved):
    # Updates the bar at the bottom with the save status and the number of characters.
    state = "All changes saved" if saved else "Unsaved changes"
    count = len(characters)
    word = "character" if count == 1 else "characters"
    status_bar.config(text=state + "     " + str(count) + " " + word)


def save_characters():
    # Writes every character to the save file on this computer.
    with open(SAVE_FILE, "w", encoding="utf8") as file:
        json.dump(characters, file, indent=2, ensure_ascii=False)
    update_status(True)


def is_valid(data):
    # Checks that loaded data is a list of characters that each have a name and a description.
    if not isinstance(data, list):
        return False
    for item in data:
        if not isinstance(item, dict) or "name" not in item or "description" not in item:
            return False
    return True


def handle_damaged_file():
    # Keeps a copy of the damaged file and tells the writer, so the program opens empty instead of crashing.
    os.replace(SAVE_FILE, DAMAGED_FILE)
    messagebox.showinfo(
        "Your save file could not be read",
        "Worldkeeper could not open worldkeeper_data.json, so it started with an empty list. "
        "A copy of the damaged file was kept as worldkeeper_data_damaged.json.")


def load_characters():
    # Loads saved characters when the program opens. If there is no file, the list stays empty.
    if not os.path.exists(SAVE_FILE):
        return
    try:
        with open(SAVE_FILE, "r", encoding="utf8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        data = None
    if is_valid(data):
        characters.extend(data)
    else:
        handle_damaged_file()


def clear_screen():
    # Removes everything from the content area so a new screen can be shown.
    for widget in content.winfo_children():
        widget.destroy()


def show_welcome():
    # Shows the Welcome screen (screen 1).
    clear_screen()
    tk.Label(content, text="Welcome to Worldkeeper", font=("Arial", 20)).pack(pady=40)


def show_names():
    # Shows the name of every character, in the order they were added.
    for character in characters:
        tk.Label(content, text=character["name"], font=("Arial", 14)).pack(anchor="w", padx=40, pady=2)


def show_empty_message():
    # Tells the writer there are no characters yet.
    tk.Label(content, text="No characters yet.", font=("Arial", 14)).pack(pady=10)


def show_character_list():
    # Shows the Character List screen (screen 2).
    clear_screen()
    tk.Label(content, text="My Characters", font=("Arial", 20)).pack(pady=20)
    buttons = tk.Frame(content)
    buttons.pack(anchor="e", padx=40)
    tk.Button(buttons, text="Save", command=save_characters).pack(side="left", padx=5)
    tk.Button(buttons, text="Add Character", command=show_add_character).pack(side="left")
    if len(characters) == 0:
        show_empty_message()
    else:
        show_names()


def show_add_character():
    # Shows the Add Character screen (screen 5).
    clear_screen()
    tk.Label(content, text="Add Character", font=("Arial", 20)).pack(pady=20)
    tk.Label(content, text="Step 1: Type a name (required)").pack(anchor="w", padx=40)
    name_box = tk.Entry(content, width=50)
    name_box.pack(anchor="w", padx=40, pady=5)
    error_label = tk.Label(content, text="", fg="red")
    error_label.pack(anchor="w", padx=40)
    tk.Label(content, text="Step 2: Type a description").pack(anchor="w", padx=40)
    description_box = tk.Text(content, width=50, height=6)
    description_box.pack(anchor="w", padx=40, pady=5)
    tk.Label(content, text="Step 3: Click Add Character when you are done.").pack(anchor="w", padx=40)
    tk.Button(content, text="Add Character",
              command=lambda: add_character(name_box, description_box, error_label)).pack(anchor="w", padx=40, pady=10)


def add_character(name_box, description_box, error_label):
    # Adds the new character to the list. If the name is blank, shows a message instead.
    name = name_box.get().strip()
    description = description_box.get("1.0", "end").strip()
    if name == "":
        error_label.config(text="A name is required. Please type a name for your character.")
    else:
        characters.append({"name": name, "description": description})
        update_status(False)
        show_character_list()


tk.Label(menu_bar, text="Worldkeeper", font=("Arial", 12, "bold"), bg="#e8e8e8").pack(side="left", padx=10, pady=5)
tk.Button(menu_bar, text="Characters", command=show_character_list).pack(side="right", padx=5, pady=5)
tk.Button(menu_bar, text="Home", command=show_welcome).pack(side="right", padx=5, pady=5)

show_welcome()
load_characters()
update_status(True)
window.mainloop()