#! /usr/bin/env python3

from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import re

# Local settings file.
import settings

def get_epoch(date):
    # Payload for calendar data request.
    caldata = {
        "m": "calscroll",
        "gid": settings.gid,
        "date": date
    }

    # Request the calendar data from the website.
    request_url = settings.process_url + "?" + urlencode(caldata)

    # Verify the web request went ok.
    try:
        cal_data = requests.get(request_url)
    except:
        print("Page request failure: " + request_url)
        return(-1)

    if cal_data.status_code != 200:
        print(
             "Page request failure: "
             + str(cal_data.status_code)
             + " requesting: "
             + request_url
        )
        return(-1)

    # Parse the HTML out to make it more manageable.
    soup = BeautifulSoup(cal_data.content, 'html.parser')

    # From the calendar table, return the first free session (first link)
    first_free = soup.find('div', id='time_grid_scroll').a

    # Pick out the room name and the start time of the session.
    # It's likley these will require tuning for your instiution!
    room_name = re.search('Room (.*) \(', first_free['onclick']).group(1)
    session_start = re.search('(\d{2}):\d{2}', first_free.decode()).group(1)

    # Select the session ID for the first free session.
    first_sid = int(first_free['id'])

    # Find the index of the room with the first availability.
    for room in settings.room_src:
        if room_name in room['room']:
            epoch_room_idx = room['index']
            break

    # Compute the epoch for the very start of the day.
    day_epoch = first_sid - (23*epoch_room_idx+int(session_start))
    return(day_epoch)

def main():
    print(get_epoch("2017-01-31"))

if __name__ == "__main__":
    main()
