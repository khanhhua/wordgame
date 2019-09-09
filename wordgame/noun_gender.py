"""
Noun gender game
"""
from random import randrange

def run(game):
    """
    Required function for a game module
    :param game:
    :return:
    """
    print("Welcome to WordGame!")
    print("Let's get the gender correctly...")

    while True:
        index = randrange(0, len(game.words))
        word = game.words[index]
        print("Word:\t {}\n".format(word.text))

        answer = input("DER/DIE/DAS? ")
        if answer == word.gender:
            print("Correct!")
            game.collect_result(word.text, True)
        else:
            print("IN YOUR FACE!")
            game.collect_result(word.text, False)

        print("\n")
