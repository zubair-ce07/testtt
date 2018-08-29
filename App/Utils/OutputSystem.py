import sys
import re


class OutputSystem:
    '''This class take care of all the required outputs'''
    
    def invalid_url_warning(self):
        print("Warning: Please enter the valid url & Try again!")
    
    def word_cloud_generator(self, words_list):
        print("-----------------WORD CLOUD-------------------")
        for word_n_freq in words_list[:100]:
            print(word_n_freq)
