from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

DICTIONARY = 'dictionnaire.txt'

state = None
dictionary = None
keys = None


class GameState:
    def __init__(self, username='', word='', lives=0):
        self.username = username.strip()
        self.word = word
        self.lives = lives
        self.guesses = ''


def get_dictionary(path):
    """
    :param path: The file path to the dictionary text file.
    :return: The dictionary extracted from the file as a list of strings.
    """
    with open(path, 'r') as file:
        lines = file.readlines()
        dictionary = []
        for line in lines:
            values = line.split(';')
            if len(values) != 0:
                dictionary.append(values[0])
    return dictionary


def build_keymap(dictionary):
    keys = []
    for word in dictionary:
        for letter in word:
            if letter not in keys:
                keys.append(letter)
    keys.sort()
    return keys


def get_random_word(dictionary):
    return random.choice(dictionary)


def initialize():
    global state, dictionary, keys
    state = GameState()
    dictionary = get_dictionary(DICTIONARY)
    keys = build_keymap(dictionary)


@app.route('/')
def home():
    global state, dictionary, keys
    if state is None:
        state = GameState()
        dictionary = get_dictionary(DICTIONARY)
        keys = build_keymap(dictionary)
    return render_template('home.html')


@app.route('/play', methods=['GET', 'POST'])
def play():
    global state
    if request.method == 'GET' and state is None:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if 'username' in request.form.keys() and request.form['username'] != '':
            state.username = request.form['username']
        if 'guesses' in request.form.keys() and request.form['guesses'] != '':
            pass
    return render_template('play.html', state=state)
