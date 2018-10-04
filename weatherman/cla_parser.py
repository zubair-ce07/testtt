import re
import argparse
import os.path

def arguments_parser():
    cla_parser = argparse.ArgumentParser()

    cla_parser.add_argument(
        "dir",
        help="Data DIR path",
        type=str
    )

    cla_parser.add_argument(
        "-e", "--yearly",
        help="For Yearly weather report",
        action="store_true"
    )
    # cla_parser.add_argument(
    #     "--date_str_year",
    #     help="Year Date format must be yyyy",
    #     type=str,
    #     # action="store"
    # )

    cla_parser.add_argument(
        "-a", "--monthly",
        help="For maonthly weather report",
        action="store_true"
    )
    # cla_parser.add_argument(
    #     "--date_str_month",
    #     help="Month Date format must be yyyy/mm",
    #     # type=str,
    #     # action="store_true"
    # )

    cla_parser.add_argument(
        "-c", "--monthly_eachday",
        help="For monthly eachday report",
        action="store_true"
    )
    # cla_parser.add_argument(
    #     "--date_str_eachday",
    #     help="Eachday Date format must be yyyy/mm",
    #     # type=str,
    #     # action="store_true"
    # )

    cla_parser.add_argument(
        "-cb", "--monthly_bonus",
        help="For monthly eachday report(bonus)",
        action="store_true"
    )
    cla_parser.add_argument(
        "date_str",
        help="Eachday Date format must be yyyy/mm",
        type=str,
        # action="store_true"
    )
    
    
    return cla_parser.parse_args()


def validate_argumets():
        cmd_line_args = arguments_parser()
        
        
        if not re.search(r'\d{4}/{0,1}\d{0,2}',cmd_line_args.date_str):
            # print(cmd_line_args.date_str_year)
            print("Enter the correct format of date")
            exit(0)

        if not os.path.exists(cmd_line_args.dir):
            print("Provide existing path of directory")
            exit(0)

        return cmd_line_args