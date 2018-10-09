import os

# Set your application settings file path here
APPLICATION_SETTINGS = "application.settings"

# Donot edit this line in any case otherwise your application will issue error
os.environ["application_settings"] = APPLICATION_SETTINGS

if os.environ["application_settings"]:
    from framework.framework import run_server
    run_server()
