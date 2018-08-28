'''This file is entry point for app & act as the controller for app'''
from Utils.InputSystem import InputSystem


def main_controller():
    input_sys = InputSystem()
    url = input_sys.get_input()
    is_valid = input_sys.validate_url(url)
    print(is_valid)

if __name__ == "__main__":
    main_controller()
