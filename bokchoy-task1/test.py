import unittest
from bok_choy.web_app_test import WebAppTest
from pages import StudioHomepage, SignInPage

EMAIL = "rchachar@edx.org"
PASSWORD = "raees"

class TestStudio(WebAppTest):
	"""
	Tests Studio Site
	"""

	def setUp(self):
		"""
		Instantiate the page object.
		"""

		super(TestStudio,self).setUp()
		self.studio_homepage = StudioHomepage(self.browser)
		self.signinpage = SignInPage(self.browser)


		self.studio_homepage.visit()