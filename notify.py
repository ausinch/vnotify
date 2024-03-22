#!/usr/bin/python3
#  Creates verbal notifications leading up to events
#  by Chris Sullivan
#  verison 0.1 - Created
#  :r!date Su Mar 14 22:00:57 CET 2021
#  version 0.2 - add base notification creation
#  Do 14 Mär 2024 08:15:19 CET

# prerequisits
#sudo apt install python3-pip mpg123 at
#sudo pip install gtts

from gtts import gTTS
import os
import datetime

# test for mpg123 command in the os
app_check = os.popen('whereis mpg123').read()
if app_check.count('mpg123') == 1:
    print("Application mpg123 is needed to run this application.\nPlease install it then try again.\n")
    quit()

app_check = os.popen('whereis at').read()
if app_check.count('at') == 1:
    print("Application at is needed to run this application.\nPlease install it then try again.\n")
    quit()

#  check if base files exist
if not os.path.exists("base/in_30_minutes.mp3"):
    # now create the base MP3 files
    tts = gTTS(text='%s' % the_event, lang='en')
    tts.save("%s" % the_file)



the_event = input ("Enter event text: ")
# enter in the time for the alert. It must be in hhmm format
the_time = input ("When (hh:mm): ")
# check format; numeric only, size 4, 0-24:0-60
# check if this is in the future
now = datetime.datetime.now()
new_time = datetime.datetime.strptime(the_time,'%H:%M').time()
# put into the same format as now
new_time = datetime.datetime.combine(now, new_time)
time_delta = new_time - now
delta_minutes = time_delta.total_seconds() / 60
if delta_minutes < 1:
    print("Sorry. this is in the past")
    #sys.exit("Terminating")
    quit()

# does the mp3 file already exist? no - create it.
the_file = "%s.mp3" % the_event
the_file = the_file.replace(" ", "_")
if os.path.isfile(the_file):
    print("File already exists")
else:
    # now create the MP3 file
    tts = gTTS(text='%s' % the_event, lang='en')
    tts.save("%s" % the_file)

# Create 1 minute to go notification
text_file = open("1.txt", "w")
text_file.write("mpg123 --stereo %s in_1_minute.mp3\nsleep 30\nmpg123 --stereo 30_seconds.mp3\n" % the_file)
text_file.write("sleep 30\nmpg123 --stereo %s starts_now.mp3\n^D\n" % the_file)
text_file.close()

offset_time = datetime.timedelta(minutes=1)
notify_time = new_time - offset_time
os.system('at %s < 1.txt' % notify_time.strftime("%H:%M"))

# Create 5 minute to go notification
if delta_minutes < 5:
    quit()

text_file = open("1.txt", "w")
text_file.write("mpg123 --stereo %s in_5_minutes.mp3\n^D\n" % the_file)
text_file.close()

offset_time = datetime.timedelta(minutes=5)
notify_time = new_time - offset_time
os.system('at %s < 1.txt' % notify_time.strftime("%H:%M"))

# Create 15 minute to go notification
if delta_minutes < 15:
    quit()

text_file = open("1.txt", "w")
text_file.write("mpg123 --stereo %s in_15_minutes.mp3\n^D\n" % the_file)
text_file.close()

offset_time = datetime.timedelta(minutes=15)
notify_time = new_time - offset_time
os.system('at %s < 1.txt' % notify_time.strftime("%H:%M"))

# Create 30 minute to go notification
if delta_minutes < 30:
    quit()

text_file = open("1.txt", "w")
text_file.write("mpg123 --stereo %s in_30_minutes.mp3\n^D\n" % the_file)
text_file.close()

offset_time = datetime.timedelta(minutes=30)
notify_time = new_time - offset_time
os.system('at %s < 1.txt' % notify_time.strftime("%H:%M"))

