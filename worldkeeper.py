import tkinter as tk

# The list of characters lives here. Each character will have a name and a description.
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


def show_character_list():
    # Shows the Character List screen (screen 2).
    clear_screen()
    tk.Label(content, text="My Characters", font=("Arial", 20)).pack(pady=40)


tk.Label(menu_bar, text="Worldkeeper", font=("Arial", 12, "bold")).pack(side="left", padx=10, pady=5)
tk.Button(menu_bar, text="Characters", command=show_character_list).pack(side="right", padx=5, pady=5)
tk.Button(menu_bar, text="Home", command=show_welcome).pack(side="right", padx=5, pady=5)

show_welcome()
window.mainloop()