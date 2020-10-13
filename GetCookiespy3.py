# -*- coding: UTF-8 -*-
# Written by xizhi

import os
import platform
import time
import re
import rsa
import base64
import urllib
import requests
import random

def GetCookiesExit1():
  print("程序5秒后自动退出")
  time.sleep(5)
  os._exit(0)

def GetCookiesClear1():
  OS = platform.system()
  if OS == "Windows":
    os.system("cls")
  else:
    os.system("clear")

class UniCookies():
  def UniPublicKey(self):
    global unipublickey
    unipublicpem = "-----BEGIN PUBLIC KEY-----\n"\
                             "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6"\
                             "FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQ"\
                             "o07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHO"\
                             "nwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n"\
                             "-----END PUBLIC KEY-----"
    unipublickey = rsa.PublicKey.load_pkcs1_openssl_pem(unipublicpem)

  def UniMobile(self):
    global unimob
    unimob = input("\n请输入你的手机号:")
    if len(unimob) != 11:
      print("请输入11位手机号码,1秒后重新输入")
      time.sleep(1)
      GetCookiesClear1()
      self.UniMobile()

  def UniRcode(self):
    global unilogin
    unircode = input("\n请输入验证码:")
    self.UniRSAEnc(unimob)
    quob64encunimob = quob64enca
    self.UniRSAEnc(unircode)
    quob64encunirpw = quob64enca
    unitimes = time.strftime("%Y%m%d%H%M%S",time.localtime(int(time.time())))
    unilgparams = "yw_code=&loginStyle=0&deviceOS=android10&mobile=%s&"\
                           "netWay=4G&deviceCode=7e5cb8b9fb0d422d9c17c389d774f917&"\
                           "isRemberPwd=true&version=android%%407.0601&"\
                           "deviceId=7e5cb8b9fb0d422d9c17c389d774f917&password=%s&"\
                           "keyVersion=&pip=127.0.0.1&provinceChanel=general&voice_code=&"\
                           "appId=ChinaunicomMobileBusiness&voiceoff_flag=1&deviceModel=GM1910&"\
                           "deviceBrand=OnePlus&timestamp=%s"\
                            %(quob64encunimob,quob64encunirpw,unitimes)
    try:
      unilogin = requests.post("https://m.client.10010.com/mobileService/radomLogin.htm",
                              headers=uniheaders,data=unilgparams,timeout=10)
      unilogins = eval(unilogin.content.decode("utf-8"))
      if re.findall(r"proName",str(unilogins),flags=re.I) != []:
        print("\n返回登录成功信息:\n%s省 %s市 %s\n"\
               %(unilogins["list"][0]["proName"],unilogins["list"][0]["cityName"],unilogins["list"][0]["num"]))
      elif re.findall(r"验证码错误",str(unilogins)) != []:
        print("\n返回信息: %s\n输入验证码错误,1秒后重新输入,如果多次输入正确却提示错误的请重新打开程序获取新的验证码"%(unilogins["dsc"]))
        time.sleep(1)
        self.UniRcode()
    except:
      print("\n可能程序出错了,正在重新运行程序")
      GetCookiesClear1()
      self.UniMain()
      
  def UniRSAEnc(self,a):
    global quob64enca
    self.UniPublicKey()
    enca = rsa.encrypt(a.encode("utf-8"),unipublickey)
    b64enca = base64.b64encode(enca).decode()
    quob64enca = urllib.parse.quote(b64enca,safe="")
      
  def UniMain(self):
    global uniheaders
    self.UniMobile()
    uniheaders = {"Content-Type":"application/x-www-form-urlencoded; Charset=UTF-8",
                          "User-Agent":"okhttp/3.9.1"}
    print("\n是否需要发送验证码,上次获取了5分钟内未使用成功的可以继续用哦")
    unisrcodeask = input("是 直接按确定继续,否 输入 n 后按确定:")
    if unisrcodeask.lower() == "n":
      pass
    else:
      self.UniRSAEnc(unimob)
      quob64encunimob = quob64enca
      uniscparams = "mobile=%s&version=android%%407.0601&keyVersion="%(quob64encunimob)
      try:
        unisrcode = requests.post("https://m.client.10010.com/mobileService/sendRadomNum.htm",
                               headers=uniheaders,data=uniscparams,timeout=10)
        unisrcodes =eval(unisrcode.content.decode("utf-8"))["rsp_desc"]
        if re.findall(r"验证码已发送",unisrcodes) != []:
          print("\n返回信息: "+unisrcodes)
        else:
          print("\n返回信息: %s\n验证码发送失败哦"%(unisrcodes))
          self.UniMain()
      except:
        print("\n可能程序出错了,正在重新运行程序")
        GetCookiesClear1()
        self.UniMain()
    self.UniRcode()
    unidiccookies = requests.utils.dict_from_cookiejar(unilogin.cookies)
    unilstcookies = []
    for cookie in unidiccookies:
      unilstcookies.append(cookie+"="+unidiccookies.get(cookie))
    unistrcookies = ";".join(unilstcookies)
    print("%s Cookies获取成功,将以下内容复制粘贴到需要的地方即可,同时已在该目录下生成一个 .cookies 文件(一般的打开文本类程序即可查看修改),30秒后自动退出程序\n%s"%(unimob,unistrcookies))
    with open(unimob+" uni.cookies","w") as unicookies:
      unicookies.write(unistrcookies)
    time.sleep(30)
    os._exit(0)

class JDCookies():
  def JDLogined(self):
    jdlogin = requests.get("https://passport.jd.com/uc/qrCodeTicketValidation?t=%s"%(ticket),
                                        headers=jdheaders,timeout=3)
    jddiccookies = requests.utils.dict_from_cookiejar(jdlogin.cookies)
    jdlstcookies = []
    for cookie in jddiccookies:
      jdlstcookies.append(cookie+"="+jddiccookies.get(cookie))
    jdstrcookies = ";".join(jdlstcookies)
    print("%s Cookies获取成功,将以下内容复制粘贴到需要的地方即可,同时已在该目录下生成一个 .cookies 文件(一般的打开文本类程序即可查看修改),30秒后自动退出程序\n%s"%(jddiccookies["unick"],jdstrcookies))
    with open(jddiccookies["unick"]+" JDCookies.cookies", "w")as jdcookies:
      jdcookies.write(jdstrcookies)
    time.sleep(30)
    os._exit(0)
  
  def JDBeforLogin(self):
    global jdheaders,ticket
    jdheaders = {
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                         "referer": "https://passport.jd.com"
                         }
    jdgetqr = requests.get("https://qr.m.jd.com/show?appid=133&size=147&t=%s"%(int(time.time()*1000)),
                                      headers=jdheaders,timeout=3)
    jddiccookies = requests.utils.dict_from_cookiejar(jdgetqr.cookies)
    jdtoken = jddiccookies["wlfstk_smdl"]
    jdlstcookies = []
    for cookie in jddiccookies:
      jdlstcookies.append(cookie+"="+jddiccookies.get(cookie))
    jdstrcookies = ";".join(jdlstcookies)
 
    with open("JDQRcode.png", "wb")as f:
      f.write(jdgetqr.content)
    print("\n二维码图片 JDQRcode.png 已下载到该目录下,请后台运行程序,电脑打开图片后用京东APP扫码登录\n"\
             "手机端操作在提示扫码时选择本地图片即可\n"\
             "Android需要系统更新图库信息才能看到图片,可以选择不删除图片,不然下次又得等系统更新图库信息了\n"\
             "iPhone需要先将图片保存到相簿且需要手动清理相簿里的登录二维码,否则很难知道哪个是哪个的\n")

    while 1:
      jdheaders["cookie"] = jdstrcookies
      jdcheckqrs = requests.get("https://qr.m.jd.com/check?callback=jQuery%s&appid=133&token=%s&_=%s"\
                                                 %(random.randint(1000000,9999999),jdtoken,int(time.time()*1000)),
                                                 headers=jdheaders,timeout=3)
      jdcheckqrj = eval(re.match(r".*({.*}).*",str(jdcheckqrs.text),flags=re.S).group(1))
      if re.findall(r"201|202",str(jdcheckqrj["code"])) != []:
        print(jdcheckqrj["msg"])
      elif re.findall(r"257|203|205",str(jdcheckqrj["code"])) != []:
        print("返回信息: %s\n是否重新获取二维码,手机端操作需要先完全关闭京东APP哦"%(jdcheckqrj["msg"]))
        jdqrcask = input("是 直接按确定继续,否 输入 n 然后按确定退出:")
        if jdqrcask.lower() == "n":
          GetCookiesExit1()
        else:
          self.JDBeforLogin()
      elif re.findall(r"ticket",str(jdcheckqrj),flags=re.I) !=[]:
        ticket = jdcheckqrj["ticket"]
        print("登录成功并获取到ticket,正在获取Cookies...\n")
        break
      time.sleep(3)
    time.sleep(1)
    self.JDLogined()

def GetCookiesMain1():
  funcl = ["1 获取联通Cookies",
               "2 获取京东Cookies",]
  print("功能选择:\n\n"+"\n\n".join(funcl))
  funcsel = input("\n更多整合等待发现,欢迎回复提供\n\n请输入对应数字然后按确定:")
  if funcsel == "" or funcsel == "0":
    funcsel = 1
    print("数字小于1,默认选择第一个 %s"%(funcl[int(funcsel)-1])[2:])
    time.sleep(1)
  if len(funcl)-int(funcsel) >= 0:
    GetCookiesClear1()
    if int(funcsel) == 1:
      UniCookies().UniMain()
    elif int(funcsel) == 2:
      JDCookies().JDBeforLogin()
  else:
    print("请输入仅列出的数字,1秒后重新输入")
    time.sleep(1)
    GetCookiesClear1()
    GetCookiesMain1()

GetCookiesMain1()
