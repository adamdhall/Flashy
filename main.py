from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

french_data = pd.read_csv("data/french_words.csv")
card_data = french_data.to_dict(orient="records")

current_card = {}



def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card_background, image=card_front_img)
    current_card = random.choice(card_data)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_card["French"])
    canvas.itemconfig(card_title, fill="black")
    canvas.itemconfig(card_word, fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card["English"])
    canvas.itemconfig(card_title, fill="white")
    canvas.itemconfig(card_word, fill="white")


def remove_word():
    to_learn.remove(current_card)
    new_card()
    data = pd.DataFrame(to_learn)
    data.to_csv("Data/words_to_learn.csv", index=False)



window=Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, func=flip_card)

try:
    data=pd.read_csv("Data/french_words.csv")
except FileNotFoundError:
    window.messagebox.showinfo(title="Error",text="Words to learn file does not exist")
else:
    to_learn=data.to_dict(orient="records")

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_button_img = PhotoImage(file="images/right.png")
wrong_button_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(height=526, width=800)
card_background=canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 180, text="Title", font=("Arial", 25, "italic"))
card_word = canvas.create_text(400, 261, text="word", font= ("Arial", 42, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


correct=Button(image=right_button_img, highlightthickness=0, command= remove_word)
correct.grid(row=1, column=1)

incorrect=Button(image=wrong_button_img, highlightthickness=0, command=new_card)
incorrect.grid(row=1, column=0)

new_card()
window.mainloop()