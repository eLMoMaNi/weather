from Weather import Accuweather as Accu
from ImageCombine import ImageCombine
import pickle
# to open all background images in a directory
import os
# to create a json file
import json
# to get day of year
from datetime import datetime

govs_list = {
    "عجلون": 221874,
    "مأدبا": 224575,
    "إربد": 224033,
    "جرش": 224190,
    "المفرق": 222143,
    "عمان": 221790,
    "الزرقاء": 222674,
    "السلط": 221989,
    "الكرك": 222081,
    "الطفيلة": 222569,
    "معان": 224521,
    "العقبة": 221898,
    "التكنو": 224034
}
# Accuweather API token
token = "XiiGZhD2SDOxEKo7eZFlviOgYNTaeZ4P"
# host name to send image url to chatfuel (payload)
host_name = "https://justgeeks.tk/"
# Working dir relative - don't start with "\" - to web server's root (for json file and img)
# note : you should but all of this repo files & dirs there
working_dir = "apis/weather2"

host = host_name+working_dir

# do you love pickles ? I do :). (for debugging)
load_pickle = 0


for gov in govs_list:
    # load pickle or not
    if load_pickle:
        print("WARNING: Using Pickled Weather")
        weather = pickle.load(open("./weather.pickle", "rb"))
    else:
        weather = Accu(token, govs_list[gov], lang="ar")
        pickle.dump(weather, open("./weather.pickle", "wb"))

# background image path
    # directory of background folders
    bg_dir = "/assests/img/backgrounds/"
    # this list will contain image names (eg pic.png)
    bg_list = []
    # loop over all files in current gov folder
    #note os.getcwd() = working dir, since os lib can only take absolute dirs
    for f in os.listdir(os.getcwd()+bg_dir+gov):
        bg_list.append(os.getcwd()+bg_dir+gov+"/"+f)
    # get day of the year
    day_of_year = datetime.now().timetuple().tm_yday
    # get image depending on day of year
    bg_img_path = bg_list[day_of_year % len(bg_list)]
# /end of bg path
    # storing ready image (combined) object
    img = ImageCombine(weather, bg_img_path)
    # saving image
    img.save(f"./outputs/{gov}.png")
    # content of json file (only a single message with gov image)
    json_data = {"messages": [
        {"attachment": {"type": "image", "payload": {"url": host+f"/outputs/{gov}.png"}}}
    ],
                "set_attributes":{"gov_link":weather.link}
    }
    # writing json file
    json_file = open(f"./outputs/{gov}.json", "w", encoding='utf8')
    json.dump(json_data, json_file, ensure_ascii=False)