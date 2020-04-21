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
token = "GetYourOwn"
# Host name to send image url to chatfuel (payload)
host_name = "https://justgeeks.tk/"
# Working dir relative - don't start with "\" - to web server's root (for json file and img)
# Note: Put all of this repo files & dirs there
working_dir = "apis/weather2"

host = host_name+working_dir

# load_pickle: set 0 to not load pickle, 1 to load
load_pickle = 0

for gov in govs_list:
    # Load pickle or not
    if load_pickle:
        print("WARNING: Using Pickled Weather")
        with open("weather.pickle","rb") as f:
            weather = pickle.load(f)
    else:
        weather = Accu(token, govs_list[gov], lang="ar")
        with open("weather.pickle","wb") as f:
            pickle.dump(weather,f)
# Background image path
    # Directory of background folders
    bg_dir = "/assests/img/backgrounds/"

    # This list will contain image names (eg pic.png)
    bg_list = []

    # Loop over all files in current gov folder
    # Note: os.getcwd() = working dir, since os lib can only take absolute dirs
    for f in os.listdir(os.getcwd()+bg_dir+gov):
        bg_list.append(os.getcwd()+bg_dir+gov+"/"+f)

    # Get day of the year
    day_of_year = datetime.now().timetuple().tm_yday

    # Get image depending on day of year
    bg_img_path = bg_list[day_of_year % len(bg_list)]
# End of bg path
    # Storing ready (combined) image object
    img = ImageCombine(weather, bg_img_path)
    # Saving image
    img.save("outputs/{}.png".format(gov))
    # content of json file (only a single message with gov image)
    json_data = {"messages": [
        {"attachment": {"type": "image", "payload": {"url": host+"/outputs/{}.png".format(gov)}}}
    ],
                "set_attributes":{"gov_link":weather.link}
    }
    # Writing json file
    with open("outputs/{}.json".format(gov), "w", encoding='utf8') as json_file:
        json.dump(json_data, json_file, ensure_ascii= False)
