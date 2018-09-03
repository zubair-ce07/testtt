import sqlite3


class DataAccessLayer:
    '''This class is responsible for maintaning database for App'''

    def __init__(self):
        self.conn = sqlite3.connect('Db/wordfreq.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wordfreq
             (id text, word text, freq real)''')
        self.conn.commit()

    def insert_row(self, encrypted_list):
        for w_id, encrypted_word, freq in encrypted_list:
            self.cursor.execute(
                'INSERT INTO wordfreq VALUES ("{}","{}","{}")'.format(
                    w_id, encrypted_word, freq
                ))
            self.conn.commit()

    def get_words_n_freqs(self):
        return self.cursor.execute('SELECT * FROM wordfreq')
