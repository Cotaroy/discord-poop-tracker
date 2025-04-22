
from dataclasses import dataclass
from user import User
from quick_sort import quicksort


def _get_user_today_poop(user: User) -> int:
    """return user poops today"""
    return user.poops.today


def _get_user_total_poop(user: User) -> int:
    """return total user poop"""
    return user.poops.total


def _get_user_date_poop(user: User, date: str) -> int:
    """return total user poop"""
    if date not in user.poops.log:
        return 0
    return user.poops.log[date]


@dataclass
class Leaderboard:
    """Leader Board of Users"""
    users: list[User]

    def __str__(self):
        """Note this is not sorted in any order."""
        output = '-------------------------'

        for user in self.users:
            build_line = f'\n{user.name} -> {str(user.poops)}'
            output += build_line

        return output

    def get_total_leaderboard(self):
        """show total leaderboard"""
        output = 'Total Poop Leaderboard \n-------------------------'

        self._sort_by_poop()

        for i in range(len(self.users)):
            build_line = f'\n[1] -> {self.users[i].name}: {self.users[i].poops.total}'
            output += build_line

        return output

    def get_today_leaderboard(self):
        """show today's leaderboard"""
        output = "Today's Poop Leaderboard \n-------------------------"

        self._sort_by_poop('today')

        for i in range(len(self.users)):
            build_line = f'\n[1] -> {self.users[i].name}: {self.users[i].poops.today}'
            output += build_line

        return output

    def get_date_leaderboard(self, date: str):
        """
        show leaderboard on date
        """
        date_set = {set(user.poops.log.keys()) for user in self.users}
        final = set()
        for days in date_set:
            final.union(days)
        if date not in date_set:
            return "No one has pooped on that day."

        output = f"{date} Poop Leaderboard \n-------------------------"

        self._sort_by_poop(date)

        for i in range(len(self.users)):
            if date in self.users[i].poops.log:
                build_line = f'\n[1] -> {self.users[i].name}: {self.users[i].poops.log[date]}'
                output += build_line

        return output

    def get_total_poops(self):
        """return total poops from all users"""
        sum = 0
        for user in self.users:
            sum += user.poops.total
        return sum

    def _sort_by_poop(self, date: str = 'total'):
        """
        mutate self.users so that users are sorted

        Preconditions:
        range in {'today', 'total}
        """
        if date == 'today':
            val = _get_user_today_poop
        elif date == 'total':
            val = _get_user_total_poop
        else:
            val = _get_user_date_poop

        quicksort(self.users, 0, len(self.users), val, reverse=True)
