from datetime import datetime, timedelta
import random

WEATHER = {
    's': "sunny",
    'c': "cloudy",
    'f': "foggy",
    'd': "drizzling",
    'r': "raining",
    'h': "showering",
    'n': "snowing",
    'o': "oraging",
}

CHAINS = [
    "rscncscnncssrrccfccrccccncsccns", # january
    "ssscrccsrnnnccsnrsrssdccccsr", # february
    "ssrcssscccccsscsccsdddscdcccsod", # march
    "ssdcccccccsccsscssscssdsssssss", # april
    "sddhrcccdrrrddcccssssssssssrsdr", # may
    "cdssssssccsssrdrsrcdcssscsssss", # june
    "ssssscssssscsssssssscccssccscss", # july
    "shcscssssssosshcscscscccsshssss", # august
    "scsssccsrsssssscsdsssssorccssc", # september
    "ssshssssscrssssddcssccsrdssssrh", # october
    "csscscrcddcdsrhccssrscccccncsc", # november
    "ccnsnrcdsssssscsnsnfddrncscdsfc", # december
]



class Time():

    def __init__(self, game):
        self.game = game
        self.interval = timedelta(seconds=4)
        self.minute = 0
        self.hour = 0
        self.day = 1
        self.month = 1
        self.season = 1
        self.weather = ('s', 's')
        self.next_tick = datetime.now() + self.interval
        self._get()
        self.models = []
        for chain in CHAINS:
            self.models.append(self._modelize(chain))

    def _log(self):
        self.game.log("Game time: {}-{} {}:{}, {}.".format(
            self.month, self.day, self.hour, self.minute,
            WEATHER[self.weather[1]],
            ))

    def _get(self):
        gametime = self.game.db.get("gametime")
        if gametime:
            self.minute = gametime['minute']
            self.hour = gametime['hour']
            self.day = gametime['day']
            self.month = gametime['month']
            self.season = gametime['season']
            self.weather = gametime['weather']
        self._log()

    def _put(self):
        self.game.db.put("gametime", {
                "minute": self.minute,
                "hour": self.hour,
                "day": self.day,
                "month": self.month,
                "season": self.season,
                "weather": self.weather,
            })

    def _modelize(self, chain):
        model = {}
        l1 = ''
        l2 = ''
        for letter in chain + chain:
            model.setdefault( (l1, l2), []).append(letter)
            l1, l2 = l2, letter
        return model 

    def _change_weather(self):
        month = self.month -1
        model = self.models[month]
        # It may be possible that this key is not in the model
        if self.weather in model:
            weather = random.choice(model[ self.weather ])
        else:
            weather = weather[1]
        self.weather = (self.weather[1], weather)

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
        self._change_weather()
        self._log()

    def _month(self):
        self.month += 1
        if self.month == 4:
            self.month = 1
            self._season()

    def _season(self):
        self.seadon += 1
        if self.season == 5:
            self.season = 1

