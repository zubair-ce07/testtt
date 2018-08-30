import sys
import result_data_reader
import result_processor
import result_reporter
import result_parser

if __name__ == '__main__':
    """
    This function compares the parsed input parameters
    and calls the respective functions.
    """
    cmd_arguments = result_parser.parse_arguments()
    users = result_data_reader.read_data()
    if not len(sys.argv) > 1:
        print("for Usage instructions, try main.py -h ")
    if cmd_arguments.present:
        # task 1: Showing the present students
        present_percentage = result_processor.get_percentage(users)
        result_reporter.show_percentage(present_percentage)
    if cmd_arguments.meritlist:
        # task 4: Showing the merit list
        groups = result_processor.create_merit_list(users, 50)
        result_reporter.generate_merit_list_files(groups)

    if cmd_arguments.passed:
        # performing task 3, scaled result percentage
        if "threshold" in cmd_arguments and "scale_ratio" in cmd_arguments:
            scaled_per = result_processor.get_percentage(
                users,
                cmd_arguments.threshold,
                cmd_arguments.scale_ratio
            )
            result_reporter.show_percentage(
                scaled_per,
                cmd_arguments.threshold,
                cmd_arguments.scale_ratio
            )
        # task 2, only passing threshold is given
        elif "threshold" in cmd_arguments:
            result_per = result_processor.get_percentage(
                users,
                cmd_arguments.threshold
            )
            result_reporter.show_percentage(
                result_per,
                cmd_arguments.threshold
            )
        else:
            print("Add -passing_criteria to get result")
