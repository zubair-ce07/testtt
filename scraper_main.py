import argparse
from scraper import Scraper


def main(argv):
    scraper = Scraper(argv.url)
    products = scraper.scrap()
    print(len(products), products)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="Website url to scrap")
    args = parser.parse_args()
    main(args)
