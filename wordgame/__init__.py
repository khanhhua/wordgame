from .models import Game

def start(datafile):
    game = Game.load(datafile)

    print("Let's get the gender correctly...")
    for word in game.words:
        print("Word:\t {}\n".format(word.text))

        answer = input("DER/DIE/DAS? ")
        if answer == word.gender:
            print("Correct!")
        else:
            print("IN YOUR FACE!")
        print("\n")
