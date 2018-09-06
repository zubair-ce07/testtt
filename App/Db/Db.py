import sqlite3


class DataAccessLayer:
    '''This class is responsible for maintaning database for App'''

    def __init__(self):
        self.conn = sqlite3.connect('Db/wordfreq.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wordfreq
             (id text, word text, freq real)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tfidf
             (url text, tfidf real)''')
        self.conn.commit()

    def insert_word_freq(self, encrypted_words):

        for w_id, encrypted_word, freq in encrypted_words:
            self.cursor.execute(
                f'INSERT INTO wordfreq VALUES ("{w_id}","{encrypted_word}","{freq}")')
            self.conn.commit()

    def get_words_freqs(self):
        return self.cursor.execute('SELECT * FROM wordfreq')

    def insert_term_freq_inverse_doc_freq(self, url, term_freq_inverse_doc_freq):
        self.cursor.execute(
                f'INSERT INTO tfidf VALUES ("{url}","{term_freq_inverse_doc_freq}")')
        self.conn.commit()

    def get_term_freq_inverse_doc_freq(self):
        return self.cursor.execute('SELECT * FROM tfidf')
