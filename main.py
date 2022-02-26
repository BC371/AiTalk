import os
import requests
import urllib3
from pydub import AudioSegment
import urllib
import inch
# from PIL import Image
import random
import time


def get_ranstr():
    s = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    return "".join(s[random.randint(0, 15)] for i in range(8)) + "-" + "".join(
        s[random.randint(0, 15)] for i in range(4)) + "-" + "".join(
        s[random.randint(0, 15)] for i in range(4)) + "-" + "".join(
        s[random.randint(0, 15)] for i in range(4)) + "-" + "".join(s[random.randint(0, 15)] for i in range(12))


# raw msg <700
def sendtext(std, msg, at):
    print("SENDTEXT ------")
    msg = urllib.parse.quote(msg)
    # yan first
    url = f"http://school.incich.com:9208/display-rest/message/save?stuname={stu_dict['name'][std]}&addusername=Hurrah%2Bzhangjs%2B%2521%2521&schoolid=9482&coverimg=&msg={msg}&adduser=C9F306EE46025F001D242D4A31D3B35C&url=&stuguid={stu_dict['id'][std]}&aspectratio=0.0&voicelen=0&classid=9486&type=1"
    inch.Post_Msg(http, url, at)


def upload(std, file, at):
    print("UPLOADING ------")
    url = "http://school.incich.com:9207/UploadImageServlet"
    inch_timestamp, nonce, inch_sign = inch.get_it_ne_is("", at)
    boundary = get_ranstr()
    header = {
        "systemid": "parent",
        "access_token": at,
        "inch_timestamp": inch_timestamp,
        "nonce": nonce,
        "inch_sign": inch_sign,
        "Content-Type": "multipart/form-data; boundary=" + boundary,
        "Content-Length": "0",
        "Host": "school.incich.com:9207",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
    }
    amr_len = ""
    msg = ""
    aspectratio = "0.0"
    if file[-3:] == "amr":
        amr_len = AudioSegment.from_file(file).duration_seconds  # float
        filename = str(int(inch_timestamp) - int(amr_len * 1000)) + ".amr"
    else:
        # img = Image.open(file)
        msg = "%25E7%25BB%2599%25E6%2582%25A8%25E5%258F%2591%25E6%259D%25A5%25E4%25B8%2580%25E6%259D%25A1%25E5%259B%25BE%25E7%2589%2587%25E6%25B6%2588%25E6%2581%25AF"
        filename = get_ranstr() + ".jpg"
        # aspectratio = img.width / img.height  # ----------------------------------

    # file=r"C:\Users\ASUS\Downloads\ms.amr"
    d = open(file, "rb").read()
    # --------------------------------------------------
    h = f'--{boundary}\r\nContent-Disposition: form-data; name="file0"; filename="{filename}"\r\nContent-Type: image/png\r\nContent-Length: {len(d)}\r\n\r\n'.encode()
    t = f"\r\n--{boundary}--\r\n".encode()
    http.headers.update(header)
    re_url = http.post(url, verify=False, data=h + d + t).json()["url"]
    http.headers.clear()
    url = f"http://school.incich.com:9208/display-rest/message/save?stuname={stu_dict['name'][std]}&addusername=Hurrah%2Bzhangjs%2B%2521%2521&schoolid=9482&coverimg=&msg={msg}&adduser=C9F306EE46025F001D242D4A31D3B35C&url={urllib.parse.quote(re_url)}&stuguid={stu_dict['id'][std]}&aspectratio={aspectratio}&voicelen={str(int(amr_len))}&classid=9486&type=2"
    inch.Post_Msg(http, url, at)

def mc(msg):
    if "-s" in msg:
        if len(msg) == msg.find("-s") + 2:
            msg = msg.replace("-s", "-s10 ")
        else:
            msg = msg + " -s0"
        if not ":" in msg:
            msg = msg + " 0"
        try:
            os.system("python3 mc.py {}".format(msg[2:].replace("+", " ")))
        except Exception as e:
                    # print(e)
            inch.write_log(e)
        if "-l" in msg or "-s10" in msg:
            sendtext(std, open("response.txt").read(), access_token)
        else:
            upload(std, open("response.txt").read(), access_token)


# time str
def get_modetime(num):
    s = time.ctime(int(num[0:-3]))
    return s[0:3] + ", " + str(int(s[8:10]) + 100)[1:] + s[3:7] + s[19:25] + " " + str(
        100 + (24 + int(s[11:13]) - 8) % 24)[1:] + s[13:20] + "GMT"

# raw lasttime access_token
def refresh(at):
    print("REFRESHIING ------")
    global refresh_time
    url = "http://school.incich.com:9208/display-rest/getInfo/getNoticeNew.json?unionid=C9F306EE46025F001D242D4A31D3B35C&classid=9486&schoolid=9482&name=%E7%8E%8B%E6%9D%B0%E9%93%AD&pageno=1&length=20"
    inch_timestamp, nonce, inch_sign = inch.get_it_ne_is(url, at)
    header = {
        "access_token": at,
        "systemid": "parent",
        "nonce": nonce,
        "inch_timestamp": inch_timestamp,
        "inch_sign": inch_sign,
        "Host": "school.incich.com:9208",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0",
        "If-Modified-Since": get_modetime(refresh_time)
    }
    http.headers.update(header)
    response = http.get(url, verify=False)
    if response.status_code==401:
        http.headers.clear()
        global access_token=inch.oath(http)
        return refersh(access_token)
    response=response.json()
    refresh_time = inch_timestamp
    # yan first
    time_text_dict = {"te": [response["data"][1]["addtime"], response["data"][2]["addtime"]],
                      "tt": [response["data"][1]["title"], response["data"][2]["title"]]}
    inch.write_log(url, header, response)
    http.headers.clear()
    return time_text_dict


urllib3.disable_warnings()
http = requests.session()
frame = 3  # fps
alive_time = 2 * 60 * 60  # second
http.headers.clear()
stu_dict = {"name": ["%E9%97%AB%E4%BD%B3%E4%B9%90", "%E7%8E%8B%E6%9D%B0%E9%93%AD"],
            "id": ["47fb7e8e-c626-473b-a562-45ea07acab1b", "37b073f9-a900-423b-a8ea-4b13e527ab24"]}

###################################
refresh_time_file = r"refresh_time.txt"
# 1644223547810
with open(refresh_time_file) as f:
    refresh_time = f.readline()[0:13]

access_token = inch.login()
# print(access_token)
old_dict = refresh(access_token)
# print(old_dict)
run_time = 0

while True:
    time.sleep(1)
    run_time += 1
    if not run_time % frame:
        new_dict = refresh(access_token)
        # s=input()
        # exec(s)# --------------------------------------------
        if not old_dict["te"] == new_dict["te"]:
            # new message yan outdo
            std = 1 if old_dict["te"][0] == new_dict["te"][0] else 0
            old_dict = new_dict
            msg = new_dict["tt"][std]  # new_message
            if msg[:2] == "mc":
                mc(msg)
            if msg[:4] == "echo":
                sendtext(std, msg[5:], access_token)
            if msg == "clearchache":
                os.system("rm -r ./mc_logs")
                os.mkdir("./mc_logs")
                sendtext(std, "200", access_token)

    if run_time >= alive_time:
        run_time = 0
        with open(refresh_time_file, "w") as f:
            f.write(refresh_time)
        access_token = inch.login()
