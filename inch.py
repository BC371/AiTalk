import requests
import os
import time
import random
import urllib
import re

import urllib3

log_file = "log.txt"


# parameter string ++++++ split %20
def Get_inch_sign(line):
    return os.popen(f"/home/bc/Downloads/jdk-17.0.2/bin/java CD {line}").read()[-33:-1]


def write_log(*args):
    with open(log_file, "a") as f:
        f.write(time.asctime())
        for text in args:
            f.write(str(text))


# inch-timestamp nonce inch_sign
def get_it_ne_is(url, access_token):
    inch_timestamp = str(int(time.time() * 1000))
    nonce = inch_timestamp + str(int(random.random() * 100000000))
    line = ""
    if re.search("\?.*", url):
        line += urllib.parse.unquote(" ".join(re.search("\?.*", url).group()[1:].split("&")))
    line += " inch_timestamp=" + inch_timestamp + " nonce=" + nonce
    if access_token:
        line += " access_token=" + access_token
    inch_sign = Get_inch_sign(line)
    write_log(line, inch_sign)
    return inch_timestamp, nonce, inch_sign


def Post_Msg(http, url, at=""):
    inch_timestamp, nonce, inch_sign = get_it_ne_is(url, "")
    header = {
        "systemid": "parent",
        "access_token": at,
        "inch_timestamp": inch_timestamp,
        "nonce": nonce,
        "inch_sign": inch_sign,
        "Content-Length": "0",
        "Host": "school.incich.com:9208",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
    }
    if not at:
        header.pop("access_token")
    http.headers.update(header)
    response = http.post(url, verify=False)
    write_log(url, header, response)
    http.headers.clear()
    
    
def oath(http):
    inch_timestamp, nonce, inch_sign = get_it_ne_is(
        "?systemid=parent&grant_type=password&username=C9F306EE46025F001D242D4A31D3B35C", "")
    header = {
        "Authorization": "Basic aW5jaF9wYXJlbnQ6ODVhMzNlNTAtMmJmZC0xMWU4LTkzYzktMzhjOTg2NDEyZmZj",
        "nonce": nonce,
        "inch_timestamp": inch_timestamp,
        "inch_sign": inch_sign,
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "77",
        "Host": "school.incich.com:9208",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
    }
    body = "systemid=parent&grant_type=password&username=C9F306EE46025F001D242D4A31D3B35C"
    http.headers.update(header)
    response = http.post("http://school.incich.com:9208/display-rest/oauth/token", data=body).json()
    http.headers.clear()
    return response["access_token"]

def login():
    print("LOGIN ---------")
    urllib3.disable_warnings()
    http = requests.Session()
    http.headers.clear()
    # qq 登录
    url = r"http://school.incich.com:9208/display-rest/ThirdLogin/login.json?unionid=C9F306EE46025F001D242D4A31D3B35C&imgurl=http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DE9mdGLujGiaSmqDukQib2L8w%26s%3D100%26t%3D1623461878&nickname=Hurrah+zhangjs+%21%21&sex=1&source=QQ&factory=xiaomi"
    Post_Msg(http, url)
    url = r"http://school.incich.com:9208/display-rest/ThirdLogin/saveToken.json?unionid=C9F306EE46025F001D242D4A31D3B35C&phonetoken=8M%2BaAnjXrQ9zq4ratucPVdby%2FF%2B0rkMvfMDNHyczPX5lObQWNILHafZ2l85fPJvv&phonetype=M2007J22C&factory=xiaomi"
    Post_Msg(http, url)
    inch_timestamp, nonce, inch_sign = get_it_ne_is(
        "?systemid=parent&grant_type=password&username=C9F306EE46025F001D242D4A31D3B35C", "")
    header = {
        "Authorization": "Basic aW5jaF9wYXJlbnQ6ODVhMzNlNTAtMmJmZC0xMWU4LTkzYzktMzhjOTg2NDEyZmZj",
        "nonce": nonce,
        "inch_timestamp": inch_timestamp,
        "inch_sign": inch_sign,
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "77",
        "Host": "school.incich.com:9208",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
    }
    body = "systemid=parent&grant_type=password&username=C9F306EE46025F001D242D4A31D3B35C"
    http.headers.update(header)
    response = http.post("http://school.incich.com:9208/display-rest/oauth/token", data=body).json()
    http.headers.clear()
    access_token=oath(http)
    return access_token
