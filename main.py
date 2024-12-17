import requests
import logging
import os
import ctypes
import subprocess
import random
import datetime

def get_random_date(start_year=1996, end_year=2024):
    return datetime.date(random.randint(start_year, end_year), random.randint(1, 12), random.randint(1, 28))


def fetch_image_data(endpoint, endpoint_params):
    try:
        responseJson = {}
        iteration = 1

        while "hdurl" not in responseJson:
            if iteration != 1:
                date = get_random_date()
                endpoint_params["start_date"] = endpoint_params["end_date"] = date 

            response = requests.get(endpoint, endpoint_params)
            response.raise_for_status()

            if "start_date" in endpoint_params or "end_data" in endpoint_params:
                responseJson = response.json()[0]
            else:
                responseJson = response.json()

            iteration += 1

        return responseJson["hdurl"]
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def download_image(image_url, filename):
    response = requests.get(image_url)

    with open(filename, "wb") as f:
        f.write(response.content)


def set_wallpaper(image_path, style):
    powershell_cmd = f"""
        Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop" -Name WallpaperStyle -Value {style} -Force
        RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters 1, True
    """

    process = subprocess.Popen(["powershell", "-Command", powershell_cmd])
    process.wait()

    full_path = os.path.join(os.getcwd(), image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 0)


def main(endpoint, params, filename, style):
    logging.basicConfig(filename='daily_image_error.log', level=logging.ERROR)

    image_url = fetch_image_data(endpoint, params)
    if image_url:
        download_image(image_url, filename)
        set_wallpaper(filename, style)


if __name__ == "__main__":
    api_key = os.environ.get('NASA_APOD_API_KEY') or "DEMO_KEY"
    endpoint = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key
    }
    filename = "nasa_apod_image.jpg"
    style = 6

    main(endpoint, params, filename, style)