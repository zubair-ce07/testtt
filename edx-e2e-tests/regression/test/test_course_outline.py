"""
End to end tests for Studio Course Outline page
"""
import os
from bok_choy.web_app_test import WebAppTest
from edxapp_acceptance.tests.helpers import assert_side_bar_help_link

from regression.pages.studio.course_outline_page import (
    CourseOutlinePageExtended
)
from regression.pages.studio.login_studio import StudioLogin
from regression.pages.studio.settings_studio import SettingsPageExtended
from regression.pages.studio.studio_home import DashboardPageExtended
from regression.tests.helpers.utils import (
    get_course_info, get_course_display_name
)

DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')


class StudioCourseOutlineTest(WebAppTest):
    """Tests of the Course Outline in Studio."""

    def setup(self):
        """
        Handles the common instantiations and function calls needed for
        all the tests in this Class
        :return:none
        """

        studio_login_page = StudioLogin(self.browser)
        studio_home_page = DashboardPageExtended(self.browser)

        course_info = get_course_info()

        studio_course_outline = CourseOutlinePageExtended(
            self.browser, course_info['org'], course_info['number'],
            course_info['run'])

        schedule_page = SettingsPageExtended(
            self.browser, course_info['org'], course_info['number'],
            course_info['run'])

        studio_login_page.visit()
        studio_login_page.login(DEMO_COURSE_USER, DEMO_COURSE_PASSWORD)

        # Verification only, should be on this page after login.
        self.studio_home_page.wait_for_page()

        # Navigate to the course's outline page
        self.studio_home_page.select_course(get_course_display_name())
        studio_course_outline.wait_for_page()

    def test_course_outline(self):
        """
        Verifies that user can click Edit Start Date button and is navigated
        to Schedule and Details page, and that the Help link for
        'Learn more about content visibility settings' is working.
        """
        link_text='Learn more about content visibility settings'

        # First verify the Help link
        expected_href = 'https://edx.readthedocs.io/projects/' \
                        'edx-partner-course-staff/en/latest/' \
                        'developing_course/controlling_content_visibility.html'

        self.verify_helplink(expected_href, link_text)

        # If the help page is still up (see LT-53), then close it.
        if self.browser.current_url.startswith('https://edx.readthedocs.io'):
            # TODO wrap this in a try/except block or otherwise harden,
            # make sure that you now have an active window (the other one)
            # and it's the right one (i.e. Studio or LMS)
            self.browser.close()  # close only the current window
            self.browser.switch_to_window(self.browser.window_handles[0])

        # Now do the verification for the edit start date button.
        self.studio_course_outline.click_edit_start_date_button()

        # This wait_for_page will also assert that we are on the correct page.
        self.schedule_page.wait_for_page()

    def test_verify_helplink_course_outline(self):
        """
        Verifies that the Help link for
        'Learn more about the course outline' is working.
        :return:
        """

        # First verify the Help link
        expected_href = 'https://edx.readthedocs.io/projects/' \
                        'edx-partner-course-staff/en/latest/' \
                        'developing_course/course_outline.html'

        link_text = 'Learn more about the course outline'

        self.verify_helplink(expected_href, link_text)

    def test_verify_helplink_grading_policy(self):
        """
        Verifies that the Help link for
        'Learn more about grading policy settings' is working.
        :return:
        """

        # First verify the Help link
        expected_href = 'https://edx.readthedocs.io/projects/' \
                        'edx-partner-course-staff/en/latest/' \
                        'grading/index.html'

        link_text = 'Learn more about grading policy settings'

        self.verify_helplink(expected_href, link_text)

    def test_verify_helplink_content_visibility(self):
        """
        Verifies that the Help link for
        'Learn more about content visibility settings' is working.
        :return:
        """

        # First verify the Help link
        expected_href = 'https://edx.readthedocs.io/projects/' \
                        'edx-partner-course-staff/en/latest/' \
                        'developing_course/controlling_content_visibility.html'

        link_text = 'Learn more about content visibility settings'

        self.verify_helplink(expected_href, link_text)

    def verify_helplink(self, link_url, link_text):
        """
        This function verifies the side bar link text and url
        :param link_url:
        :param link_text:
        :return:
        """
        # Assert that help link is correct.
        assert_side_bar_help_link(
            test=self,
            page=self.studio_course_outline,
            href=link_url,
            help_text=link_text,
            as_list_item=False
        )
