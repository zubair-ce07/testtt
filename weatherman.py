from weatherman_ds import MonthData
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('directory')
    parser.add_argument('-e', default='0')
    parser.add_argument('-a', default='0')
    parser.add_argument('-c', default='0')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
