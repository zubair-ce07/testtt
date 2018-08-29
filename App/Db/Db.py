import sqlite3
from Utils.Hasher import Hasher


class AppDB:
    '''This class is responsible for maintaning database for App'''

    def __init__(self):
        self.conn = sqlite3.connect('Db/wordfreq.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        self.hasher = Hasher()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wordfreq
             (id text, word text, freq real)''')
        self.conn.commit()

    def insert_row(self, words_list):
        for word, freq in words_list[:100]:
            w_id = self.hasher.generate_salted_hash(word)
            if self.is_already_in_db(word):
                self.update_row(w_id, freq)
            else:
                encrypted_word = self.hasher.generate_asym_encryption(word)
                self.cursor.execute(
                    'INSERT INTO wordfreq VALUES ("{}","{}","{}")'.format(
                        w_id, encrypted_word, freq
                    ))
                self.conn.commit()
    
    def update_row(self, w_id, freq):
        result = self.cursor.execute(
                'SELECT * FROM wordfreq where id="{}"'.format(
                    w_id))
        for row in result:
            self.cursor.execute(
                'UPDATE INTO wordfreq (freq) VALUES' +
                '("{}") where id="{}"'.format(
                    freq+row[2], w_id
                    ))
            self.conn.commit()

    def is_already_in_db(self, word):
        for row in self.cursor.execute('SELECT * FROM wordfreq'):
            decrypted_word = self.hasher.decyrpt_asym_encycryption(row[1])
            print(str(decrypted_word)+"--------------"+word)
            # is_in_db = decrypted_word == word
            # print(is_in_db)
            # if is_in_db:
            #     return True
        return False
