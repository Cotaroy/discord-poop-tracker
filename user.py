
from poops import Poops
from const import USER_DATA_FOLDER
import json


class User:
    """The User Class"""
    id: str
    name: str
    poops: Poops

    def __init__(self, id, name, poops=None):
        if poops is None:
            poops = Poops()

        self.id = id
        self.name = name
        self.poops = poops

    def log_poop(self, n: int):
        """log n poops"""
        self.poops.log_poop(n)
        return f'Your poop count has increased by {n}.'

    def save(self):
        """save user data into USER_DATA_FOLDER"""
        file_path = f"{USER_DATA_FOLDER}{self.id}.json"
        with open(file_path, 'w') as f:
            dict = self._to_json_dict()
            json.dump(dict, f, **{"indent": 4})
            f.close()

    def get_poop_count(self, date: str = 'total'):
        """
        get poop count on date

        date in {'today', 'total'} or is YYYY-MM-DD
        """
        date = date.replace('/', '-')
        if date == 'today':
            output = self.poops.today
        elif date == 'total':
            output = self.poops.total
        elif date not in self.poops.log:
            output = 0
        else:
            output = self.poops.log[date]
        return output

    def _to_json_dict(self):
        dict = {"id": f"{self.id}",
                "name": f"{self.name}",
                "poops": {"total": self.poops.total}
                }

        for date in self.poops.log:
            dict["poops"][date] = self.poops.log[date]
        return dict
