from bok_choy.page_object import PageObject

class StudioHomepage(PageObject):
	"""
	Studio Home Page
	"""

	url = 'https://studio.stage.edx.org/'

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

	def enter_login_email(self,email):
		"""
		fill email field with user's email
		"""
		self.q(css='input#email').fill(email)

	def enter_login_password(self,password):
		"""
		fill email field with user's email
		"""
		self.q(css='input#password').fill(password)

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
