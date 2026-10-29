import tkinter as tk

# The list of characters lives here. Each character is a small record with a name and a description.
characters = []

window = tk.Tk()
window.title("Worldkeeper")
window.geometry("700x500")

# The menu bar sits at the top of every screen.
menu_bar = tk.Frame(window, bg="#e8e8e8")
menu_bar.pack(fill="x")

# The area below the menu bar where screens get swapped in and out.
content = tk.Frame(window)
content.pack(fill="both", expand=True)


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
    tk.Button(content, text="Add Character", command=show_add_character).pack(anchor="e", padx=40)
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
        show_character_list()


tk.Label(menu_bar, text="Worldkeeper", font=("Arial", 12, "bold"), bg="#e8e8e8").pack(side="left", padx=10, pady=5)
tk.Button(menu_bar, text="Characters", command=show_character_list).pack(side="right", padx=5, pady=5)
tk.Button(menu_bar, text="Home", command=show_welcome).pack(side="right", padx=5, pady=5)

show_welcome()
window.mainloop()