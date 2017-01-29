""" settings.py - Configuration for the LibCal bot """

""" List of Rooms in the calendar.

room: Friendly name of room.

index: index position for SID generation. This is usually a sequence in they
order rooms appear in the calendar. May change if rooms have been added or
removed from the calendar since its creation

Min and max cap data is enforced at our library, but doesn't seem to be part
of LibCal.

min_cap: Minimum group size for booking the room. Currently unused.
max_cap: Maximim group size for the room. Currently unused.

preference: When selecting a room to book, rooms are selected in preference
order. (Lowest first.) Shared preference threshold will lead to one of the set
being selected. Depends on the order of the sorted operation.

"""

room_src = [
    {"room":"A", "index":0, "min_cap":7, "max_cap":14, "preference":2},
    {"room":"B", "index":1, "min_cap":2, "max_cap":10, "preference":1},
    {"room":"C", "index":2, "min_cap":2, "max_cap":6, "preference":3}
]

""" Maximum index value

This may well be larger than the maximum room index. Identified by how the
timestamp rolls over from one day to the next.
"""
max_index = 4

""" URL of the process_roombooking.php file """
process_url = "http://libcal.example.org/process_roombookings.php"

""" URL of the user interface for booking """
referer_url = "http://libcal.example.org/booking/"

""" Name to use when placing bookings """
name = "My Name"

""" Email to use when placing bookings """
email = "user@example.org"

""" Session name to use when placing bookings """
session_name = "My Booking"

""" Calendar GID to use """
gid = 0000

""" Epoch for most hours. """

""" Epoch time - full ISO8601 datestamp for the start time. """
epoch_time = "2017-01-01T00:00:00+0000"

""" Epoch SID - the SID at the epoch_time. """
epoch_sid = 123456789
