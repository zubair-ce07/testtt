from config.Parser import Parser
from models.WeatherData import WeatherData


def main():
    p = Parser('/home/asad/work/assignments/the-lab/weatherfiles/weatherfiles')
    p.read()  # reads complete dir and populate data in data structures
    print("Now showing data")

    WeatherData.print_()


if __name__ == "__main__":
    main()
