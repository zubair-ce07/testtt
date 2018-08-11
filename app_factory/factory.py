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
        Provides specific application's object by loading specific module of that particular application and returning
        application object from module.
        :return: Application object.
        """
        module_name = AppConfig.get_app_module_name()
        app_name = AppConfig.get_app_name()
        spec = util.spec_from_file_location(
            app_name, os.path.join(f"{module_name}_app/{module_name}.py")
        )
        application = util.module_from_spec(spec)
        spec.loader.exec_module(application)
        return getattr(application, app_name)()
