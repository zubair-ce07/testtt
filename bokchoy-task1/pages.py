from bok_choy.page_object import PageObject
from utils import EMAIL, PASSWORD, AUTH_PASSWORD, AUTH_USER

class StudioHomepage(PageObject):
	"""
	Studio Home Page
	"""
	url = 'https://' + AUTH_USER + ':' + AUTH_PASSWORD + '@studio.stage.edx.org/'

	def is_browser_on_page(self):
		return 'Welcome' in self.browser.title

	def sign_in(self):
		"""
		CLick on the sign in button and go to the next page
		"""
		self.q(css='a.action.action-signin').click()
		SignInPage(self.browser).wait_for_page()


class SignInPage(PageObject):
	"""
	Sign in page
	"""

	url = None

	def is_browser_on_page(self):
		return 'Sign In | edX Studio' in self.browser.title

	def enter_login_email(self, EMAIL):
		"""
		fill email field with user's email
		"""
		self.q(css='input#email').fill(EMAIL)

	def enter_login_password(self, PASSWORD):
		"""
		fill email field with user's email
		"""
		self.q(css='input#password').fill(PASSWORD)

	def click_sign_in_button(self):
		"""
		click the sign in button
		"""
		self.q(css='button.action.action-primary').click()
		Dashboard(self.browser).wait_for_page()

	def login(self,email,password):
		"""
		login a user
		"""
		self.enter_login_email(email)
		self.enter_login_password(password)
		self.click_sign_in_button()


class Dashboard(PageObject):

	url = None


	def is_browser_on_page(self):
		return 'Studio Home | edX Studio' in self.browser.title

	def open_course(self):
		"""
		opens a specific course
		"""

		self.q(css="li[data-course-key='course-v1:ColumbiaX+AP123+2017_T2']").click()
		CoursePage(self.browser).wait_for_page()


class CoursePage(PageObject):

	url = None

	def is_browser_on_page(self):
		return 'Course Outline' in self.browser.title

	def go_to_pages(self):
		"""
		This function redirects to the Pages page of the course
		:return:none
		"""

		self.wait_for_ajax()
		content_button = self.q(css="li.nav-item.nav-course-courseware")
		content_button.click()

		page_option = self.q(css="li.nav-item.nav-course-courseware-pages")
		page_option.click()

		PagesPage(self.browser).wait_for_page()


class PagesPage(PageObject):

	url = None

	def is_browser_on_page(self):
		return 'Pages' in self.browser.title

	def add_new_page(self):
		"""
		This function adds a new page to the course
		:return: none
		"""

		new_page_button = self.q(css="a.button.new-button.new-tab")
		new_page_button.click()
		self.wait_for_ajax()

