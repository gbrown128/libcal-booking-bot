# libcal-booking-bot
A bot to make room booking requests via Springshare's LibCal system.

This bot has been developed without any inside knowledge of the LibCal system. 
I have developed it with only user side access to the University of 
Southampton's LibCal system. Hopefully it will prove useful to somebody else 
in the future though!

# How LibCal Works

The core of LibCal is the `process_roombookings.php` file. Obtaining booking 
availabilities and placing bookings is done by GET requests to this file.

There are three request types I am currently aware of. The request type is set 
by the `m` field in the request.

* `showNick` - Return the current confirmed bookings. Seems to populate the 
table below the calendar.

 * `gid` - The ID of the calendar to request bookings from.
 * `d` - The day to request data about, i.e. `2017-01-25`.

* `calscroll` - Return the list of rooms, notes about those rooms, and the 
calendar body as a table of hyperlinks to sessions.

 * `gid` - The ID of the calendar to request bookings from.
 * `date` - The day to request data about, i.e. `2017-01-25`. (Note the change 
   from just `d` above!)

* `booking_full` - Places a booking request.
 * `sid` - The 9-digit 'session' identifier which refers to the room, and the 
   hour. See the [Session Identifiers](#session-identifiers) section. Multiple session 
   identifiers can be selected using a `|` between each one.
 * `tc = done` - Not sure about this one.
 * `gid` - The ID of the calendar to request bookings from.
 * `name = Your+Name` - The name on the booking.
 * `email = name@example.org` - The email where confirmation requests will be sent.
 * `nick = My+Event` - Name of your event. (Publicly visible once confirmed.)
 * `qcount = 0` - Unknown.
 * `fid = 0` - Unknown.

# Session Identifiers

Session identifiers seem to be mostly sane, but I haven't quite figured them out yet!

At Southampton, the library rooms are available for booking 24 hours a day, 7 
days a week. Each booking session is 1 hour long. Things may well be different 
elsewhere.

Session identifiers are 9-digit decimal numbers.

Every room gets a sequential set of **23** SIDs, each corresponding to the 
hour starting 00:00 - 22:00. The next room in the set continues where the 
sequence left off, 00:00 - 22:00. The session ID seems to be based on some 
epoch, but I haven't been able to collect enough data to confirm this yet!

*SIDs in the following section are not real, just examples.*

For example, room 1 at 00:00 has a SID of 157260320, and the same room at 
22:00 has SID 157260342. Room 2 at 00:00 continues the sequence starting at 
157260343. This sequence continues for all rooms.

The next day, room 1 at 00:00 continues the sequence where the last room at 
22:00 left off.

The 23:00 SIDs are seemingly a somewhat separate sequence, with an offset 
epoch.

For example room 1, at 23:00 may have an SID of 157200455. Room 2 will be next 
in the sequence at 157200456. This pattern again continues for all rooms in 
the calendar. Room 1 continues the sequence the next day.

One important note is that SIDs are still generated for rooms that are not 
shown in the calendar. At some point before my time, two of the bookable rooms 
were either removed or renamed. It seems that SIDs are being generated for 
these rooms regardless, which leads to a discontinuity in both the SID 
sequences.

