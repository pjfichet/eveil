from datetime import datetime, timedelta

class Time():

    def __init__(self, game):
        self.game = game
        self.interval = timedelta(seconds=4)
        self.minute = 0
        self.hour = 0
        self.day = 0
        self.month = 0
        self.season = 0
        self.next_tick = datetime.now() + self.interval
        self._get()

    def _get(self):
        gametime = self.game.db.get("gametime")
        if gametime:
            self.minute = gametime['minute']
            self.hour = gametime['hour']
            self.day = gametime['day']
            self.month = gametime['month']
            self.season = gametime['season']

    def _put(self):
        self.game.db.put("gametime", {
                "minute": self.minute,
                "hour": self.hour,
                "day": self.day,
                "month": self.month,
                "season": self.season
            })

    def tick(self):
        now = datetime.now()
        if now >= self.next_tick:
            self.next_tick = self.next_tick + self.interval
            self._minute()
            self._put()

    def _minute(self):
        self.minute += 1
        if self.minute == 60:
            self.minute = 0
            self._hour()

    def _hour(self):
        self.hour += 1
        if self.hour == 24:
            self.hour = 0
            self._day()

    def _day(self):
        self.day += 1
        if self.day == 31:
            self.day = 1
            self._month()

    def _month(self):
        self.month += 1
        if self.month == 4:
            self.month = 1
            self._season()

    def _season(self):
        self.seadon += 1
        if self.season == 5:
            self.season = 1

