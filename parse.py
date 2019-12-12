import bs4, requests, json

json_file = open("creds.json")
data = json.load(json_file)
print(data['pass'])


login = requests.post("http://eclass.informatics.teicm.gr/", data={'uname': data['uname'], 'pass': data['pass'], 'submit': data['submit']})
print(login.headers)
