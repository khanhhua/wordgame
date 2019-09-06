import argparse

parser = argparse.ArgumentParser()
parser.add_argument('datafile', type=str, help='Path to data file')

if __name__ == "__main__":
    import wordgame

    print("Welcome to WordGame!")
    args = parser.parse_args()

    wordgame.start(args.datafile)
