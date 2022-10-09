# COSC 343 Wordle Assignment.

## How to run
Settings are changed in settings.py, where you can change language, number of guesses, amount of games, word length, 
and whether it is in easy or hard mode.

Make sure your environment has numpy installed, and run
```
py wordle.py
```
With verbose mode on, you will see the results of each game and the average score (the number of guesses it took) after 
each game. The random agent chooses a word randomly each time, to see its performance, change the agent in settings.py

## How does it work
The goal is to make a Wordle agent that can solve a Wordle with the state of the game as percepts.

The agent function takes the percepts as input and outputs a guess for the next word.

The percepts are a tuple of three items: the current guess, the letter indexes from the letters list so the agent
knows what letter was guessed last, and the letter states which can show what the result of the last guess was.

my_agent.py is my agent I created. Each guess, it eliminates all words from the dictionary that are not consistent 
with the percepts. For example, if the last guess had an S in it, and the letter is grey, this means it isn't in 
the answer, so all words with S in it can be eliminated from the dictionary.

When the last guess has yellows in it, I count the frequencies of all the letters in the dictionaries, and then use 
these to make a guess with the yellows in the most frequent spot for them.

In easy mode, the next guess does not have to contain the letters that are correct or in the wrong place from previous
 guesses, so I can guess a word made up of any letters. This means I can eliminate more words from the dictionary if I 
 can guess a word that has the most frequent letters in it. By reducing the dictionary each time, I can eventually find a 
 word that is the correct answer.
 
