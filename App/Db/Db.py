import sqlite3
from Utils.EncryptionManager import EncryptionManager


class AppDB:
    '''This class is responsible for maintaning database for App'''

    def __init__(self):
        self.conn = sqlite3.connect('Db/wordfreq.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        self.encry_manager = EncryptionManager()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wordfreq
             (id text, word text, freq real)''')
        self.conn.commit()

    def insert_row(self, words_list):
        for word, freq in words_list[:100]:
            if self.is_already_in_db(word):
                self.update_row(word, freq)
            else:
                w_id = self.encry_manager.generate_salted_hash(word)
                encrypted_word = (
                    self.encry_manager.generate_asym_encryption(word))
                self.cursor.execute(
                    'INSERT INTO wordfreq VALUES ("{}","{}","{}")'.format(
                        w_id, encrypted_word, freq
                    ))
                self.conn.commit()

    def update_row(self, word, freq):
        w_id = None
        result = self.cursor.execute(
                'SELECT * FROM wordfreq')
        for row in result:
            if self.encry_manager.match_salted_hash(row[0], word):
                w_id = row[0]
        result = self.cursor.execute(
                'SELECT * FROM wordfreq where id="{}"'.format(
                    w_id))
        for row in result:
            self.cursor.execute(
                'UPDATE wordfreq SET freq="{}" where id="{}"'.format(
                    freq + row[2], w_id
                    ))
            self.conn.commit()

    def is_already_in_db(self, word):
        for row in self.cursor.execute('SELECT * FROM wordfreq'):
            decrypted_word = (
                self.encry_manager.decyrpt_asym_encycryption(row[1]))
            if decrypted_word == word:
                return True
        return False

    def get_all_data(self):
        decrypted_data = []
        for row in self.cursor.execute('SELECT * FROM wordfreq'):
            decrypted_word = (
                self.encry_manager.decyrpt_asym_encycryption(row[1]))
            decrypted_data.append([decrypted_word, row[2]])
        return decrypted_data
