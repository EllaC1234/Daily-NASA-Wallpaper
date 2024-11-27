import requests
import subprocess
import os
import ctypes

def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{image_path}" , 0)


def get_apod_image():
    api_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": "DEMO_KEY"
    }

    response = requests.get(api_url, params)

    if response.status_code == 200:
        image_url = response.json()['url']
        response = requests.get(image_url)

        with open("./nasa_apod_image.jpg", "wb") as f:
            f.write(response.content)
        
        set_wallpaper("nasa_apod_image.jpg")
        # os.remove("nasa_apod_image.jpg")

get_apod_image()