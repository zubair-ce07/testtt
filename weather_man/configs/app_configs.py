# -*- coding: utf-8 -*-
"""
Configurations which can be used through out the application are written here.
"""


class AppConfig:
    """
    Configurations for the application.
    """
    app_name = None
    app_type = None
    output_to = 'console'
    parser = None

    @classmethod
    def get_app_module_name(cls):
        """
        Provides application's module name by processing application name
        :return: Application's module name
        """
        return cls.app_name.replace('-', '_')

    @classmethod
    def get_app_name(cls):
        """
        Provides application's app name by processing application name
        :return: Application's app name
        """
        return "".join(map(lambda x: x.capitalize(), cls.app_name.split('-')))
