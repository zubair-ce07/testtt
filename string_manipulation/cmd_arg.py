import sys
import helpers as funcs_module

def main():
    """
    Operates on user input meanwhile handling any excptions.
    """
    # First input to be accepted from CMD argument,
    # rest from user input
    is_first_input_received = False

    while(True):
        try:
            if is_first_input_received:
                input_str = str(input())
            else:
                is_first_input_received = True
                input_str = sys.argv[1]

            retain_first_output = funcs_module.retain_first_occurence_remove_rest(input_str)
            retain_last_output = funcs_module.retain_last_occurence_remove_rest(input_str)

        except IndexError as i:
            print(i.args[0])
        except ValueError as e:
            print(e.args[0])
        else:
            print ("Retain first output: " + retain_first_output)
            print("Retain last output: " + retain_last_output)
            break

main()




