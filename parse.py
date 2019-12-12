import bs4, requests, json, datetime
from apscheduler.schedulers.blocking import BlockingScheduler



def sign_in():
    print("Decorated job")
    json_file = open("creds.json")
    data = json.load(json_file)
    login = requests.post("http://eclass.informatics.teicm.gr/", data={'uname': data['uname'], 'pass': data['pass'], 'submit': data['submit']})

    print(login.headers["Set-Cookie"])




scheduler = BlockingScheduler()
scheduler.add_job(sign_in, 'interval', hours=1, next_run_time=datetime.datetime.now())
scheduler.start()
