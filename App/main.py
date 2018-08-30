'''This file is entry point for app & act as the controller for app'''

from Utils.InputSystem import InputSystem
from Utils.OutputSystem import OutputSystem
from Crawler.Crawler import Crawler
from Utils.TextProcessor import TextProcessor
from Db.Db import AppDB


input_sys = InputSystem()
output_sys = OutputSystem()
crawler = Crawler()
text_processor = TextProcessor()
db = AppDB()


def main_controller():
    '''This function control whole app & also transfer data &
        responses between multiple modules'''

    while(1):
        output_sys.display_menu()
        m_input = input_sys.get_menu_input()
        if m_input == "1":
            new_crawl()
        elif m_input == "2":
            view_db()
        else:
            exit(1)


def new_crawl():
    '''This function crawls new url & store/update in database'''

    url = input_sys.get_url_input()
    if url:
        words = crawler.crawl_url(url)
        words_dict = text_processor.dictionary_generator(words)
        sorted_list = text_processor.word_cloud_processor(words_dict)
        output_sys.word_cloud_generator(sorted_list)
        db.insert_row(sorted_list)
    else:
        output_sys.invalid_url_warning()
        main_controller()


def view_db():
    '''This function shows all data in decrypted form from database'''

    decrypted_data = db.get_all_data()
    output_sys.data_viewer(decrypted_data)

if __name__ == "__main__":
    main_controller()
