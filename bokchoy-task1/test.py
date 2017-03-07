import unittest

from bok_choy.web_app_test import WebAppTest
from pages import StudioHomepage, SignInPage, Dashboard, CoursePage, PagesPage, LMSPage, LMSSignInPage
from utils import EMAIL, PASSWORD, PAGE_NAME

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
        self.pages_page = PagesPage(self.browser)
        self.lms_page = LMSPage(self.browser)
        self.lms_signinpage = LMSSignInPage(self.browser)

        #Login to LMS page
        """self.lms_page.visit()
        self.lms_page.sign_in()
        self.lms_signinpage.login()"""

        #Login to studio page
        self.studio_homepage.visit()
        self.studio_homepage.sign_in()
        self.sign_in_page.login(EMAIL, PASSWORD)
        self.dashboard.open_course()
        self.course_page.go_to_pages()

    def test_addpage(self):
        """
        This test adds a new page to a particular course
        :return:none
        """

        self.pages_page.add_new_page()
        self.pages_page.edit_page(PAGE_NAME)
        tab_list = self.lms_page.is_page_present(PAGE_NAME).text

        self.assertIn(PAGE_NAME, tab_list)

    def test_hidepage(self):
        """
        this test hides an existing page of a particular course
        :return:none
        """

       self.pages_page.hide_page()


if __name__ == '__main__':
    unittest.main()
