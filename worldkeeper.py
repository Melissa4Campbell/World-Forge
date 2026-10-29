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
window.geometry("720x580")
window.minsize(720, 580)

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


def handle_key(event):
    # Saves the characters when Ctrl+S is pressed. Windows reports the Control key as the number 4.
    if event.state & 4 and event.keysym.lower() == "s":
        save_characters()


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


def add_info_box(parent, heading, lines, wrap):
    # Builds one box with a bold heading and a few lines of text underneath.
    box = tk.LabelFrame(parent, text=heading, font=("Arial", 11, "bold"), padx=10, pady=5)
    box.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    for line in lines:
        tk.Label(box, text=line, wraplength=wrap, justify="left", anchor="w").pack(anchor="w", pady=2)


def show_welcome():
    # Shows the Welcome screen (screen 1). It explains the benefits, the costs, and the steps.
    clear_screen()
    tk.Label(content, text="Welcome to Worldkeeper", font=("Arial", 20)).pack(pady=(20, 0))
    tk.Label(content, text="A notebook for the people in your fantasy world.").pack(pady=(0, 10))
    boxes = tk.Frame(content)
    boxes.pack(fill="x", padx=15)
    add_info_box(boxes, "What it does for you", [
        "Keeps every character's name and description in one place.",
        "Lets you find any detail in seconds instead of digging through scattered notes.",
        "Gives you more time to write."], 290)
    add_info_box(boxes, "What it costs you", [
        "Nothing. It is free and needs no account.",
        "Characters are saved only in a file on this computer. Nothing is uploaded.",
        "Adding your first character takes about 2 minutes."], 290)
    steps = tk.Frame(content)
    steps.pack(fill="x", padx=15)
    add_info_box(steps, "How it works", [
        "Step 1: Click Add Character, then type a name and a description.",
        "Step 2: Check your list. Click a name to read its description.",
        "Step 3: Click Save so your characters are here next time."], 640)
    tk.Button(content, text="Go to My Characters", command=show_character_list).pack(pady=10)
    tk.Label(content, text="Already know your way around? Click Characters in the menu above to skip this page.").pack()


def show_names():
    # Shows every character's name in the order they were added. Clicking a name opens its details.
    for character in characters:
        tk.Button(content, text=character["name"], font=("Arial", 14), relief="flat", anchor="w",
                  fg="#1a4fa3", cursor="hand2",
                  command=lambda c=character: show_details(c)).pack(anchor="w", padx=40, pady=2)
    tk.Label(content, text="Click a name to see its description.").pack(anchor="w", padx=40, pady=10)


def show_empty_message():
    # Tells the writer there are no characters yet and shows three steps to get started.
    tk.Label(content, text="No characters yet.", font=("Arial", 14)).pack(pady=(10, 0))
    tk.Label(content, text="Get started in 3 steps:", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(content, text="1. Click Add Character (top right).").pack()
    tk.Label(content, text="2. Type a name and a description, then click Add Character.").pack()
    tk.Label(content, text="3. Click Save so your characters are here next time.").pack()


def show_details(character):
    # Shows the Character Details screen (screen 4) with the full description of one character.
    clear_screen()
    tk.Button(content, text="\u2039 Back to Characters", relief="flat", fg="#1a4fa3", cursor="hand2",
              command=show_character_list).pack(anchor="w", padx=30, pady=10)
    tk.Label(content, text=character["name"], font=("Arial", 20)).pack(anchor="w", padx=40)
    tk.Label(content, text="DESCRIPTION", font=("Arial", 10, "bold")).pack(anchor="w", padx=40, pady=(15, 0))
    description = character["description"] or "No description was added."
    tk.Label(content, text=description, wraplength=600, justify="left").pack(anchor="w", padx=40, pady=5)
    tk.Label(content, text="Click Back to Characters to return to your list.").pack(anchor="w", padx=40, pady=20)


def show_character_list():
    # Shows the Character List screen (screen 2).
    clear_screen()
    tk.Label(content, text="My Characters", font=("Arial", 20)).pack(pady=20)
    buttons = tk.Frame(content)
    buttons.pack(anchor="e", padx=40)
    tk.Button(buttons, text="\U0001F4BE Save", command=save_characters).pack(side="left", padx=5)
    tk.Button(buttons, text="+ Add Character", bg="#1a4fa3", fg="white",
              command=show_add_character).pack(side="left")
    tk.Label(content, text="Save not working? Press Ctrl+S.").pack(anchor="e", padx=40)
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

window.bind("<Key>", handle_key)
show_welcome()
load_characters()
update_status(True)
window.mainloop()