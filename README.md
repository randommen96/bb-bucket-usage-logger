# bb-bucket-usage-logger
Simple python tool to login to backblaze, scrape all the bucket sizes and save them into a CSV file for later usage.

Usage:
Place the tool somewhere on your disk, I recommend a linux distro and use crontab to kick it off once in a while.
Make sure to fill in the .env file correctly.

After pip installing telegram_send, run it once and setup a bot, also needs selenium with chrome webdriver.

Containerized usage:  
docker build -t <tagname> .  
docker run -d --rm --shm-size=1gb --name runb2usage <tagname>
  
You can run it with a cron on your host, or through k8s or even add cron inside the container itself.