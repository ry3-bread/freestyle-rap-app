import sqlite3
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
words_database = os.path.join(base_dir, "words.db")

def get_connection():
    return sqlite3.connect(words_database)

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
            UNIQUE(word_id, rhyme),
            FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
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
        cur.execute('SELECT id FROM words WHERE word = ?', (word,))
        return cur.fetchone()[0]

def add_rhyme(conn, rhyme, word_id):
    sql = """
        INSERT OR IGNORE INTO rhymes (word_id, rhyme)
        VALUES (?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, (word_id, rhyme))


def edit_database():
    pass

def get_word(conn, word_id):
    cur = conn.cursor()
    cur.execute("SELECT id, word FROM words where id = ?", (word_id,))
    return cur.fetchone()

def get_rhymes(conn, word_id):
    cur = conn.cursor()
    cur.execute("SELECT id, rhyme FROM rhymes where word_id = ?", (word_id,))
    return cur.fetchall()

def get_all_words(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, word FROM words")
    return cur.fetchall()

def rename_word(conn, word_id, new_name):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE words SET word = ? WHERE id = ?", (new_name, word_id))
        return True
    except sqlite3.IntegrityError:
        return False

def delete_word(conn, word_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM words WHERE id = ?", (word_id,))

def delete_rhyme(conn, rhyme_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM rhymes WHERE id = ?", (rhyme_id,))

def initialize_database():
    try:
        with sqlite3.connect(words_database) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            create_words_table(conn)
            create_rhymes_table(conn)
    except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

if __name__ == "__main__":
    initialize_database()
