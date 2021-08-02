# bb-bucket-usage-logger
Simple python tool to login to backblaze, scrape all the bucket sizes and save them into a CSV file for later usage.

Usage:
place the tool somewhere on your disk, I recommend a linux distro and use crontab to kick it off once in a while.
Run it the first time manually so you can fill out the OTP, afterwards it should not need it anymore (until backblaze asks it again).
