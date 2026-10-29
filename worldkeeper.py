import tkinter as tk

window = tk.Tk()
window.title("Worldkeeper")
window.geometry("600x400")

title = tk.Label(window, text="Welcome to Worldkeeper", font=("Arial", 20))
title.pack(pady=40)

window.mainloop()