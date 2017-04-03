from bok_choy.page_object import PageObject
from utils import EMAIL, PASSWORD, AUTH_PASSWORD, AUTH_USER, PAGE_NAME, COURSE_KEY

class StudioHomepage(PageObject):
	"""
	Studio Home Page
	"""
	url = 'https://{}:{}@studio.stage.edx.org/'.format(AUTH_USER, AUTH_PASSWORD)

	def is_browser_on_page(self):
		return 'Welcome' in self.browser.title

	def click_sign_in(self):
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

	def enter_login_email(self):
		"""
		fill email field with user's email
		"""
		self.q(css='input#email').fill(EMAIL)

	def enter_login_password(self):
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

	def login(self):
		"""
		login a user
		"""
		self.enter_login_email()
		self.enter_login_password()
		self.click_sign_in_button()


class Dashboard(PageObject):
	"""
	Dashboard Page
	"""

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
	"""
	Page of a particular course
	"""
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
	"""
	This page adds pages to the course
	"""

	url = None

	def is_browser_on_page(self):
		return 'Pages' in self.browser.title

	def add_new_page(self):
		"""
		This function adds a new page to the course
		:return: none
		"""

		new_page_button = self.q(css="a.button.new-button.new-tab")
		new_page_button[0].click()
		self.wait_for_ajax()

	def edit_page(self, PAGE_NAME):
		"""
		This function edits the page name
		:return: none
		"""

		edit_button = self.q(css="a.edit-button.action-button")
		edit_button_index = -1
		edit_button[edit_button_index].click()
		self.wait_for_ajax()

		settings_button = self.q(css="a.settings-button")
		settings_button.click()
		self.wait_for_ajax()

		name_field = self.q(css="input.input.setting-input")
		name_field.fill(PAGE_NAME)

		save_button = self.q(css="a.button.action-primary.action-save")
		save_button.click()
		self.wait_for_ajax()

		view_live_button = self.q(css="a.button.view-button.view-live-button")
		view_live_button.click()
		LMSPage(self.browser).wait_for_page()

	def hide_page(self):
		"""
		This function hides a visible page of a course
		:return: none
		"""
		hide_button = self.q(css="input.toggle-checkbox")
		hide_button.click()

		self.wait_for_ajax()


class LMSPage(PageObject):
	"""
	Live LMS Page
	"""

	url = 'https://' + AUTH_USER + ':' + AUTH_PASSWORD + '@courses.stage.edx.org/'

	def is_browser_on_page(self):
		return self.q(css="a.menu-item").visible

	def click_sign_in(self):
		"""
		CLick on the sign in button and go to the next page
		"""
		self.wait_for_element_visibility('a.btn[href="https://courses.stage.edx.org/login"]',
										 'Sign in button is visible')

		sign_in_button = self.q(css='a.btn[href="https://courses.stage.edx.org/login"]')
		sign_in_button[0].click()
		LMSSignInPage(self.browser).wait_for_page()

	def get_page_tabs (self):
		"""
		This function checks if the page is on the live LMS or not
		:param PAGE_NAME:
		:return:boolean
		"""
		self.wait_for_ajax()
		page_tabs = self.q(css="li.tab > a[href^='/courses']").text
		print page_tabs

		return page_tabs


class LMSSignInPage(PageObject):
	"""
	LMS Sign In page
	"""

	url = None

	def is_browser_on_page(self):
		return self.q(css='button.action.action-primary').visible

	def enter_login_email(self, EMAIL):
		"""
		fill email field with user's email
		"""
		self.q(css='input#login-email').fill(EMAIL)

	def enter_login_password(self, PASSWORD):
		"""
		fill email field with user's email
		"""
		self.q(css='input#login-password').fill(PASSWORD)

	def click_sign_in_button(self):
		"""
		click the sign in button
		"""
		self.q(css='button.action.action-primary').click()
		Dashboard(self.browser).wait_for_page()

	def login(self, email, password):
		"""
		login a user
		"""
		self.enter_login_email(email)
		self.enter_login_password(password)
		self.click_sign_in_button()
