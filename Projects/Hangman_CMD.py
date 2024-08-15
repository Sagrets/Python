import requests
import random

# Fetch the list of words
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()
WORDS = [word.decode('utf-8') for word in WORDS]

# Select a random word from the list
answer = random.choice(WORDS)

# Initialize game state
guesses = 6
display = ['_' for _ in answer]  # Display underscores for unguessed letters
used_letters = set()

# Game loop
while guesses > 0 and '_' in display:
    print('Current word:', ' '.join(display))
    guess = input('Guess a letter:').lower()

    # Check if input is valid
    if not guess.isalpha() or len(guess) != 1:
        print('Please enter a valid letter.')
        continue

    # Check if letter has already been guessed
    if guess in used_letters:
        print('You have already guessed that letter.')
        continue
    used_letters.add(guess)

    # Process the guess
    if guess in answer:
        print('Correct!')
        # Reveal the letter in the display
        for index, letter in enumerate(answer):
            if letter == guess:
                display[index] = letter
    else:
        guesses -= 1
        print('Wrong. You have', guesses, 'guesses left.')

# Game end messages
if '_' not in display:
    print('Congratulations! You guessed the word:', answer)
else:
    print('You lose, please play again. The word was:', answer)
