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
		Course_page(self.browser).wait_for_page()


class Course_page(PageObject):

	url = None

	def is_browser_on_page(self):
		return 'Course Outline' in self.browser.title