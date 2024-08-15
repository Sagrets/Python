import tkinter as tk
import requests
import random

# Fetch the list of words
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()
WORDS = [word.decode('utf-8') for word in WORDS]
    
# Select a random word from the list
answer = random.choice(WORDS)
guessed_letters = set()
display = ['_ ' for _ in answer]
lbl_word = None
graphic_list = [
    """
    -----
    |   |
        |
        |
        |
        |
      ------ 
    """, 
    """
    -----
    |   |
    0   |
        |
        |
        |
     ------
   """,
    """
    -----
    |   |
    0   |
    |   |
        |
        |
      ------ 
    """,
    """
    -----
    |   |
    0   |
   /|   |
        |
        |
      ------
    """,
    """
    -----
    |   |
    0   |
   /|\\ |
        |
        |
      ------ 
    """,
    """
     -----
     |   |
     0   |
    /|\\ |
     |   |
         |
      ------
    """,
    """
    -----
    |   |
    0   |
   /|\\ |
    |   |
     \\ |
      ------ 
    """,
    """
     -----
    |    |
    0    |
   /|\\  |
    |    |
   / \\  |
         |
       ------
    """
    ]
current_graphic = graphic_list[0]

#Hangman Graphic
def graphic_update(n):
    global graphic_pic
    current_graphic = graphic_list[n]
    graphic_pic.config(text=current_graphic)

def guess(letter):
    global display, response_label, answer, guessed_letters
    letter = letter.lower()
    
    # Check if input is valid
    if not letter.isalpha() or len(letter) != 1:
        response_label.config(text='Please enter a valid letter.')
        return
    
    # Check if letter has already been guessed
    if letter in guessed_letters or letter in display:
        response_label.config(text='You have already guessed that letter.')
        return
    
  # Process the guess
    if letter in answer:
        response_label.config(text='Correct!')
        for index, n in enumerate(answer):
            if n == letter:
                display[index] = letter
    else:
        guessed_letters.add(letter)
        graphic_update(len(guessed_letters))
        response_label.config(text='Wrong!')

    if ''.join(display) == answer:
        answer = random.choice(WORDS)
        display = ['_ ' for _ in answer]
        guessed_letters = set()
        update_display()
        graphic_update(0)
        response_label.config(text='Congratulations, you win!')
        return
    
    if letter not in answer and len(guessed_letters) >= 7:
        answer = random.choice(WORDS)
        display = ['_ ' for _ in answer]
        update_display()
        guessed_letters = set()
        graphic_update(0)
        response_label.config(text='You lose, please play again.')
    else:
        update_display()

def update_display():
    global lbl_word
    lbl_word.config(text=''.join(display))
    guess_bank.config(text=''.join(guessed_letters))


def reset_game():
    global answer, display, guessed_letters, response_label, guess_bank
    answer = random.choice(WORDS)
    display = ['_ ' for _ in answer]
    guessed_letters = set()
    update_display()
    graphic_update(0)
    response_label.config(text='The game has been reset.')
    
def main():
    global window, lbl_word, response_label, guess_bank, graphic_pic
    
    # Create the main window
    window = tk.Tk()
    window.title("Hangman Game")
    window.geometry("400x300")

    graphic_pic = tk.Label(window, text=current_graphic)
    graphic_pic.pack(fill=tk.NONE, expand=False)

    lbl_word = tk.Label(window, text=''.join(display))
    lbl_word.pack(pady=40)

    # Create frames to hold buttons for each line
    frame1 = tk.Frame(window)
    frame1.pack(side='top', pady=5)
    frame2 = tk.Frame(window)
    frame2.pack(side='top', pady=5)

    # Buttons for letters (split along two lines)
    for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
        if i < 13:
            tk.Button(frame1, text=char.upper(), width=6, height=2, relief='raised', command=lambda c=char: guess(c)).pack(side='left')
        else:
            tk.Button(frame2, text=char.upper(), width=6, height=2, relief='raised', command=lambda c=char: guess(c)).pack(side='left')

    reset_button = tk.Button(window, text='Reset', width=20, height=2, relief='raised', command=reset_game)
    reset_button.pack(fill=tk.NONE, expand=False)
    
    response_label = tk.Label(window, text='')
    response_label.pack(fill=tk.NONE, expand=False, pady=(0, 450), side=tk.BOTTOM)

    bank_title = tk.Label(window, text='Your guesses:')
    bank_title.pack(fill=tk.NONE, expand=False, pady=(41), side=tk.TOP)
    guess_bank = tk.Label(window, text=''.join(guessed_letters))
    guess_bank.pack(fill=tk.NONE, expand=False, pady=(0, 40), side=tk.BOTTOM)
    
    window.mainloop()

if __name__ == "__main__":
    main()