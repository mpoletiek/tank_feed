#!/usr/bin/python

# get_image.py
# Author: https://enlightened.army/@mpoletiek

# Purpose: Get an image from an RTSP (Camera) stream and save it localy for later review.
#   Additionally, post the image to Mastodon @enlightened.army for fun and monitoring.

import datetime, os, subprocess, re, time
from mastodon import Mastodon
import tokenlib_public

# Setup Variables
rtsp_stream = "rtsp://Viewer:Key1234@192.168.1.182:554/live/ch0"
now_dt = datetime.datetime.now()
now_str = now_dt.strftime('%Y-%m-%d_%H:%M')
image_path="./images"
image_name="fishtank_image"
image_ext="jpg"
dated_image_name = "%s_%s.%s" % (now_str, image_name, image_ext)
hashtagcontent = "#fishtankcam"

# Get the image using 'ffmpeg'
print("Getting %s" % (dated_image_name))
process = subprocess.Popen("ffmpeg -y -i %s -vframes 1 %s/%s" % (rtsp_stream, image_path, dated_image_name), shell=True)
process.wait()

####################################
## SETTING UP MASTODON CONNECTION ##
## modify tokenlib_pub.py for Auth #
####################################
## now lets get the tokens for our bot
tokendict=tokenlib_public.getmytokenfor("enlightened.army")
pa_token = tokendict["pa_token"]
host_instance = tokendict["host_instance"]
botname = tokendict["botname"]
print("host instance is", host_instance)
print("POSTING AS %s" %(botname))
# we need this to use pythons Mastodon.py package
mastodon = Mastodon(
    access_token = pa_token,
    api_base_url = host_instance
)

# Upload the image we want to post to Mastodon
target_image = "%s/%s" % (image_path, dated_image_name)
media_dict = mastodon.media_post(target_image,description="a_fishtank cam shot")

# the text to toot
feed_title = "a_fishtank cam shot."
feed_link = now_str
toottxt = "%s \n%s" % (feed_title, feed_link)

# prepend botname to hashtags
hashtag1 = "#" + botname

# hashtags and tweettext together
post_text = str(toottxt) + "\n" + "posted by " + hashtag1 + " " + hashtagcontent + "\n" # creating post text
post_text = post_text[0:499]
print("%s\n" % (post_text))

###############
## POST TOOT ##
###############
# Post in 20 seconds
print("Posting New Toot in 20 seconds as a safety measure.")
time.sleep(20)

mastodon.status_post(post_text,media_ids=media_dict)
###############
########################




