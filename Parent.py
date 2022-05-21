import os
import requests
from pydub import AudioSegment
import re
import urllib
from PIL import Image
import random
import time


def get_ranstr():
    s=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    return "".join(s[random.randint(0,15)] for i in range(8))+"-"+"".join(s[random.randint(0,15)] for i in range(4))+"-"+"".join(s[random.randint(0,15)] for i in range(4))+"-"+"".join(s[random.randint(0,15)] for i in range(4))+"-"+"".join(s[random.randint(0,15)] for i in range(12))

def Get_inch_sign(line):
    #print(line)
    d={}
    list=line.split(' ')
    for li in list:
        l=li.find('=')
        l=l if l!=-1 else len(li)
        d[li[:l]]=li[l+1:]
    #print(d)

    temp2 = ''
    for i in sorted(d.keys()):
        temp2 += str(i) + "=" + str(d[i]) + "&"
    temp2 += "aef2890665d884a3080971b4eca594d7"
    #print(temp2)
    sign = hashlib.md5(temp2.encode("utf-8")).hexdigest().upper()
    #print(sign)
    return sign

stu_dict={"name":["xxxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxx"],
"id":["xxxxxxxxxxxxxxxxxxx","xxxxxxxxxxxxxxxxxxx4"]}
class Parent():
    def __init__(self,userid):
        self.access_token=0
        self.url=""
        self.refresh_time=int(time.time()*1000)
        self.http=requests.session()
        self.http.headers.clear()
        self.login()


    def write_log(*args):
        with open(log_file,"a")as f:
            f.write(time.asctime())
            for text in args:
                f.write(str(text))

    # inch-timestamp nonce inch_sign USE self.url
    def get_it_ne_is(self,at):
        inch_timestamp=str(int(time.time()*1000))
        nonce=inch_timestamp+str(int(random.random()*100000000))
        line=""
        if re.search("\?.*",self.url):
            line+=urllib.parse.unquote(" ".join(re.search("\?.*",self.url).group()[1:].split("&")))
        line+=" inch_timestamp="+inch_timestamp+" nonce="+nonce
        if at:
            line+=" access_token="+at
        inch_sign=Get_inch_sign(line)
        # print(line,inch_sign)
        # write_log(line,inch_sign)
        return inch_timestamp,nonce,inch_sign

    def upload(self,std,file):
        print("UPLOADING ------")
        url="http://school.incich.com:9207/UploadImageServlet"
        self.url=""
        inch_timestamp,nonce,inch_sign=self.get_it_ne_is(self.access_token)
        boundary=get_ranstr()
        header={
        "systemid": "parent",
        "access_token": self.access_token,
        "inch_timestamp": inch_timestamp,
        "nonce": nonce,
        "inch_sign": inch_sign,
        "Content-Type": "multipart/form-data; boundary="+boundary,
        "Content-Length": "0",
        "Host":"school.incich.com:9207",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
        }
        voicelen = "0"
        coverimg=""
        type=""
        aspectratio="0.0"
        fe_url=[""]
        msg = ""
        if file[-3:] in ["amr","mp3"]:
            type="2"
            voicelen=AudioSegment.from_file(file).duration_seconds
            filename=str(int(inch_timestamp)-int(voicelen)*1000)+".amr"
            print(voicelen)

        elif file[-3:]=="mp4":
            type="3"
            msg=r"%25E7%25BB%2599%25E6%2582%25A8%25E5%258F%2591%25E6%259D%25A5%25E4%25B8%2580%25E6%259D%25A1%25E8%25A7%2586%25E9%25A2%2591%25E6%25B6%2588%25E6%2581%25AF"
            video_len="71000"
            filename="video_"+str(int(inch_timestamp)-71000)+".mp4"
            aspectratio="1.7"
            pass
        else:
            type="4"
            msg=r"%25E7%25BB%2599%25E6%2582%25A8%25E5%258F%2591%25E6%259D%25A5%25E4%25B8%2580%25E6%259D%25A1%25E5%259B%25BE%25E7%2589%2587%25E6%25B6%2588%25E6%2581%25AF"
            img=Image.open(file)
            aspectratio=img.height/img.width*10//1/10
            filename = get_ranstr() + ".jpg"
        d=open(file,"rb").read()
        # --------------------------------------------------
        h=f'--{boundary}\r\nContent-Disposition: form-data; name="file0"; filename="{filename}"\r\nContent-Type: image/png\r\nContent-Length: {len(d)}\r\n\r\n'.encode()
        t=f"\r\n--{boundary}--\r\n".encode()
        self.http.headers.update(header)
        fe_url=fe_url+self.http.post(url,verify=False,data=h+d+t).json()["url"].split(",")
        print(fe_url)
        for i in range(len(fe_url)):
            fe_url[i]=urllib.parse.quote(fe_url[i]).replace("/","%2F")

        self.http.headers.clear()
        self.url=f"http://school.incich.com:9208/display-rest/message/save?msg={msg}&classid=xxxx&coverimg=&adduser=xxxxxxxxxxxxxxxxxxx&schoolid=xxxx&addusername=xxxxxxxxxxxxxxxxxxx&type={type}&stuguid={stu_dict['id'][std]}&stuname={stu_dict['name'][std]}&url={fe_url[-1]}&voicelen={int(voicelen)}&aspectratio={aspectratio}"
        self.Post_Msg(self.access_token)

    def Post_Msg(self,at=""):
        inch_timestamp,nonce,inch_sign=self.get_it_ne_is("")
        header={
        "systemid": "parent",
        "access_token": at,
        "inch_timestamp": inch_timestamp,
        "nonce": nonce,
        "inch_sign": inch_sign,
        "Content-Length": "0",
        "Host":"school.incich.com:9208",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
        }
       #print(header)
        if not at:
            header.pop("access_token")
        self.http.headers.update(header)
        self.http.post(self.url,verify=False)
        # write_log(url,header,response)
        self.http.headers.clear()

    def sendtext(self,std,msg):
        print("SENDTEXT ------")
        msg=urllib.parse.quote(msg).replace("/","%2F")
        self.url=f"http://school.incich.com:9208/display-rest/message/save?stuname={stu_dict['name'][std]}&addusername=xxxxxxxxxxxxxxxxxxx&schoolid=xxxx&coverimg=&msg={msg}&adduser=xxxxxxxxxxxxxxxxxxx&url=&stuguid={stu_dict['id'][std]}&aspectratio=0.0&voicelen=0&classid=9486&type=1"
        self.Post_Msg(self.access_token)

    def oath(self):
        self.url=r"?systemid=parent&grant_type=password&username=xxxxxxxxxxxxxxxxxxx"
        inch_timestamp, nonce, inch_sign = self.get_it_ne_is("")
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
        body = "systemid=parent&grant_type=password&username=xxxxxxxxxxxxxxxxxxx"
        self.http.headers.update(header)
        self.access_token=self.http.post("http://school.incich.com:9208/display-rest/oauth/token", data=body).json()["access_token"]
        self.http.headers.clear()

    def refresh(self):
        print("REFRESHIING ------")
        s=time.ctime(self.refresh_time)
        GMT=s[0:3]+", "+str(int(s[8:10])+100)[1:]+s[3:7]+s[19:25]+" "+str(100+(24+int(s[11:13])-8)%24)[1:]+s[13:20]+"GMT"
        self.url="http://school.incich.com:9208/display-rest/getInfo/getNoticeNew.json?unionid=xxxxxxxxxxxxxxxxxxx&classid=9486&schoolid=xxxx&name=xxxxxxxx&pageno=1&length=20"
        inch_timestamp,nonce,inch_sign=self.get_it_ne_is(self.access_token)
        header={
        "access_token": self.access_token,
        "systemid": "parent",
        "nonce": nonce,
        "inch_timestamp": inch_timestamp,
        "inch_sign": inch_sign,
        "Host":"school.incich.com:9208",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0",
        "If-Modified-Since": GMT
        }
    
        self.http.headers.update(header)
        response = self.http.get(self.url, verify=False)
        if response.status_code==401:
            self.http.headers.clear()
            self.oath()
            return self.refresh()
            
        response=response.json()
        time_text_dict=[[],[]]
        self.refresh_time=int(inch_timestamp[:-3])
        for i in range(5):
            if response["data"][i]["type"]=="8":
                if response["data"][i]["adduser"]==stu_dict["id"][0]:
                    time_text_dict[0]=[response["data"][i]["addtime"],response["data"][i]["title"]]
                elif response["data"][i]["adduser"]==stu_dict["id"][1]:
                    time_text_dict[1]=[response["data"][i]["addtime"],response["data"][i]["title"]]
        # inch.write_log(url,header,response)
        self.http.headers.clear()
        return time_text_dict


    def login(self):
        print("LOGIN ---------")
        self.http.headers.clear()
        #qq 登录
        self.url=r"http://school.incich.com:9208/display-rest/ThirdLogin/login.json?unionid=xxxxxxxxxxxxxxxxxxx&imgurl=http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DE9mdGLujGiaSmqDukQib2L8xxxxxxxx&nickname=xxxxxxxxxxx&sex=1&source=QQ&factory=xiaomi"
        self.Post_Msg()
        self.url=r"http://school.incich.com:9208/display-rest/ThirdLogin/saveToken.json?unionid=xxxxxxxxxxxxxxxxxxx&phonetoken=8M%2BaAnjXrQ9zq4ratucPVdby%2FF%2B0rkMvfMDNxxxxxxxxxxxxx&phonetype=M20xxxxxxx&factory=xiaomi"
        self.Post_Msg()
        self.oath()
        msg="AiTalk login:"+time.asctime(time.localtime())[4:-5]
        self.sendtext(0,msg)
        wrong=os.popen("tail -1 nohup.out").read()
        if wrong:
            self.sendtext(0,"$?:"+wrong)
        
