import sys
import String_manip_functions as funcsModule

def print_empty_message():
    print("\nYou did not enter an input.\n"
          "Please re-enter:")

def print_invalid_message():
    print("\nNumbers or special characters are not allowed.\n"
          "You must enter alphabets only.\n"
          "Please re-enter:")

def main():
    """
    Operates on user input meanwhile handling any excptions.
    """
    # First input to be accepted from CMD argument,
    # rest from user input
    isFirstInputReceived = False

    while(True):
        try:
            if isFirstInputReceived:
                input_str = str(input())
            else:
                isFirstInputReceived = True
                input_str = sys.argv[1]

        except IndexError:
            print_empty_message()
        else:
            # Print here
            retain_first_output = funcsModule.retain_first_occurence_remove_rest(input_str)
            retain_last_output = funcsModule.retain_last_occurence_remove_rest(input_str)

            if retain_first_output == "0num":
                print_invalid_message()
            elif retain_first_output == "0empty":
                print_empty_message()
            else:
                print ("Retain first output: " + retain_first_output)
                print("Retain last output: " + retain_last_output)
                break

main()




