import sys
import re


class InputSystem:
    '''This class take care of all the required input validation & parsing'''

    def get_url_input(self):
        url = input("Enter your desired url: ")
        return self.validate_url(url)

    def validate_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(regex, url) is not None:
            return url
    
    def get_menu_input(self):
        m_input = input("Enter your input: ")
        return m_input

