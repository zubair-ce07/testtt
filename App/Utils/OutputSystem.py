import sys
import re


class OutputSystem:
    '''This class take care of all the required outputs'''

    def display_warning(self):
        print("Warning: Please enter the valid url & Try again!")

    def display_word_cloud(self, words_list):
        print("-----------------WORD CLOUD-------------------")
        for word_n_freq in words_list[:100]:
            print(word_n_freq)

    def display_menu(self):
        print("1. Enter URL to add or update record")
        print("2. View DB record")
        print("3. Exit")

    def display_data(self, data, is_itr=False):
        if is_itr:
            for item in data:
                print(item)
        else:
            print(data)
