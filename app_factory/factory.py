import os
from importlib import util

from configs.app_configs import AppConfig


class AppFactory:
    """
    Provides application objects on run time, based on which app is wanted.
    """
    @staticmethod
    def get_specific_application():
        """
        Provides specific application's object and it's specific args by loading specific module of that particular
        application and returning application object and argumentsHandler class from module.
        :return: Application object.
        """
        module_name = AppConfig.get_app_module_name()
        app_name = AppConfig.get_app_name()
        spec_app = util.spec_from_file_location(
            app_name, os.path.join(f"{module_name}_app/{module_name}.py")
        )
        application = util.module_from_spec(spec_app)
        spec_app.loader.exec_module(application)

        spec_args = util.spec_from_file_location(
            "ArgsParserCategoryHandler", os.path.join(f"{module_name}_app/utils/global_content.py")
        )
        args_handler = util.module_from_spec(spec_args)
        spec_args.loader.exec_module(args_handler)

        return getattr(application, app_name)(), getattr(args_handler, "ArgsParserCategoryHandler")
