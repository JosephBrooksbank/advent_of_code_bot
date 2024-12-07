import sqlite3
import time
import unittest
import json

class Sqlite:
    def __init__(self):
        self.conn = sqlite3.connect('aoc.sqlite')
        self.c = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS discord_aoc 
            (discord_id text, aoc_id text, aoc_name text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS aoc_leaderboard_cache 
            (leaderboard text, timestamp text)''')
        self.conn.commit()

    def insert_user(self, discord_id, aoc_id, aoc_name):
        self.c.execute("INSERT INTO discord_aoc VALUES (?, ?, ?)", (discord_id, aoc_id, aoc_name))
        self.conn.commit()

    def get_leaderboard_from_db(self):
        res = self.c.execute("SELECT leaderboard, timestamp FROM aoc_leaderboard_cache")
        board = res.fetchone()
        if board:
            if (time.time() - float(board[1])) < 60 * 15:
                return json.loads(board[0])
        return None

    def insert_leaderboard(self, leaderboard):
        self.c.execute("DELETE FROM aoc_leaderboard_cache")
        timestamp = time.time()
        leaderboard = json.dumps(leaderboard)
        self.c.execute("INSERT INTO aoc_leaderboard_cache VALUES (?, ?)", (leaderboard, timestamp))
        self.conn.commit()

    def get_discord_user(self, discord_id):
        res = self.c.execute("SELECT aoc_id, aoc_name FROM discord_aoc WHERE discord_id = ?", (discord_id,))
        return res.fetchone()


class Tests(unittest.TestCase):

    def test_create_tables(self):
        db = Sqlite()
        db.create_table()
        self.assertTrue(True)