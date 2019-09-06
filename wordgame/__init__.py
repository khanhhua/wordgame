from .models import Game

def start(datafile):
    try:
        game = Game.load(datafile)
    except Exception as e:
        print(str(e))
        exit(1)

    print("Welcome to WordGame!")        
    print("Let's get the gender correctly...")
    for word in game.words:
        print("Word:\t {}\n".format(word.text))

        answer = input("DER/DIE/DAS? ")
        if answer == word.gender:
            print("Correct!")
        else:
            print("IN YOUR FACE!")
        print("\n")
