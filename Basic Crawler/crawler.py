import argparse

from report_generator import ReportGenerator
from url_extractor import UrlExtractor


def check_positive(value):
    """Checks if the argument is positive or not"""
    if value >= 0:
        return True
    else:
        return False


def parse_arguments():
    """Parse the command line arguments and returns the object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="Mai url containing data")
    parser.add_argument(
        'count', help="Number of urls to be downloaded", type=int)
    parser.add_argument('delay', help="Request delay (i.e 0.001)", type=float)
    parser.add_argument('requests', help="Total requests", type=int)
    parser.add_argument('type', help="Crawler type (i.e c/C or p/P)")
    return parser.parse_args()

if __name__ == "__main__":
    arg = parse_arguments()
    if check_positive(arg.count) and check_positive(
            arg.delay) and check_positive(arg.requests):
        crawler = UrlExtractor(
            arg.url, arg.count, arg.delay,
            arg.requests, arg.type)
        details = crawler.processing()

        # Report Generation
        report = ReportGenerator(details, arg.count, arg.requests)
        report.calculate()
        report.generate_report()
