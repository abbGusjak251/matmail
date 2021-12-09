import smtplib, requests, time, datetime
import html
from email.mime.text import MIMEText

EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""
fname = "folk.txt"
names = []
with open(fname, 'r') as f:
    for line in f:
        names.append(line.replace('\n', ''))
tos = ["gustav.jakobsson@abbgymnasiet.se"]
for name in names:
    email_by_name = '.'.join(name.lower().split(' '))
    if email_by_name[len(email_by_name)-1:len(email_by_name)] == ".":
        email_by_name = email_by_name[:len(email_by_name)-1]
    email_by_name += "@abbgymnasiet.se"
    print(email_by_name)
    tos.append(email_by_name)

date = datetime.datetime.today()
url = f'https://www.foodandco.se/api/restaurant/menu/week?language=sv&restaurantPageId=188244&weekDate={str(date)}'

time.sleep(5)

def get_today():
    switcher = {
        "Monday": "Måndag",
        "Tuesday": "Tisdag",
        "Wednesday": "Onsdag",
        "Thursday": "Torsdag",
        "Friday": "Fredag",
        "Saturday": "Lördag",
        "Sunday": "Söndag"
    }
    today = datetime.datetime.today().strftime('%A')
    return switcher[today]

def sendmail(message, to, name):
    try:
        # manages a connection to the SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.set_debuglevel(1)
        msg = MIMEText(message)
        server.starttls()
        # login to the email acco unt
        msg['Subject'] = f"Mat till {name}"
        msg['From'] = "magneten@info.nu"
        msg['To'] = to
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # send the actual message
        print(to)
        server.sendmail("magneten@info.nu", to, msg.as_string().encode('utf-8'))
        print("Success")
        # terminates the session
        server.quit()
    except Exception as e:
        print(e)

def main():
    r = requests.get(url)
    print(r.encoding)
    r= r.json()
    for to in tos:
        name = to.split('.').pop(0)
        name = list(name)
        name[0] = name[0].upper()
        name = ''.join(name)
        message = f" Hej {name}!\n\nDagens mat: \n\nVecka: {r['WeekNumber']}"
        for lunch in r["LunchMenus"]:
            if not (lunch["DayOfWeek"] == "Lördag" or lunch["DayOfWeek"] == "Söndag"):
                if lunch["DayOfWeek"] == get_today():
                    message += f"\n\nDag: {lunch['DayOfWeek']}\n" + html.unescape(lunch["Html"]).replace('<p>', '').replace('</p>', '')
        message += f"\n\nHa en bra dag {name}!"
        sendmail(message, to, name)
    print("Done")
    exit()

if __name__ == "__main__":
    main()

 