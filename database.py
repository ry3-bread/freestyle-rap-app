import sqlite3
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
words_database = os.path.join(base_dir, "words.db")

def create_words_table(conn):
    create_table = """
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL UNIQUE,
            struggled INTEGER DEFAULT 0
        );
    """
    cursor = conn.cursor()
    cursor.execute(create_table)

def create_rhymes_table(conn):
    create_table = """
        CREATE TABLE IF NOT EXISTS rhymes (
            id INTEGER PRIMARY KEY,
            word_id INTEGER NOT NULL,
            rhyme TEXT NOT NULL,
            FOREIGN KEY (word_id) REFERENCES words(id)
        );
    """
    cursor = conn.cursor()
    cursor.execute(create_table)

def add_word(conn, word):
    sql = """
        INSERT INTO words (word)
        VALUES (?)
    """
    cur = conn.cursor()
    try:
        cur.execute(sql, (word,))
        return cur.lastrowid
    except sqlite3.IntegrityError:
        pass # LEFT OFF HERE

def add_rhyme(conn, rhyme, word_id):
    sql = """
        INSERT INTO rhymes (word_id, rhyme)
        VALUES (?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, (word_id, rhyme))

def edit_database():
    pass

def initialize_database():
    try:
        with sqlite3.connect(words_database) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            create_words_table(conn)
            create_rhymes_table(conn)
    except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

if __name__ == "__main__":
    initialize_database()
