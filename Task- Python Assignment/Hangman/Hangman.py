import random
def load_words():
    file=open("Task- Python Assignment\Hangman\words.txt", "r")
    words=[]
    
    for line in file:
        words.append(line.strip().upper())
    file.close()
    return words

def choose_word(words):
    return random.choice(words)

def play_game():
    words = load_words()
    word = choose_word(words)
    guessed_letters = []
    chances = 6
    print("Welcome to Hangman!")
    while chances > 0:
        display = ""
        for letter in word:
            if letter in guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        print(display)
        if "_" not in display:
            print("Congratulations! You guessed the word:", word)
            return
        guess = input("Guess your letter: ").upper()
        if guess in guessed_letters:
            print("You already guessed that letter!")
            continue
        guessed_letters.append(guess)
        if guess not in word:
            chances -= 1
            print("Incorrect!")
            print("You have", chances, "chances left.")
    print("You lost!")
    print("The word was:", word)


while True:
    play_game()
    choice = input("Play again? (y/n): ")
    if choice.lower() != 'y':
        break