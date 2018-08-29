import sqlite3


class AppDB:
    '''This class is responsible for maintaning database for App'''

    def __init__(self):
        self.conn = sqlite3.connect('Db/wordfreq.db')
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wordfreq
             (id text, word text, freq real)''')
        self.conn.commit()

    def insert_row(self, words_list):
        pass
