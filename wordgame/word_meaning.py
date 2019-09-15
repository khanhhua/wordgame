"""
Noun gender game
"""
from random import randrange, shuffle

def run(game):
    """
    Required function for a game module
    :param game:
    :return:
    """
    print("Welcome to WordGame!")
    print("Let's get the meaning correctly...")

    while True:
        count = len(game.words)
        index = randrange(0, count)
        word = game.words[index]

        choices = [
            word.meaning,
            game.words[randrange(0, count)].meaning,
            game.words[randrange(0, count)].meaning
        ]
        shuffle(choices)
        print("Word:\t {}\n".format(str(word)))

        answer = input("{}/{}/{}? ".format(*choices))
        if answer == word.meaning:
            print("Correct!")
            game.collect_result(word.text, True)
        else:
            print("IN YOUR FACE!")
            game.collect_result(word.text, False)

        print("\n")
