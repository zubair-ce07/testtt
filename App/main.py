'''This file is entry point for app & act as the controller for app'''

from Utils.InputSystem import InputSystem
from Utils.OutputSystem import OutputSystem
from Crawler.Crawler import Crawler
from Utils.TextProcessor import TextProcessor


def main_controller():
    """This function control whole app & also transfer data &
        responses between multiple modules"""

    input_sys = InputSystem()
    output_sys = OutputSystem()
    crawler = Crawler()
    text_processor = TextProcessor()
    url = input_sys.get_input()
    if url:
        words = crawler.crawl_url(url)
        words_dict = text_processor.dictionary_generator(words)
        sorted_list = text_processor.word_cloud_processor(words_dict)
        output_sys.word_cloud_generator(sorted_list)
    else:
        output_sys.invalid_url_warning()
        main_controller()

if __name__ == "__main__":
    main_controller()
