import signal
import sys

from .models import Game
from .noun_gender import run as NounGender
from .word_meaning import run as WordMeaning


def make_signal_handler(game):
    def signal_handler(sig, frame):
        print("\nFINAL REPORT\nWord\t\t\t\tResult\n"
              "-----------------------------------------------")

        for (word_text, correct, count) in game.results:
            print("{}\t{}\t(x{})".format(word_text.ljust(24), "correct" if correct else "wrong", count))
        print("===============================================")

        correct_total = len([item for item in game.results if item[1]])
        print("Total correct answers: {}".format(correct_total))

        sys.exit(0)

    return signal_handler

def start(datafile):
    try:
        game = Game.load(datafile)
        signal.signal(signal.SIGINT, make_signal_handler(game))
    except Exception as e:
        print(str(e))
        exit(1)

    print('Games:\n'
          '1. Noun gender (der/die/das)\n'
          '2. Word meaning')
    choice = input('Choose your game: ')
    options = {
        '1': NounGender,
        '2': WordMeaning
    }

    options[choice](game)
