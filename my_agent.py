__author__ = "Liam Wilson"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "wilia832@student.otago.ac.nz"

import helper
import numpy as np


class WordleAgent():
    """
       A class that encapsulates the code dictating the
       behaviour of the Wordle playing agent

       ...

       Attributes
       ----------
       dictionary : list
           a list of valid words for the game
       letter : list
           a list containing valid characters in the game
       word_length : int
           the number of letters per guess word
       num_guesses : int
           the max. number of guesses per game
       mode: str
           indicates whether the game is played in 'easy' or 'hard' mode

       Methods
       -------
       AgentFunction(percepts)
           Returns the next word guess given state of the game in percepts
       """

    def __init__(self, dictionary, letters, word_length, num_guesses, mode):
        """
      :param dictionary: a list of valid words for the game
      :param letters: a list containing valid characters in the game
      :param word_length: the number of letters per guess word
      :param num_guesses: the max. number of guesses per game
      :param mode: indicates whether the game is played in 'easy' or 'hard' mode
      """

        self.dictionary = dictionary
        self.save_dictionary = list(dictionary)
        self.letters = letters
        self.word_length = word_length
        self.num_guesses = num_guesses
        self.mode = mode
        self.contains = []

    def scoring(self, words, frequencies):
        """ Scoring function to pick the word with the highest score
            Highest score calculated with the frequencies

        :param words: Word array of words to score
        :param frequencies: Frequencies of letters to score by
        :return: A word with the highest score
        """
        high_score_word = ""
        high_score = 0

        for word in words:
            freqs = dict(frequencies)
            count = 0
            for letter in word:
                count += freqs[letter]
                freqs[letter] = 0

            if count > high_score:
                high_score_word = word
                high_score = count
        return high_score_word

    def AgentFunction(self, percepts):
        """Returns the next word guess given state of the game in percepts

      :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
      :return: string - a word from self.dictionary that is the next guess
      """

        # Extract three different parts of percepts.
        guess_counter, letter_indexes, letter_states = percepts

        # Array for letters in correct spot and yellows
        yellows = []
        letters_left = 5
        # If guess counter is 0 reset the dictionary
        if guess_counter == 0:
            self.dictionary = self.save_dictionary
            self.contains = []
        if guess_counter > 0:
            # For each letter of the word
            for s in range(self.word_length):
                # Convert letter index into letter
                letter = helper.letter_indices_to_word([letter_indexes[s]],
                                                       self.letters)
                # If letter is in correct spot
                if letter_states[s] == 1:
                    self.dictionary = [x for x in self.dictionary
                                       if letter in x[s]]
                    letters_left -= 1
                    self.contains.append(letter)
                if letter_states[s] == -1:
                    self.dictionary = [x for x in self.dictionary
                                       if letter not in x[s]]
                    self.contains.append(letter)
                    yellows.append(letter)
            # Loop through again so that greys can be counted fairly
            for s in range(self.word_length):
                letter = helper.letter_indices_to_word([letter_indexes[s]],
                                                       self.letters)
                if letter_states[s] == 0:
                    if letter not in self.contains:
                        self.dictionary = [x for x in self.dictionary
                                           if letter not in x]
                    else:
                        self.dictionary = [x for x in self.dictionary
                                           if letter not in x[s]]

            for c in self.contains:
                self.dictionary = [x for x in self.dictionary
                                   if c in x]

        # Fill in a frequency list to find what the most common letters are
        # for the empty spaces.

        # From this frequency list make a word with the most common letters,
        # if it doesn't guess right then the most common letters are gone and
        # less words to pick from

        frequent_letters = []
        total_frequencies = dict.fromkeys(self.letters, 0)
        for x in range(len(letter_states)):
            if letter_states[x] == 0 or letter_states[x] == -1:

                frequencies = dict.fromkeys(self.letters, 0)
                for word in self.dictionary:
                    frequencies[
                        word[x]] += 1
                    total_frequencies[word[x]] +=1
                frequent_letters.append(frequencies)

        # Put the yellows in the right place with
        # a new dict, go for the most frequent spot for them, first find that
        # spot.
        new_dict = list(self.dictionary)
        for c in yellows:
            index = 0
            count = 0
            for x in range(len(frequent_letters)):
                if frequent_letters[x][c] > count:
                    index = x
                    count = frequent_letters[x][c]
            new_dict = [i for i in new_dict
                        if i[index] == c]

        # Make guess off of scoring function
        if len(yellows) == 0 and letters_left < 5 and guess_counter < 5 and len(new_dict) > 2 \
                and len(self.dictionary) > 2 and self.mode == 'easy':
            return self.scoring(self.save_dictionary, total_frequencies)

        # Guess off of the shortened dictionary
        if len(new_dict) > 0:
            word_index = np.random.randint(0, len(new_dict))
            return new_dict[word_index]
        else:
            word_index = np.random.randint(0, len(self.dictionary))

        # Guess off of the full dictionary
        return self.dictionary[word_index]
