import sys
import helpers
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Remove-Retain character application.')
    parser.add_argument('-s', '--string',
                        help='String to operate on.',
                        required='True',
                        type=str,
                        default='techteam')
    results = parser.parse_args(args)
    return (results.string)

def main():
    """
    Operates on user input meanwhile handling any excptions.
    """
    input_argument = parse_args(sys.argv[1:]) # Receive arguments
    try:
        retain_first_output = helpers.retain_first_occurence_remove_rest(input_argument)
        retain_last_output = helpers.retain_last_occurence_remove_rest(input_argument)

    except (TypeError, ValueError) as i:
        print(format(i))
    # except ValueError as e:
    #     print(e.args[0])
    else:
        print ("Retain first output: " + retain_first_output)
        print("Retain last output: " + retain_last_output)

main()
