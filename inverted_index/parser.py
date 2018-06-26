__author__ = 'abdul'

from html.parser import HTMLParser

import constants


class HtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.isRecording = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.isRecording = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.isRecording = False

    def handle_data(self, data):
        """
        If data belongs to <p> tag,
        Write data to file.
        """
        if self.isRecording and data != '\n':
            with open(constants.parsed_data_file_name, 'a') as f:
                    f.write("{}\n".format(data.strip('\n')))
                    #f.write("!-#-!\n")
