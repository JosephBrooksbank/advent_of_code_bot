import requests
import json
import dotenv
import os
import unittest
import logging
import sqlite

dotenv.load_dotenv()
url = os.getenv("LEADERBOARD_URL")
session_cookie = os.getenv("SESSION_COOKIE")

def get_new_leaderboard():
    headers = {
        "Cookie": f"session={session_cookie}"
    }
    response = requests.get(url, headers=headers)

    try:
        board = json.loads(response.text)
        return board
    except json.JSONDecodeError:
        logging.error("Failed to get leaderboard, likely due to invalid session cookie")
        return None

def get_leaderboard():
    db = sqlite.Sqlite()
    leaderboard = db.get_leaderboard_from_db()
    if leaderboard:
        return leaderboard
    else:
        new_leaderboard = get_new_leaderboard()
        db.insert_leaderboard(new_leaderboard)
        return new_leaderboard

def refresh_leaderboard():
    db = sqlite.Sqlite()
    new_leaderboard = get_new_leaderboard()
    db.insert_leaderboard(new_leaderboard)
    return new_leaderboard


def get_days_completed(user_id):
    leaderboard = get_leaderboard()
    days = []
    for member in leaderboard["members"]:
        if member == user_id:
            completion_day_level = leaderboard["members"][member]["completion_day_level"]
            for day  in completion_day_level:
                days.append(f"day-{day}")

    return days

class Tests(unittest.TestCase):

    def test_leaderboard(self):
        leaderboard = get_leaderboard()
        self.assertTrue("members" in leaderboard)

    def test_days_completed(self):
        user_id = '3565071'
        days = get_days_completed(user_id)
        self.assertTrue(len(days) > 0)

