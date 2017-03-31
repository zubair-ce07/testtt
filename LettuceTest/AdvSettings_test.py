import unittest

from bok_choy.web_app_test import WebAppTest
from AdvancedSettings_pages import StudioHomepage, SignInPage, Dashboard, CoursePage, AdvancedSettingsPage
from utils import EMAIL, PASSWORD

class TestStudio(WebAppTest):
    """
    Test Studio Site
    """

    def setUp(self):
        """
        This function instantiates the PageObject
        :return: none
        """

        super(TestStudio, self).setUp()
        self.studio_homepage = StudioHomepage(self.browser)
        self.sign_in_page = SignInPage(self.browser)
        self.dashboard = Dashboard(self.browser)
        self.course_page = CoursePage(self.browser)
        self.advanced_settings_page = AdvancedSettingsPage(self.browser)

        #Login to studio page
        self.studio_homepage.visit()
        self.studio_homepage.sign_in()
        self.sign_in_page.login(EMAIL, PASSWORD)
        self.dashboard.open_course()

    def test_toggleDeprecatedSettings(self):
        """
        This fucntion tests the toggle hide/show of the deprecated settings button
        :return: None
        """
        self.course_page.open_advanced_settings()
        self.advanced_settings_page.show_deprecated_settings()
        self.advanced_settings_page.hide_deprecated_settings()


if __name__ == '__main__':
    unittest.main()


