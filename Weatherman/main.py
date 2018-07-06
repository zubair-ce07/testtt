import argparse
from processor_file import Processor


def main():
    parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
    parser.add_argument('directory', help='Enter the directory')
    parser.add_argument('-e', '--type_e', type=int, help='Annual Report')
    parser.add_argument('-a', '--type_a', type=Processor.is_valid_argument, help='Monthly Report')
    parser.add_argument('-c', '--type_c', type=Processor.is_valid_argument, help='Dual Bar Chart')
    parser.add_argument('-d', '--type_d', type=Processor.is_valid_argument, help='Single Bar Chart')
    args = parser.parse_args()
    Processor(args)


if __name__ == '__main__':
    main()
