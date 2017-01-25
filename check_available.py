#! /usr/bin/env python3

from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup

# Local settings file.
import settings

date = "2017-02-03"
time = "15"

# Dict of data for formatting the request.
caldata = {
    "m": "calscroll",
    "gid": settings.gid,
    "date": date
}

def main():
    # Build the GET request URL.
    request_url = settings.process_url + "?" + urlencode(caldata)

    try:
        cal_data = requests.get(request_url)
    except:
        print("Page request failure: " + request_url)
        exit()

    if cal_data.status_code != 200:
        print(
             "Page request failure: "
             + str(cal_data.status_code)
             + " requesting: "
             + request_url
         )
    else:
        print(cal_data.content)

if __name__ == "__main__":
    main()
