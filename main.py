from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
canvas = Canvas(width=800, height=528, bg=BACKGROUND_COLOR, highlightthickness=0)

# french word randomizer
french_words = pandas.read_csv("data/french_words.csv")
french_dict = french_words.to_dict(orient="records")
french_initial = random.choice(french_dict)
french_start = french_initial["French"]
english_start = french_initial["English"]

print(type(french_dict))
chosen_dict = {}

# csv file for words to learn
words_to_learn_df = pandas.DataFrame(french_words)
words_to_learn = words_to_learn_df.to_dict(orient="records")
print(words_to_learn_df)

# removing function for right button
chosen_entry = {}


def french_random_right():
    global chosen_dict, flip_timer, chosen_entry
    window.after_cancel(flip_timer)
    try:
        words_to_learn.remove(chosen_entry)
    except ValueError or IndexError:
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(language_text, text="Congrats!", fill="black")
        canvas.itemconfig(word_text, text="You learned all the French words", fill="black", font=("Arial", 30, "bold"))
    else:
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(language_text, text="French", fill="black")
        try:
            french_word_in_dict = random.choice(words_to_learn)
        except IndexError:
            pass
        else:
            while chosen_entry == french_word_in_dict:
                french_word_in_dict = random.choice(words_to_learn)
            chosen_entry = french_word_in_dict
            chosen_dict = french_word_in_dict
            french_chosen = french_word_in_dict["French"]
            canvas.itemconfig(word_text, text=french_chosen, fill="black")
            flip_timer = window.after(3000, flip_card)
            print(len(words_to_learn))


def french_random_wrong():
    global chosen_dict, flip_timer, chosen_entry
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(language_text, text="French", fill="black")
    french_word_in_dict = random.choice(words_to_learn)

    while chosen_entry == french_word_in_dict and len(words_to_learn) > 1:
        french_word_in_dict = random.choice(words_to_learn)
    chosen_entry = french_word_in_dict
    chosen_dict = french_word_in_dict
    french_chosen = french_word_in_dict["French"]
    canvas.itemconfig(word_text, text=french_chosen, fill="black")
    flip_timer = window.after(3000, flip_card)
    print(len(words_to_learn))


def flip_card():
    global chosen_dict
    canvas.itemconfig(canvas_image, image=card_back)
    english_chosen = chosen_dict["English"]
    canvas.itemconfig(word_text, text=english_chosen, fill="white")
    canvas.itemconfig(language_text, text="English", fill="white")


def start():
    global chosen_dict, chosen_entry
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(language_text, text="French", fill="black")
    french_word_in_dict = random.choice(french_dict)
    chosen_entry = french_word_in_dict
    chosen_dict = french_word_in_dict
    french_chosen = french_word_in_dict["French"]
    canvas.itemconfig(word_text, text=french_chosen, fill="black")


# load images
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 264, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
language_text = canvas.create_text(400, 150, text="French", fill="black", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text=french_start, fill="black",
                               font=("Arial", 60, "bold"))

# Buttons
right_button = Button(image=right_image, highlightthickness=0, command=french_random_right)
right_button.grid(column=1, row=1)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=french_random_wrong)
wrong_button.grid(column=0, row=1)

start()
flip_timer = window.after(3000, flip_card)
window.mainloop()
