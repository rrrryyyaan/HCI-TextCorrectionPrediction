import tkinter as tk
import requests
import time
from tkinter import scrolledtext
from tkinter import messagebox

"""
    File Name: Main.py
    Author: Ryan Bell & Sam Woodworth
    Date Created: 4/19/2021
    Date Last Modified: 4/19/2021
    Python Version: 3.8.5
"""

DICTIONARY_URL = "https://www.dictionary.com/browse/"
MERRIAM_URL = "https://www.merriam-webster.com/dictionary/"


def init_gui(window):
    """Initializes the Graphical User Interface that are static"""

    #Title above the word entry box
    word_title = tk.Label(window, text="Start Typing For Text Prediction:", bg="#272626", fg="#ffffff", font=("Arial", 11))
    word_title.grid(row=0, columnspan=2, sticky="w e")

    word_title = tk.Label(window, text="Paste Text To Be Corrected:", bg="#272626", fg="#ffffff", font=("Arial", 11))
    word_title.grid(row=2, columnspan=2, sticky="w e")

    word_title = tk.Label(window, text="Corrected Text:", bg="#272626", fg="#ffffff", font=("Arial", 11))
    word_title.grid(row=5, columnspan=2, sticky="w e")
    
    correct_button = tk.Button(window, text="Correct", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", width=20, command= lambda: correct_text(text_entry.get()))
    correct_button.grid(row=4, columnspan=2, sticky="w")

    #Clear button to clear various texts on the gui
    clear_button = tk.Button(window, text="Clear", bd=3, bg="#4e89bf", fg="#000000", activebackground="#2b5072", width=20, command=clear)
    clear_button.grid(row=4, columnspan=2, sticky="e")


def clear():
    """Clears the definition title, definition, and word entry input"""
    text_entry.delete(1.0, 'end')
    text_corrected_entry.delete(1.0, 'end')


def handle_button(dictionary):
    """Handles the buttons clicked"""
    global dictionary_selected
    dictionary_selected = dictionary



def correct_text(word):
    lit = "lit"

#         #Clears the whole scrollbox where the definition is displayed
#         definition_display.delete(1.0, "end")

#         #Update the current wording being searched label
#         definition_title.configure(text="Definition for " + word + ":")

#         #Display the adverb and definition to the current word searched on the scrollbox
#         definition_display.insert(1.0, adverb + "\n- " + definition)
#     except:
#         #Clears the whole scrollbox where the definition is displayed
#         definition_display.delete(1.0, 'end')

#         #Update the current wording being searched label
#         definition_title.configure(text="Definition for :")

#         #Show an error box because word can't be found
#         messagebox.showerror("Error!", "Word not found!\nPlease check your spelling.")


if __name__ == '__main__':

    input_text_prediction = ""
    input_text_correction = ""

    #Initialize the tkinter gui
    window = tk.Tk()
    window.title("Text Correction & Prediction")
    window.configure(bg="#272626")

    prediction_entry = tk.Entry(window, textvariable=input_text_prediction, bd=1, bg="#272626", fg="#ffffff", selectforeground="#ffffff")
    prediction_entry.grid(row=1, columnspan=2, pady=3, sticky="w e")
    prediction_entry.focus()

    text_entry = scrolledtext.ScrolledText(window, bg="#272626", fg="#ffffff", bd=1, width=34, height=10)
    text_entry.grid(row=3, columnspan=2, pady=6)

    text_corrected_entry = scrolledtext.ScrolledText(window, bg="#272626", fg="#ffffff", bd=1, width=34, height=10)
    text_corrected_entry.grid(row=6, columnspan=2)

    #Initialize the static gui
    init_gui(window)

    #Loop for the gui
    window.mainloop()