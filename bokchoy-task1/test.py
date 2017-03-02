import unittest

from bok_choy.web_app_test import WebAppTest
from pages import StudioHomepage, SignInPage, Dashboard, Course_page
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
        self.course_page = Course_page(self.browser)

        self.studio_homepage.visit()

    def test_addpage(self):
        """
        This test adds a new page to a particular course
        :return:
        """

        self.studio_homepage.sign_in()
        self.sign_in_page.login(EMAIL, PASSWORD)
        self.dashboard.open_course()


if __name__ == '__main__':
    unittest.main()
