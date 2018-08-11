import importlib
import os


class AppFactory:
    """
    Provides application objects on run time.
    """
    @staticmethod
    def get_specific_application(args):
        app_name = args[0]
        spec = importlib.util.spec_from_file_location("", os.path.join(f"{app_name}_app/utils/args_parser.py"))
        app_parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_parser)
        app_parser.a