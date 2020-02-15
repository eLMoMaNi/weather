import requests


class Accuweather:
    def __init__(self, token, city, lang="ar"):
        # initializing the request
        URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + \
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
            self.forecasts = [{
                "day": {"temp": 0, "icon": 0, "text": ""},
                "night": {"temp": 0, "icon": 0, "text": ""}
            }] * 5
            for i in range(5):
                # Day
                self.forecasts[i]["day"]["temp"] = self.dic["DailyForecasts"][i]["Temperature"]["Maximum"]["Value"]
                self.forecasts[i]["day"]["icon"] = self.dic["DailyForecasts"][i]["Day"]["Icon"]
                self.forecasts[i]["day"]["text"] = self.dic["DailyForecasts"][i]["Day"]["IconPhrase"]
                # Night
                self.forecasts[i]["night"]["temp"] = self.dic["DailyForecasts"][i]["Temperature"]["Minimum"]["Value"]
                self.forecasts[i]["night"]["icon"] = self.dic["DailyForecasts"][i]["Night"]["Icon"]
                self.forecasts[i]["night"]["text"] = self.dic["DailyForecasts"][i]["Night"]["IconPhrase"]
# /_end of __init__()

    def print(self):
        print(self.res.status_code)
        print(self.forecasts)
