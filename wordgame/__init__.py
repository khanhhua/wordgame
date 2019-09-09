import signal
import sys

from .models import Game
from .noun_gender import run as NounGender


def make_signal_handler(game):
    def signal_handler(sig, frame):
        print("\nFINAL REPORT\nWord\t\t\t\tResult\n"
              "-----------------------------------------------")

        for (word_text, correct) in game.results:
            print("{}\t{}".format(word_text.ljust(24), "correct" if correct else "wrong"))
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

    NounGender(game)
