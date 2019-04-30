import argparse
from life_game import LifeGame

def main():
    """ main function """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="enter file name")
    parser.add_argument("iterations", help="enter iterations number")
    args = parser.parse_args()
    if args.file_name:
        obj = LifeGame(args.file_name)
        for counter in range(int(args.iterations)):
            print('Generation No: ' + str(counter+2))
            obj.populate_new_generation()
            obj.display_new_generation()
            obj.change_transition()
            print()

if __name__ == "__main__":
    main()
