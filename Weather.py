import requests
import datetime

class Accuweather:
    def __init__(self, token, city, lang="ar"):
        self.today = int(datetime.datetime.today().strftime('%w'))
        self.days_in_week = {  
            0:"الأحد",
            1:"اللإثنين",
            2:"الثلاثاء",
            3:"الأربعاء",
            4:"الخميس",
            5:"الجمعة",
            6:"السبت"
        }
        # initializing the request
        URL = "http://dataservice.accuweather.com/forecasts/v1/daily/10day/" + \
            str(city)
        options = {
            "apikey": token,
            "language": lang,
            "metric": True
        }
        # sending the POST request
        self.res = requests.post(URL, params=options)
        # checking the response status
        if self.res.status_code != 200:
            print("ERROR, status code:")
            print(self.res.status_code)
            print("URL:\n"+self.res.url)
            self.res.content
        # stroing the data on the format day/night :temp,icon,text
        else:
            # stroing json into a Dictionary
            self.dic = self.res.json()
            # the "more details" link
            self.link = self.dic["Headline"]["MobileLink"]
            # initializing forecasts array
            self.forecasts = []
            for i in range(7):
                # Day
                self.forecasts.append(
                    {
                        "day":
                        {
                            "temp":str(int(self.dic["DailyForecasts"][i]["Temperature"]["Maximum"]["Value"])),
                            "icon":self.dic["DailyForecasts"][i]["Day"]["Icon"],
                            "text":self.dic["DailyForecasts"][i]["Day"]["IconPhrase"]
                        },
                        "night":
                        {
                            "temp":str(int(self.dic["DailyForecasts"][i]["Temperature"]["Minimum"]["Value"])),
                            "icon":self.dic["DailyForecasts"][i]["Night"]["Icon"],
                            "text":self.dic["DailyForecasts"][i]["Night"]["IconPhrase"]
                        },
                        "weekday":self.days_in_week[self.today%7]
                    }
                )
                print(self.today)
                self.today+=1
# /_end of __init__()

    def print(self):
        print(self.res.status_code)
        print(self.forecasts)