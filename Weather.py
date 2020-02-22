# to send a GET request
import requests
# to get day date as a number
import datetime

govs = {
    "عجلون": 221874,
    "مأدبا": 224575,
    "إربد": 224033,
    "جرش": 224190,
    "المفرق": 222143,
    "عمّان": 221790,
    "الزرقاء": 222674,
    "السلط": 221989,
    "الكرك": 222081,
    "الطفيله": 222569,
    "مَعان": 224521,
    "العقبة": 221898,
}


class Accuweather:
<<<<<<< HEAD
    def __init__(self, token, city_id, lang="ar"):
=======
    def __init__(self, token, city, lang="ar"):
        # Fetch current week day
>>>>>>> a3a7d28dd5eba0f91a3ebbfe0cf3701570516da6
        self.today = int(datetime.datetime.today().strftime('%w'))
        # Since self.today is guaranteed to be 0-6 map the integers to actual days
        self.days_in_week = {
            0: "الأحد",
            1: "اللإثنين",
            2: "الثلاثاء",
            3: "الأربعاء",
            4: "الخميس",
            5: "الجمعة",
            6: "السبت"
        }
        # Initializing the request
        URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + \
            str(city_id)
        options = {
            "apikey": token,
            "language": lang,
            "metric": True
        }
        # Sending the GET request
        self.res = requests.get(URL, params=options)
        # Checking the response status
        if self.res.status_code != 200:
            print("ERROR, status code:")
            print(self.res.status_code)
            print("URL:\n"+self.res.url)
            raise Exception()
        # Storing the data in the format day/night :temp,icon,text
        else:
            # Storing json into a Dictionary
            self.dic = self.res.json()
            # The "more details" link
            self.link = self.dic["Headline"]["MobileLink"]
            # Initializing forecasts array
            self.forecasts = []
            for i in range(5):
                # Day
                self.forecasts.append(
                    {
                        "day":
                        {
                            "temp": str(int(self.dic["DailyForecasts"][i]["Temperature"]["Maximum"]["Value"]))+"°",
                            "icon": self.dic["DailyForecasts"][i]["Day"]["Icon"],
                            "text": self.dic["DailyForecasts"][i]["Day"]["IconPhrase"]
                        },
                        "night":
                        {
                            "temp": str(int(self.dic["DailyForecasts"][i]["Temperature"]["Minimum"]["Value"]))+"°",
                            "icon": self.dic["DailyForecasts"][i]["Night"]["Icon"],
                            "text": self.dic["DailyForecasts"][i]["Night"]["IconPhrase"]
                        },
                        "weekday": self.days_in_week[self.today % 7]
                    }
                )
                self.today += 1

    def print(self):
        print(self.res.status_code)
        print(self.forecasts)
