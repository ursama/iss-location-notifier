import requests
import smtplib
import time
from datetime import datetime

#input your own data
MY_LAT = 123 
MY_LONG = 123


# Making sure it's currently nighttime
def is_nighttime():
    if hour_now >= sunset or hour_now <= sunrise:
        return True
    return False


# Checking if iss is at my location
def is_near():
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


# Getting the ISS position
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data['iss_position']['latitude'])
iss_longitude = float(data['iss_position']['longitude'])

iss_current_location = (iss_latitude, iss_longitude)

# Getting the data of sunrise and sunset according to my position
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response_rise_set = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response_rise_set.raise_for_status()
data = response_rise_set.json()
sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0]) + 1
sunset = int(data['results']['sunset'].split("T")[1].split(":")[0]) + 1

# Getting the current hour
hour_now = datetime.now().hour

# Checking the conditions continuously
while True:
    time.sleep(60)
    if is_nighttime() and is_near():
        mail = "mail address" # add your mail address
        password = "pass" # add password to the mail

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(mail, password)
            connection.sendmail(
                from_addr=mail,
                to_addrs="mail address", # mail address to send the notification to
                msg="Subject:ISS notification\n\nLook up! There's ISS above you!"
            )
