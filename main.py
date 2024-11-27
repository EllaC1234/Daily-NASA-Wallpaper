import requests
import logging
import os
import ctypes
import subprocess

def set_wallpaper(image_path, style):
    powershell_cmd = f"""
        Set-ItemProperty -Path "HKCU:\\Control Panel\\Desktop" -Name WallpaperStyle -Value 6 -Force
        RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters 1, True
    """

    process = subprocess.Popen(["powershell", "-Command", powershell_cmd])
    process.wait()

    full_path = os.path.join(os.getcwd(), image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 0)


def download_image(image_url, filename):
    response = requests.get(image_url)

    with open(filename, "wb") as f:
        f.write(response.content)


def fetch_image_data(endpoint, endpoint_params):
    try:
        response = requests.get(endpoint, endpoint_params)
        response.raise_for_status()

        return response.json()[0]['hdurl']
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def main(endpoint, params, filename, style):
    logging.basicConfig(filename='daily_image_error.log', level=logging.ERROR)

    image_url = fetch_image_data(endpoint, params)
    if image_url:
        download_image(image_url, filename)
        set_wallpaper(filename, style)

if __name__ == "__main__":
    api_key = os.environ.get('NASA_APOD_API_KEY')
    if not api_key:
        api_key = "DEMO_KEY"

    endpoint = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "start_date": "2024-11-26",
        "end_date": "2024-11-26"
    }
    filename = "nasa_apod_image.jpg"
    style = 6

    main(endpoint, params, filename, style)