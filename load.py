
import json
import os
from datetime import datetime

from user import User
from poops import Poops
from const import USER_DATA_FOLDER


def load_user(id: str) -> User:
    """load user data from USER_DATA_FOLDER/id.json"""
    file_path = f'{USER_DATA_FOLDER}{id}.json'
    with open(file_path, 'r') as f:
        user_data = json.load(f)

    name = user_data['name']

    total = user_data['poops']['total']

    log = {}
    for date in user_data['poops']:
        if date != 'total':
            log[date] = user_data['poops'][date]

    today = str(datetime.today().date())
    if today in log:
        today = log[today]
    else:
        today = 0

    poops = Poops(today, total, log)

    f.close()
    return User(id, name, poops)


def find_file(filename, search_path):
    """look for filename in search_path"""
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def user_exists(id) -> bool:
    """check if id already has a file in player_data"""
    file_path = f'{id}.json'
    if find_file(file_path, USER_DATA_FOLDER) is not None:
        return True
    return False
