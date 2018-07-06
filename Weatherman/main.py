import argparse
import processor_file


def main():
    parser = argparse.ArgumentParser(description='Report will be generated according to the Arguments')
    parser.add_argument('directory', help='Enter the directory')
    parser.add_argument('-e', '--type_e', type=int, help='Annual Report', choices=range(1900, 2017))
    parser.add_argument('-a', '--type_a', type=processor_file.is_valid, help='Monthly Report')
    parser.add_argument('-c', '--type_c', type=processor_file.is_valid, help='Dual Bar Chart')
    parser.add_argument('-d', '--type_d', type=processor_file.is_valid, help='Single Bar Chart')
    args = parser.parse_args()
    processor_file.run(args)


if __name__ == '__main__':
    main()
