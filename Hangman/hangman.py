def print_lives(lives):
    print("("+str(lives) +" mistakes left)")

def game_loop():
    mystery_word_str = "applesauce"
    mystery_word = []
    dashes_word = []

    for i in range(len(mystery_word_str)):
      mystery_word.append(mystery_word_str[i])
      dashes_word.append('_')

    guesses_left = 8
    old_guesses = []
    bad_guesses = []
    valid_guess = True

    while (dashes_word != mystery_word) and (guesses_left > 0):
      valid_guess = False
      for i in range(len(mystery_word)):
        print(dashes_word[i] + " ", end="")
      print_lives(guesses_left)
      print("Bad guesses: ", end="")
      for i in range(len(bad_guesses)):
        print(bad_guesses[i] + " ",end="")
      print()

      g = input("Enter a character")
      if(g.isalpha()):
        if(len(g) == 1):
          valid_guess = True

      if(not valid_guess):
        print("Please enter a character")

      if (valid_guess):
        if(g in old_guesses):
          print("You've already guessed this letter")
        else:
          old_guesses.append(g)
          if(g in mystery_word):
            for i in range(len(mystery_word)):
              if (mystery_word[i] == g):
                dashes_word[i] = g
          else:
            bad_guesses.append(g)
            guesses_left = guesses_left - 1
      print()

    if(dashes_word==mystery_word):
      print("Congratulations! You won! The word was " + mystery_word_str)
    else:
      print("Sorry, you lost. The word was " + mystery_word_str)

print("Welcome to hangman! I've picked a word.")
game_loop()
          
