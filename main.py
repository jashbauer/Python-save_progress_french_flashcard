from tkinter import *
from tkinter import messagebox
import csv
import random

# ------------------------ CONSTANTS ---------------------------------------
BACKGROUND = "#B1DDC6"
FONT_SIZE = 40
FONT_NAME = "arial"
FONT_TYPE = "italic"

# ----------------------- GAME MODE MESSAGE BOX ----------------------------
game_mode = messagebox.askyesno(title="Game Mode",
                                message="Use Unknown Words Data? (y / n = Full set of words)")

# Importing word data as a list of dictionaries
if game_mode:
    try:
        with open("./data/unknown_words.csv", mode="r", encoding="utf-8") as file:
            words = csv.DictReader(file)
            WORDS_LIST = []
            for key in words:
                WORDS_LIST.append(key)
    except FileNotFoundError:
        messagebox.showwarning(title="Data Warning", message="Unknown Words data not found!\n"
                                                             "Using full set of words.")
        with open("./data/french_words.csv", mode="r", encoding="utf-8") as file:
            words = csv.DictReader(file)
            WORDS_LIST = []
            for key in words:
                WORDS_LIST.append(key)

else:
    with open("./data/french_words.csv", mode="r", encoding="utf-8") as file:
        words = csv.DictReader(file)
        WORDS_LIST = []
        for key in words:
            WORDS_LIST.append(key)

# ------------------------ FUNCTIONS ---------------------------------------


def next_card_unknown():
    global flip_timer
    window.after_cancel(flip_timer)

    try:
        random_word = random.choice(WORDS_LIST)
        word_canvas.itemconfig(card_face, image=card_front)
        word_canvas.itemconfig(title_text, text="French", fill="black")
        word_canvas.itemconfig(word_text, text=random_word["French"], fill="black")

        flip_timer = window.after(3000, flip_card, random_word)
        return random_word
    except IndexError:
        messagebox.showinfo(title="Congratulations!",
                            message="There are no more words in this list for you to learn!")


def next_card_known():
    word_to_remove = next_card_unknown()
    global WORDS_LIST
    try:
        WORDS_LIST.remove(word_to_remove)
    except ValueError:
        pass


def flip_card(word):
    word_canvas.itemconfig(card_face, image=card_back)
    word_canvas.itemconfig(title_text, text="English", fill="white")
    word_canvas.itemconfig(word_text, text=word["English"], fill="white")


# ------------------------ WINDOW SETUP ------------------------------------
window = Tk()
window.title("L'éclat")
window.config(width=800, height=576, padx=50, pady=50, bg=BACKGROUND)

flip_timer = window.after(3000, func=flip_card)

# ----------------------- IMAGES and CANVAS ---------------------------------
card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")
right_icon = PhotoImage(file="./images/right.png")
wrong_icon = PhotoImage(file="./images/wrong.png")


# Canvas griding
word_canvas = Canvas(width=800, height=576, bg=BACKGROUND, highlightthickness=0)
word_canvas.grid(row=1, column=1, columnspan=2)
card_face = word_canvas.create_image(400, 260, image=card_front)

title_text = word_canvas.create_text(400, 150, text="Title", font=(FONT_NAME, FONT_SIZE, FONT_TYPE))
word_text = word_canvas.create_text(400, 263, text="word", font=(FONT_NAME, FONT_SIZE, "bold"))


# ----------------------- BUTTONS ---------------------------------------------
right_button = Button(image=right_icon, highlightthickness=0, command=next_card_known)
right_button.grid(row=2, column=1)

wrong_button = Button(image=wrong_icon, highlightthickness=0, command=next_card_unknown)
wrong_button.grid(row=2, column=2)

next_card_unknown()

window.mainloop()

# -------------------- SAVE DATA MESSAGE BOX ------------------------------------------------
save_data = messagebox.askyesno(title="Save Data?",
                                message="Do you wish to save your progress?")
# -------------------- SAVE UNKNOWN WORDS INTO A CSV -----------------------------------------
if save_data:
    columns = ["French", "English"]
    with open("./data/unknown_words.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for key in WORDS_LIST:
            writer.writerow(key)
