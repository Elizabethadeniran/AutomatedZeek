import requests
import random
import threading

url = "http://127.0.0.1:9541/login"
username = "admin"
passwd_list = ["ot", "ul", "az", "j5", "98", "wk", "dq","hu", "oz"]

def send_request(username, password):
    data = {
        "username": username,
        "password": password
    }

    r = requests.post(url, json=data)
    return r

def main():
    
    passwd = random.choice(passwd_list)
    r = send_request(username=username, password=passwd)
    
    if 'Login failed' in r.json()['message']:
        print(f'Incorrect password:{passwd}', r.status_code)
    else:
        print(f'Correct Password: {passwd}', r.status_code)


for x in range(100):
    main()
