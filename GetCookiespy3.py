# -*- coding: utf-8 -*-
# Written by xizhi

import sys
import time
try:
  import requests
except (ImportError,ModuleNotFoundError):
  print("请先安装 requests 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
try:
  import rsa
except (ImportError,ModuleNotFoundError):
  print("请先安装 rsa 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
try:
  import qrcode
except (ImportError,ModuleNotFoundError):
  print("请先安装 qrcode 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
try:
  from PIL import Image
except (ImportError,ModuleNotFoundError):
  print("请先安装 Pillow 模块哦,5秒后自动退出")
  time.sleep(5)
  sys.exit()
import os
import re
import base64
import urllib
import random
import uuid
import ast

def GetCookiesExit1():
  print("程序5秒后自动退出")
  time.sleep(5)
  sys.exit()

def GetCookiesClear1():
  if sys.platform == "win32":
    os.system("cls")
  else:
    os.system("clear")

class UniCookies():
  def UniPublicKey(self):
    unipublicpem = "-----BEGIN PUBLIC KEY-----\n"\
                   "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6"\
                   "FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQ"\
                   "o07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHO"\
                   "nwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n"\
                   "-----END PUBLIC KEY-----"
    unipublickey = rsa.PublicKey.load_pkcs1_openssl_pem(unipublicpem)
    return unipublickey

  def UniRSAEnc(self,a):
    enca = rsa.encrypt(a.encode("utf-8"),self.UniPublicKey())
    b64enca = base64.b64encode(enca).decode()
    quob64enca = urllib.parse.quote(b64enca,safe="")
    return quob64enca

  def UniMobile(self):
    unimob = input("\n请输入你的手机号:")
    if len(unimob) != 11:
      print("请输入11位手机号码,1秒后重新输入")
      time.sleep(1)
      GetCookiesClear1()
      return self.UniMobile()
    else:
      return unimob

  def UniSRcode(self):
    unimob = self.UniMobile()
    uniheaders = {"Content-Type":"application/x-www-form-urlencoded; Charset=UTF-8",
                  "User-Agent":"okhttp/3.9.1"}
    print("\n是否需要发送验证码,上次获取了5分钟内未使用成功的可以继续用哦")
    unisrcodeask = input("是 直接按确定继续,否 输入 n 后按确定:")
    if unisrcodeask.lower() == "n":
      return unimob,uniheaders
    else:
      quob64encunimob = self.UniRSAEnc(unimob)
      uniscparams = "mobile=%s&version=android%%408.0002&keyVersion="%(quob64encunimob)
      try:
        unisrcode = requests.post("https://m.client.10010.com/mobileService/sendRadomNum.htm",
                                  headers=uniheaders,data=uniscparams,timeout=5)
        unisrcodes = ast.literal_eval(unisrcode.content.decode("utf-8"))["rsp_desc"]
        if re.findall(r"验证码已发送",unisrcodes) != []:
          print("\n返回信息: "+unisrcodes)
          return unimob,uniheaders
        else:
          print("\n返回信息: %s\n验证码发送失败哦"%(unisrcodes))
          return self.UniSRcode()
      except:
        print("\n可能程序出错了,正在重新运行程序")
        GetCookiesClear1()
        self.UniLogined()

  def UniLogin(self,unimob,uniheaders):
    unircode = input("\n请输入验证码:")
    quob64encunimob = self.UniRSAEnc(unimob)
    quob64encunirpw = self.UniRSAEnc(unircode)
    unitimes = time.strftime("%Y%m%d%H%M%S",time.localtime(int(time.time())))
    uuidstr = str(uuid.uuid4()).replace("-","")
    unilgparams = "yw_code=&loginStyle=0&deviceOS=android10&mobile=%s&"\
                  "netWay=4G&deviceCode=%s&"\
                  "isRemberPwd=true&version=android%%408.0002&"\
                  "deviceId=%s&password=%s&"\
                  "keyVersion=&pip=127.0.0.1&provinceChanel=general&voice_code=&"\
                  "appId=ChinaunicomMobileBusiness&voiceoff_flag=1&deviceModel=GM1910&"\
                  "deviceBrand=OnePlus&timestamp=%s"\
                  %(quob64encunimob,uuidstr,uuidstr,quob64encunirpw,unitimes)
    try:
      unilogin = requests.post("https://m.client.10010.com/mobileService/radomLogin.htm",
                               headers=uniheaders,data=unilgparams,timeout=5)
      unilogins = ast.literal_eval(unilogin.content.decode("utf-8"))
      if re.findall(r"proName",str(unilogins),flags=re.I) != []:
        print("\n返回登录成功信息:\n%s省 %s市 %s\n"\
              %(unilogins["list"][0]["proName"],unilogins["list"][0]["cityName"],unilogins["list"][0]["num"]))
        return unilogin
      elif re.findall(r"验证码错误",str(unilogins)) != []:
        print("\n返回信息: %s\n输入验证码错误,1秒后重新输入,如果多次输入正确却提示错误的请重新打开程序获取新的验证码"%(unilogins["dsc"]))
        time.sleep(1)
        return self.UniLogin(unimob,uniheaders)
    except:
      print("\n可能程序出错了,正在重新运行程序")
      GetCookiesClear1()
      self.UniLogined()
        
  def UniLogined(self):
    unimob,uniheaders = self.UniSRcode()
    unilogin = self.UniLogin(unimob,uniheaders)
    unidiccookies = requests.utils.dict_from_cookiejar(unilogin.cookies)
    unilstcookies = []
    for cookie in unidiccookies:
      if cookie == "cw_mutual":pass
      elif cookie == "u_account":pass
      elif cookie == "c_mobile":pass
      else:
        unilstcookies.append(cookie+"="+unidiccookies.get(cookie))
    unistrcookies = ";".join(unilstcookies)
    print("%s Cookies获取成功,将以下内容复制粘贴到需要的地方即可,同时已在该目录下生成一个 .cookies 文件(一般的打开文本类程序即可查看修改),30秒后自动退出程序\n%s"%(unimob,unistrcookies))
    with open(unimob+" uni.cookies","w") as unicookies:
      unicookies.write(unistrcookies)
    time.sleep(30)
    sys.exit()

class JDMobCookies():
  def JDMobLogin(self):
    jdheaders = {"User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
                 "Referer": "https://plogin.m.jd.com/login/login?appid=300"}
    jdgetstoken = requests.get("https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300",headers=jdheaders,timeout=5)
    stoken = jdgetstoken.json()["s_token"]
    jdsetcookiesd = requests.utils.dict_from_cookiejar(jdgetstoken.cookies)
    jdsetcookiesl = []
    for jdsetcookie in jdsetcookiesd:
      jdsetcookiesl.append(jdsetcookie+"="+jdsetcookiesd.get(jdsetcookie))
    jdsetcookies = ";".join(jdsetcookiesl)
    jdheaders["Cookie"] = jdsetcookies
    jdgettoken = requests.get("https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?lang=chs&appid=300&s_token=%s&remember=true"%(stoken),headers=jdheaders,timeout=5)
    token = jdgettoken.json()["token"]
    jdsetcookiesd = requests.utils.dict_from_cookiejar(jdgettoken.cookies)
    okltoken = jdsetcookiesd.get("okl_token")
    qrcodeb = qrcode.make("https://plogin.m.jd.com/cgi-bin/m/tmauth?appid=300&client_type=m&token=%s"%(token))
    qrcodeb.save("JDMobQRcode.png")
    print("\n二维码图片 JDMobQRcode.png 已生成到该目录下,请后台运行程序,电脑打开图片后用京东APP扫码登录\n"\
          "手机端操作在提示扫码时选择本地图片即可\n"\
          "Android需要系统更新图库信息才能看到图片,可以选择不删除图片,不然下次又得等系统更新图库信息了\n"\
          "iOS需要先将图片保存到相簿且需要手动清理相簿里的登录二维码,否则很难知道哪个是哪个的\n")
    if sys.platform == "win32":
      os.system('start "" "JDMobQRcode.png"')
    elif sys.platform == "darwin":
      os.system('open "JDMobQRcode.png"')
    else:
      os.system('xdg-open "JDMobQRcode.png"')

    while True:
      jdcheckqrp = requests.get("https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?lang=chs&appid=300&returnurl=&token=%s&ou_state=0&okl_token=%s"%(token,okltoken),
                                headers=jdheaders,timeout=5)
      jdcheckqrj = jdcheckqrp.json()
      if jdcheckqrj["errcode"] == 176:
        print(jdcheckqrj["message"])
      elif jdcheckqrj["errcode"] == 0:
        print("\n登录成功,可以关闭京东APP了...\n")
        return jdcheckqrp
      elif jdcheckqrj["errcode"] == 21:
        print("返回信息: %s\n是否重新获取二维码,手机端操作需要先完全关闭京东APP哦"%(jdcheckqrj["message"]))
        jdqrcask = input("是 直接按确定继续,否 输入 n 然后按确定退出:")
        if jdqrcask.lower() == "n":
          GetCookiesExit1()
        else:
          return self.JDMobLogin()
      else:
        print("返回信息: %s\n未遇到过的错误"%(jdcheckqrj["message"]))
      time.sleep(3)

  def JDMobLogined(self):
    jdcheckqrp = self.JDMobLogin()
    jdcookiesd = requests.utils.dict_from_cookiejar(jdcheckqrp.cookies)
    jdcookiesl = []
    for jdcookie in jdcookiesd:
      jdcookiesl.append(jdcookie+"="+jdcookiesd.get(jdcookie))
    jdstrcookies = ";".join(jdcookiesl)
    print("%s Cookies获取成功,将以下内容复制粘贴到需要的地方即可,同时已在该目录下生成一个 .cookies 文件(一般的打开文本类程序即可查看修改),30秒后自动退出程序\n%s"\
          %(jdcookiesd["pt_pin"],jdstrcookies))
    with open(jdcookiesd["pt_pin"]+" JDMob.cookies", "w") as jdcookies:
      jdcookies.write(jdstrcookies)
    time.sleep(30)
    sys.exit()

class JDPCCookies():
  def JDPCLogin(self):
    jdheaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                 "Referer": "https://passport.jd.com"}
    jdgetqr = requests.get("https://qr.m.jd.com/show?appid=133&size=147&t=%s"%(int(time.time()*1000)),
                           headers=jdheaders,timeout=5)
    jddiccookies = requests.utils.dict_from_cookiejar(jdgetqr.cookies)
    jdtoken = jddiccookies["wlfstk_smdl"]
    jdlstcookies = []
    for cookie in jddiccookies:
      jdlstcookies.append(cookie+"="+jddiccookies.get(cookie))
    jdstrcookies = ";".join(jdlstcookies)
 
    with open("JDPCQRcode.png", "wb") as qrcodeb:
      qrcodeb.write(jdgetqr.content)
    print("\n二维码图片 JDPCQRcode.png 已下载到该目录下,请后台运行程序,电脑打开图片后用京东APP扫码登录\n"\
          "手机端操作在提示扫码时选择本地图片即可\n"\
          "Android需要系统更新图库信息才能看到图片,可以选择不删除图片,不然下次又得等系统更新图库信息了\n"\
          "iOS需要先将图片保存到相簿且需要手动清理相簿里的登录二维码,否则很难知道哪个是哪个的\n")
    if sys.platform == "win32":
      os.system('start "" "JDPCQRcode.png"')
    elif sys.platform == "darwin":
      os.system('open "JDPCQRcode.png"')
    else:
      os.system('xdg-open "JDPCQRcode.png"')

    while True:
      jdheaders["Cookie"] = jdstrcookies
      jdcheckqrs = requests.get("https://qr.m.jd.com/check?callback=jQuery%s&appid=133&token=%s&_=%s"\
                                %(random.randint(1000000,9999999),jdtoken,int(time.time()*1000)),
                                headers=jdheaders,timeout=5)
      jdcheckqrj = ast.literal_eval(re.match(r".*({.*}).*",str(jdcheckqrs.text),flags=re.S).group(1))
      if re.findall(r"201|202",str(jdcheckqrj["code"])) != []:
        print(jdcheckqrj["msg"])
      elif re.findall(r"257|203|205",str(jdcheckqrj["code"])) != []:
        print("返回信息: %s\n是否重新获取二维码,手机端操作需要先完全关闭京东APP哦"%(jdcheckqrj["msg"]))
        jdqrcask = input("是 直接按确定继续,否 输入 n 然后按确定退出:")
        if jdqrcask.lower() == "n":
          GetCookiesExit1()
        else:
          return self.JDPCLogin()
      elif re.findall(r"ticket",str(jdcheckqrj),flags=re.I) !=[]:
        ticket = jdcheckqrj["ticket"]
        print("登录成功并获取到ticket,正在获取Cookies...\n")
        return jdheaders,ticket
        break
      else:
        print("返回信息: %s\n未遇到过的错误"%(jdcheckqrj["msg"]))
      time.sleep(3)
    time.sleep(1)

  def JDPCLogined(self):
    jdheaders,ticket = self.JDPCLogin()
    jdlogin = requests.get("https://passport.jd.com/uc/qrCodeTicketValidation?t=%s"%(ticket),
                           headers=jdheaders,timeout=5)
    jddiccookies = requests.utils.dict_from_cookiejar(jdlogin.cookies)
    jdlstcookies = []
    for jdcookie in jddiccookies:
      jdlstcookies.append(jdcookie+"="+jddiccookies.get(jdcookie))
    jdstrcookies = ";".join(jdlstcookies)
    print("%s Cookies获取成功,将以下内容复制粘贴到需要的地方即可,同时已在该目录下生成一个 .cookies 文件(一般的打开文本类程序即可查看修改),30秒后自动退出程序\n%s"\
          %(jddiccookies["unick"],jdstrcookies))
    with open(jddiccookies["unick"]+" JDPC.cookies", "w") as jdcookies:
      jdcookies.write(jdstrcookies)
    time.sleep(30)
    sys.exit()

def GetCookiesMain1():
  funcl = ["1 获取联通Cookies",
           "2 获取京东手机端Cookies",
           "3 获取京东PC端Cookies"]
  print("功能选择:\n\n"+"\n\n".join(funcl))
  funcsel = input("\n更多整合等待发现,欢迎回复提供\n\n请输入对应数字然后按确定:")
  if funcsel == "" or funcsel == "0":
    funcsel = 1
    print("数字小于1,默认选择第一个 %s"%(funcl[int(funcsel)-1])[2:])
    time.sleep(1)
  if len(funcl)-int(funcsel) >= 0:
    GetCookiesClear1()
    if int(funcsel) == 1:
      UniCookies().UniLogined()
    elif int(funcsel) == 2:
      JDMobCookies().JDMobLogined()
    elif int(funcsel) == 3:
      JDPCCookies().JDPCLogined()
  else:
    print("请输入仅列出的数字,1秒后重新输入")
    time.sleep(1)
    GetCookiesClear1()
    GetCookiesMain1()

if __name__ == "__main__":
  GetCookiesMain1()
  
