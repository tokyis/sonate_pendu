import random
import string

import flask
import unicodedata

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

DICTIONARY_PATH = './dictionnaire.txt'
MAX_LIVES = 5


class GameState:
    """
    Represents the state of the game.

    :param player_name: The name of the player. (default: '')
    :type player_name: str
    :param secret_word: The secret word to guess. (default: '')
    :type secret_word: str
    :param player_lives: The number of lives the player has. (default: MAX_LIVES)
    :type player_lives: int
    :param player_guesses: The letters guessed by the player. (default: '')
    :type player_guesses: str
    """

    def __init__(self, player_name='', player_lives=MAX_LIVES, secret_word='', player_guesses=''):
        self.player_name = player_name.strip()
        self.player_lives = player_lives
        self.secret_word = secret_word
        self.player_guesses = player_guesses


state: GameState = None
dictionary: list = None


def build_dictionary(path):
    """
    Reads a text file from the given `path` and extracts the first value preceded by a semicolon.

    :param path: The path to the text file.
    :return: A list of words.
    """
    global dictionary
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        dictionary = []
        for line in lines:
            values = line.split(';')
            if len(values) != 0:
                dictionary.append(values[0])
    return dictionary


def normalize_string(str):
    """
    Normalize a string by removing diacritics.

    :param str: The input string. ex.'ça arrive bientôt'
    :return: The normalized string. ex. 'ca arrive bientot'
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', str)
        if unicodedata.category(c) != 'Mn'
    )


def get_masked_word(word, guessed_letters):
    """
    :param word: The word to be masked.
    :param guessed_letters: The letters that have been guessed by the player.
    :return: The masked word where letters that have been guessed
     correctly are visible and letters that haven't been guessed are replaced with underscore(str).
    """
    masked_word = ''
    for letter in word:
        if normalize_string(letter) in guessed_letters:
            masked_word += letter + ' '
        else:
            masked_word += '_ '
    return masked_word.strip()


def is_word_found(guessed_letters, word):
    """
    Determines if all the letters in the word have been guessed correctly.

    :param guessed_letters: A list or string of letters that have been guessed.
    :param word: The word to be guessed.
    :return: True if all the letters in the word have been guessed correctly, False otherwise.
    """
    global state
    for letter in word:
        if normalize_string(letter) not in guessed_letters:
            return False
    return True


@app.route('/')
def home():
    global dictionary
    if dictionary is None:
        dictionary = build_dictionary(DICTIONARY_PATH)
    return render_template('home.html')


@app.route('/play', methods=['POST'])
def play():
    global state, dictionary
    is_gameover = False
    has_won = False

    if request.method == 'POST':
        # Handle starting or restarting a round
        if 'player_name' in request.form.keys() and request.form['player_name'] != '':
            state = GameState(request.form['player_name'].strip(), MAX_LIVES, random.choice(dictionary))
            print(f"Starting new game, secret secret_word is : {state.secret_word}")
            # Apostrophes don't need to be guessed
            if "'" in state.secret_word:
                state.player_guesses += "'"

        # Handle playing, wining and losing
        if ('letter' in request.form.keys()
                and request.form['letter'] != ''
                and request.form['letter'] not in state.player_guesses):

            letter = request.form['letter'].strip()
            state.player_guesses += letter
            if letter not in normalize_string(state.secret_word):
                state.player_lives -= 1
                print(f"Wrong : '{letter}' is not in {state.secret_word}, "
                      f"{state.player_lives} live(s) left.")
                if state.player_lives == 0:
                    print(f"Game lost.")
                    is_gameover = True
            else:
                print(f"Right : '{letter}' is in {state.secret_word}, {state.player_lives} live(s) left.")
                if is_word_found(state.player_guesses, state.secret_word):
                    print(f"Game won.")
                    is_gameover = True
                    has_won = True

    return render_template('play.html',
                           keys=string.ascii_lowercase,
                           player_name=state.player_name,
                           player_lives=state.player_lives,
                           secret_word=state.secret_word,
                           masked_word=get_masked_word(state.secret_word, state.player_guesses),
                           is_gameover=is_gameover,
                           has_won=has_won)
