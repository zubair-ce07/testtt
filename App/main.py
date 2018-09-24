'''This file is entry point for app & act as the controller for app'''

from Utils.ArgParser import ArgParser
from Crawler.Crawler import Crawler
from Utils.TextParser import TextParser
from Db.Db import DataAccessLayer
from Utils.EncryptionManager import EncryptionManager


arg_parser = ArgParser()
crawler = Crawler()
text_parser = TextParser()
db = DataAccessLayer()
encryption_manager = EncryptionManager()


def main_controller():
    '''This function control whole app & also transfer data &
        responses between multiple modules'''

    args = arg_parser.input_parser()

    if args.n:
        new_crawl(args.url)
    elif args.v:
        view_db()


def new_crawl(url):
    '''This function crawls new url & store/update in database'''

    if not url:
        print("Enter URL to crawl & Try again!")
        return

    words = crawler.crawl_url(url)
    words_formatted = text_parser.format_words(words)
    words_sorted = text_parser.generate_sorted_list(words_formatted)
    encyrpted_list = []

    for word, freq in words_sorted[:100]:
        w_id = encryption_manager.generate_salted_hash(word)
        encrypted_word = (
                encryption_manager.encrypt_word(word))
        encyrpted_list.append((w_id, encrypted_word, freq))
    
    bag_of_words = [item[0] for item in words_sorted]
    term_freq_inverse_doc_freq = text_parser.term_freq_inverse_doc_freq_generator(bag_of_words)

    db.insert_word_freq(encyrpted_list)
    db.insert_term_freq_inverse_doc_freq(url, term_freq_inverse_doc_freq)


def view_db():
    '''This function shows all data in decrypted form from database'''

    for row in db.get_words_freqs():
        decrypted_word = encryption_manager.decrypt_word(row[1])
        print((decrypted_word, row[2]))

    for row in db.get_term_freq_inverse_doc_freq():
        print(row[1])

if __name__ == "__main__":
    main_controller()
