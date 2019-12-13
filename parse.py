import bs4
import requests
import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from requests.auth import HTTPBasicAuth
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sign_in():
    print("Decorated job")
    json_file = open("creds.json")
    data = json.load(json_file)

    creds = {
        "uname": data["uname"],
        "pass": data["pass"],
        "submit": ""
    }
    login = requests.get('http://eclass.informatics.teicm.gr/')
    cookie = login.headers['Set-Cookie']
    cookie = cookie.split(";")[0]
    print(cookie)

    payload = creds

    url = 'http://eclass.informatics.teicm.gr'

    headers = {
        "Cookie": cookie,
        "Host": "eclass.informatics.teicm.gr",
        "Connection": "close",
        "Referer": "http://eclass.informatics.teicm.gr",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    with requests.Session() as s:
        r = s.post(url, data=payload, headers=headers)
        headers = {
            "Cookie": cookie,
            "Host": "eclass.informatics.teicm.gr",
            "Connection": "close",
            "Referer": "http://eclass.informatics.teicm.gr/modules/work/?course=UNDERGRAD106",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }


        check_html = requests.get("http://eclass.informatics.teicm.gr/modules/work/index.php",
                                  params={"course": "UNDERGRAD106", "id": "10"}, headers=headers)
        soup = bs4.BeautifulSoup(check_html.content, 'html.parser')

        for inp in soup.find_all('span'):
            if inp.get_text() == "(η προθεσμία έχει λήξει)":
                print("NOT READY")
                return

        print("READY")
        port = 587
        with smtplib.SMTP("mail.crowsec.io", port) as server:
            server.login(data["email"], data["password"])
            msg = MIMEMultipart()
            message = "GO SEND THE PAPER MATE"
            msg['From'] = data["email"]
            msg['To'] = "hello@badrishvili.com"
            msg['Subject'] = "SUBMISSION OPENED"
            msg.attach(MIMEText(message, 'plain'))
            for i in range(2):
                server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()


scheduler = BlockingScheduler()
scheduler.add_job(sign_in, 'interval', minutes=30,
                  next_run_time=datetime.datetime.now())
scheduler.start()
