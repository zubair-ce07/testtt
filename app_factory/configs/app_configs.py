# -*- coding: utf-8 -*-
"""
Configurations which can be used through out different applications are written here (Configurations are set
differently in different applications).
"""


class AppConfig:
    """
    Configurations for the application.
    """
    app_name = None
    app_type = None
    output_to = 'console'
    parser = None

    @staticmethod
    def get_app_module_name():
        """
        Provides application's module name by processing application name
        :return: Application's module name
        """
        return AppConfig.app_name.replace('-', '_')

    @staticmethod
    def get_app_name():
        """
        Provides application's app name by processing application name
        :return: Application's app name
        """
        return "".join(map(lambda x: x.capitalize(), AppConfig.app_name.split('-')))
