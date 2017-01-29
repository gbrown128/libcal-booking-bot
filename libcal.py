7#! /usr/bin/env python3

import datetime
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import re

# Local settings file.
import settings

def write_success_message(booking_link, booking):
    # Regex magic pulls out details about the booking made.
    booking_info = re.search(
        "(Room \w{2,4}) .*, (\d{2}:\d{2}.+?), (.*)",
        booking_link['title']
    )

    # Nice message for the status notifier.
    nice_message = (
        "I've booked "
        + booking_info.group(1)
        + " for you, from "
        + booking_info.group(2)
        + " on "
        + booking_info.group(3)
        + "\n"
    )

    # Write the message to file.
    with open('status', 'a') as logfile:
        logfile.write(nice_message)

def write_failure_message(booking_link, booking):
    # Regex magic pulls out details about the booking made.
    booking_info = re.search(
        "(Room \w{2,4}) .*, (\d{2}:\d{2}.+?), (.*)",
        booking_link['title']
    )

    # Nice message for the status notifier.
    nice_message = (
        "I tried to book "
        + booking_info.group(1)
        + " for you, from "
        + booking_info.group(2)
        + " on "
        + booking_info.group(3)
        + ". Unfortunatley it failed. Response was: ```"
        + booking.content.decode()
        + "```\n"
    )

    # Write the message to file.
    with open('status', 'a') as logfile:
        logfile.write(nice_message)

def make_booking(time):
    # Get the calendar data for the day to make the booking.
    caldata = get_caldata(time)
    # Get the epoch for the day, so we can look for bookings.
    epoch = get_epoch(caldata)

    # Sort rooms by preference.
    sorted_rooms = sorted(settings.room_src, key=lambda k: k['preference'])

    booking_sid = -1

    # Search for available bookings.
    for room in sorted_rooms:
        print(room['index'])
        target_booking = epoch + (23*room['index'] + time.hour)
        booking_link = caldata.find('a', id=target_booking)
        if(booking_link):
            booking_sid = target_booking
            break

    if(booking_sid == -1):
        return 1

    # Prepare the form data for the booking.
    booking_payload = {
        'sid':booking_sid,
        'tc':"done",
        'gid':settings.gid,
        'name':settings.name,
        'email':settings.email,
        'nick':settings.session_name,
        'qcount':"0",
        'fid':"0"
    }

    request_url = settings.process_url + '?m=booking_full'

    # Make the POST request with the form data.
    # Requires Referer to go through properly.

    booking = requests.post(
        request_url,
        data=booking_payload,
        headers={'Referer': settings.referrer_url}
    )

    if booking.content == "0":
        # Success
        write_success_message(booking_link, booking)
    else:
        write_failure_message(booking_link, booking)

def get_caldata(date):
    # Payload for calendar data request.
    caldata = {
        "m": "calscroll",
        "gid": settings.gid,
        "date": date.strftime("%Y-%m-%d")
    }

    # Request the calendar data from the website.
    request_url = settings.process_url + "?" + urlencode(caldata)

    # Verify the web request went ok.
    try:
        caldata_src = requests.get(request_url)
    except:
        print("Page request failure: " + request_url)
        return(-1)

    if caldata_src.status_code != 200:
        print(
             "Page request failure: "
             + str(caldata_src.status_code)
             + " requesting: "
             + request_url
        )
        return(-1)

    # Parse the HTML out to make it more manageable.
    soup = BeautifulSoup(caldata_src.content, 'html.parser')

    # From the calendar table, return the first free session (first link)
    caldata = soup.find('div', id='time_grid_scroll')

    return(caldata)

def get_epoch(caldata):
    # From the calendar table, return the first free session (first link)
    first_free = caldata.a

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
    time = datetime.datetime(2017,2,10,16)
    make_booking(time)

if __name__ == "__main__":
    main()
