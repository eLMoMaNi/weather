import requests
import datetime


class Accuweather:
    def __init__(self, token, city, lang="ar"):
        # Fetch current week day
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
            str(city)
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
                print(self.today)
                self.today += 1

    def print(self):
        print(self.res.status_code)
        print(self.forecasts)
