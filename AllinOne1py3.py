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
import os
import re
import linecache
import datetime
import ast

def AllinOneExit1():
  print("\n程序5秒后自动退出")
  linecache.clearcache()
  time.sleep(5)
  sys.exit()

def AllinOneClear1():
  if sys.platform == "win32":
    os.system("cls")
  else:
    os.system("clear")
      
class Unifri1():
  def UnifriNetGoods1(self,unifriheaders1):
    try:
      unifrigoodsq1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/get619Activity/v1?whetherFriday=YES",
                                   headers=unifriheaders1,timeout=5).json()
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      return self.UnifriNetGoods1(unifriheaders1)
    if re.findall(r"未登录",str(unifrigoodsq1)) != []:
      print("返回信息: "+unifrigoodsq1["msg"]+"\n联通登录状态失效了,请重新获取Cookie")
      AllinOneExit1()
    unifritabL1 = unifrigoodsq1["resdata"]["tabList"]
    unifrigoodsnl1 = []
    unifrigoodsnl11 = []
    unifrigoodsidl1 = []
    unifripaypril1 = []
    unifrigoodsbtl1 = []
    a = 0
    unifristate1 = {"00":"未开始","10":"抢购","20":"查看","30":"无法抢购",
                    "40":"抢光","50":"待支付","60":"处理中"}
    for b in range(0,len(unifritabL1)):
      for i,goods in enumerate(unifritabL1[b]["goodsList"],a+1):
        unifrigoodsnl11.append(str(i).rjust(2)+" "+unifritabL1[b]["timeNav"]+\
                               unifristate1.get(goods["state"],"未知状态").ljust(4)+" "+goods["goodsName"])
        unifrigoodsnl1.append(goods["goodsName"])
        nowdate1 = time.strftime("%Y-%m-%d",time.localtime(int(time.time())))
        actLtimes1 = int(time.mktime(time.strptime(nowdate1+" "+unifritabL1[b]["timeNav"]+":00",
                                                   "%Y-%m-%d %H:%M:%S"))*1000)
        unifrigoodsbtl1.append(actLtimes1)
      a = i
      for goods in unifritabL1[b]["goodsList"]:
        unifrigoodsidl1.append(goods["goodsId"])
      for goods in unifritabL1[b]["goodsList"]:
        if re.findall(r"\.",str(goods["price"])) != []:
          unifripaypril1.append(str(goods["price"])+"0")
        else:
          unifripaypril1.append(str(goods["price"])+".00")
    unifrigoodsn1 = "\n".join(unifrigoodsnl11)
    print(unifrigoodsq1["msg"]+"\n\n"+unifrigoodsn1)
    unifrigoodss1 = input("\n请输入对应的数字选择商品(多选要用 . 分割,如 1.2.3):")
    if unifrigoodss1 == "" or unifrigoodss1 == "0":
      unifrigoodss1 = 1
    elif re.findall("\.",unifrigoodss1) != []:
      print("已多选,抢购一开始将会按输入顺序先全部抢购一次,然后再单个抢购,成功后自动切换下一个商品\n多选建议从比较好抢到比较难抢的顺序输入(看不懂或不知道的无视这句)\n")
      unifrimultigoodsl1 = []
      unifrigoodsbtl2 = []
      for num in re.findall("\d+",unifrigoodss1):
        unifrigoodsbtl2.append(unifrigoodsbtl1[int(num)-1])
        unifrimultigoodsl1.extend([unifrigoodsnl1[int(num)-1],unifrigoodsidl1[int(num)-1],unifripaypril1[int(num)-1]])
      return unifrigoodsbtl2,unifrimultigoodsl1
    try:
      unifrigoodsn1 = unifrigoodsnl1[int(unifrigoodss1)-1]
      unifrigoodsid1 = unifrigoodsidl1[int(unifrigoodss1)-1]
      unifripaypri1 = unifripaypril1[int(unifrigoodss1)-1]
      if int(unifrigoodss1) > int(a):
        unifrigoodsbt1 = unifrigoodsbtl1[0]
      else:
        unifrigoodsbt1 = unifrigoodsbtl1[int(unifrigoodss1)-1]
      print("已选择商品名称: %s\n对应的商品ID: %s\n对应的商品价格: %s\n"\
            %(unifrigoodsn1,unifrigoodsid1,unifripaypri1))
      return unifrigoodsn1,unifrigoodsid1,unifripaypri1,unifrigoodsbtl1,unifrigoodsbt1
    except IndexError:
      print("请输入仅列出的数字,1秒后重新输入")
      time.sleep(1)
      AllinOneClear1()
      return self.UnifriNetGoods1(unifriheaders1)

  def UnifriLocalGoods1(self):
    unifrigoodsid1 = linecache.getline(r"unifri1cfg.set",26).strip()
    if unifrigoodsid1 == "8a29ac8a72a48dbe0172bb4885430d81":
      unifrigoodsn1 = "美团5元"
      unifripaypri1 = "2.00"
    elif unifrigoodsid1 == "8a29ac8972a48dc10172bb4b994e0cc5":
      unifrigoodsn1 = "美团10元"
      unifripaypri1 = "3.00"
    elif unifrigoodsid1 == "8a29ac8972a48dc10172bb4eebaf0ce7":
      unifrigoodsn1 = "美团30元"
      unifripaypri1 = "10.00"
    elif unifrigoodsid1 == "8a29ac8973e8807e017405894eaa0a70":
      unifrigoodsn1 = "任沃飞"
      unifripaypri1 = "66.00"
    elif unifrigoodsid1 == "8a29ac8973e8807e0174058dea5c0ab5":
      unifrigoodsn1 = "任沃住"
      unifripaypri1 = "66.00"
    elif unifrigoodsid1 == "8a29ac89744fa266017453230dcb0424":
      unifrigoodsn1 = "19.9任意电影票"
      unifripaypri1 = "0.10"
    else:
      unifrigoodsn1 = "月卡"
      unifripaypri1 = "4.90"
    unifrigoodsbt1 = "0"
    print("已选择商品: %s\n对应商品ID: %s\n"%(unifrigoodsn1,unifrigoodsid1))
    return unifrigoodsn1,unifrigoodsid1,unifripaypri1,unifrigoodsbt1

  def UnifriGettime1(self):
    try:
      unifriheaders1 = {"User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36; unicom{version:android@8.0002}"}
      unifritimes1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/getCurrentTimeMillis/v2",
                                  headers=unifriheaders1,timeout=1).json()["resdata"]["currentTime"]
      unifritime1 = time.strftime("%H:%M:%S",time.localtime(unifritimes1/1000))+"."+str(unifritimes1)[-3:]
      return unifritime1
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      print(("可能网络出错了, %s 正在重新尝试对时"%(datetime.datetime.now().strftime("%M:%S"))).ljust(50),end="\r")
      return self.UnifriGettime1()
    except Exception as err:
      print(err)
      return self.UnifriGettime1()

  def UnifriTiming1(self,unifrigoodsbtl1):
    unifrirt1 = []
    for times in unifrigoodsbtl1:
      timef = datetime.datetime.fromtimestamp(times/1000).strftime("%H:%M:%S.%f")[:-3]
      if not timef in unifrirt1:
        unifrirt1.append(timef)
    unifritime1 = self.UnifriGettime1()
    for timef in unifrirt1:
      unifriet1 = linecache.getline(r"unifri1cfg.set",19).strip()
      unifriwm1 = linecache.getline(r"unifri1cfg.set",17).strip()
      unifriwt1 = (datetime.datetime.strptime(timef,"%H:%M:%S.%f")+datetime.timedelta(minutes=-int(unifriwm1))).strftime("%H:%M:%S.%f")[:-3]
      unifriwt11 = (datetime.datetime.strptime(timef,"%H:%M:%S.%f")+datetime.timedelta(minutes=-1)).strftime("%H:%M:%S.%f")[:-3]
      if unifritime1 >= unifriwt1 and unifritime1 < timef:
        timef = (datetime.datetime.strptime(timef,"%H:%M:%S.%f")+datetime.timedelta(milliseconds=-int(unifriet1))).strftime("%H:%M:%S.%f")[:-3]
        print("请勿关闭,程序将在 %s 开抢"%(timef))
        while unifritime1 > unifriwt1 and unifritime1 < timef:
          if unifritime1 < unifriwt11:
            print("当前联通的时间是: %s ,每隔30秒刷新时间"%(unifritime1),end="\r")
            time.sleep(30)
          else:
            print("当前联通的时间是: %s ,每隔0.01秒刷新时间"%(unifritime1),end="\r")
            time.sleep(0.01)
          unifritime1 = self.UnifriGettime1()

  def UnifriGetOrderj1(self,unifriheaders1,unifridata1):
    try:
      unifriorderj1 = requests.get("http://m.client.10010.com/welfare-mall-front/mobile/api/bj2402/v1",
                                   headers=unifriheaders1,params=unifridata1,
                                   timeout=float(linecache.getline(r"unifri1cfg.set",32).strip())).json()
      return unifriorderj1
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      print(("可能网络出错了, %s 正在重新尝试下单"%(datetime.datetime.now().strftime("%M:%S"))).ljust(50),end="\r")
      return self.UnifriGetOrderj1(unifriheaders1,unifridata1)
    except Exception as err:
      print(err)
      return self.UnifriGetOrderj1(unifriheaders1,unifridata1)

  def UnifriCaptcha(self,unifriheaders1,unifriappId):
    try:
      imagep = requests.get("https://act.10010.com/riskService?appId=%s&method=send&riskCode=image"%(r""+unifriappId),
                            headers=unifriheaders1,timeout=5).content.decode("utf-8")
      imagepj = ast.literal_eval(imagep)
      imageUrl = imagepj["imageUrl"].replace("\\","")
      image = requests.get(imageUrl,headers=unifriheaders1,timeout=5)
      with open("unifricaptcha.jpg","wb") as jpg:
        jpg.write(image.content)
        print("验证码 unifricaptcha.jpg 已下载到该目录下,如果没有自动打开图片,请手动打开图片查看")
      if sys.platform == "win32":
        os.system('start "" "unifricaptcha.jpg"')
      elif sys.platform == "darwin":
        os.system('open "unifricaptcha.jpg"')
      else:
        os.system('xdg-open "unifricaptcha.jpg"')
      captcha = input("输入验证码(不区分大小写)后按确定:")
      riskr = requests.get("https://act.10010.com/riskService?appId=%s&method=check&riskCode=image&checkCode=%s"%(r""+unifriappId,captcha),
                           headers=unifriheaders1,timeout=5).content.decode("utf-8")
      riskrj = ast.literal_eval(riskr)
      if riskrj.get("token") != None:
        print("号码已正常,可以继续抢购了")
      else:
        print("验证码出错,重新获取后再输入")
        self.UnifriCaptcha(unifriheaders1,unifriappId)
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      print("该网址有概率访问不了,5秒后重新尝试验证...")
      time.sleep(5)
      self.UnifriCaptcha(unifriheaders1,unifriappId)
    except Exception as err:
      print(err)
      self.UnifriCaptcha(unifriheaders1,unifriappId)

  def UnifriOrdering1(self,unifriaccount,unifriheaders1,unifrigoodsn1,unifridata1):
    try:
      unifriftime1 = linecache.getline(r"unifri1cfg.set",29).strip()
      unifriftimes1 = 1
      unifriorderj1 = self.UnifriGetOrderj1(unifriheaders1,unifridata1)
      unifriorders1 = unifriorderj1["msg"]
      while re.findall(r"下单成功",str(unifriorders1)) == []:
        print("返回信息: "+unifriorders1)
        if unifriftimes1 % 20 == 0:
          try:
            unifriwporderj1 = requests.get("https://m.client.10010.com/welfare-mall-front/mobile/api/bj2404/v1",
                                           headers=unifriheaders1,params='reqsn=&reqtime=&cliver=&reqdata={"orderState":"00","start":"1","limit":10}',
                                           timeout=5).json()
            unifriwporders1 = unifriwporderj1["resdata"]
            if unifriwporders1 != []:
              print("%s有未支付订单,请尽快支付,逾期将失效哦"%(unifriaccount))
              unifriwpgoodsnl1 = []
              for i in unifriwporders1:
                unifriwpgoodsnl1.append(i["goodList"][0]["proName"])
              if unifrigoodsn1 in unifriwpgoodsnl1:
                unifriorders1 = "下单成功"
                break
            else:
              print("%s已查询未支付订单,但未发现有未支付订单,如有需要,请手动在APP查看"%(unifriaccount))
          except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
            pass
          except TypeError:
            print("%s查询未支付订单出错了,可能刷新间隔过短导致限制访问一段时间或联通服务器出现问题,请手动查看是否有未支付订单"%(unifriaccount))
        if re.findall(r"达到上限|数量限制|次数限制|最大限制",str(unifriorders1)) != []:
          print("%s已有订单或不能再次购买该商品\n"%(unifriaccount))
          break
        elif re.findall(r"无法购买请稍候再试",str(unifriorders1)) != [] and int(linecache.getline(r"unifri1cfg.set",42).strip()) == 0:
          print("%s可能已被限制当天所有活动,请下次再参加\n"%(unifriaccount))
          AllinOneExit1()
        elif re.findall(r"活动太火爆，请稍后再试",str(unifriorders1)) != [] and int(linecache.getline(r"unifri1cfg.set",40).strip()) == 1:
          if int(linecache.getline(r"unifri1cfg.set",15).strip()) == 1:
            requests.get("https://sc.ftqq.com/%s.send?text=%s处于半黑状态,需要过一下验证才能继续抢购哦"%(unifriaccount)\
                         %(linecache.getline(r"unifri1cfg.set",37).strip()),timeout=5)
          unifriappId = unifriorderj1["resdata"]
          input("%s处于半黑状态,需要过一下验证才能继续抢购哦\n按确定键继续用程序过验证..."%(unifriaccount))
          self.UnifriCaptcha(unifriheaders1,unifriappId)
        unifriftimes1 += 1
        print("没有下单成功,将在%s秒后第%s次刷新"%(unifriftime1,unifriftimes1))
        time.sleep(float(unifriftime1))
        unifriorderj1 = self.UnifriGetOrderj1(unifriheaders1,unifridata1)
        unifriorders1 = unifriorderj1["msg"]
      if re.findall(r"下单成功",str(unifriorders1)) != []:
        print("%s 已下单成功,请尽快在30分钟内支付,逾期将失效哦"%(unifrigoodsn1))
        with open(unifriaccount+"的商品 "+unifrigoodsn1+" "+\
                  time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"下单成功.ordered","w") as ordered:
          print("已记录%s的商品:%s 下单成功时间"%(unifriaccount,unifrigoodsn1))
        if int(linecache.getline(r"unifri1cfg.set",35).strip()) == 1:
          times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")
          requests.get("https://sc.ftqq.com/%s.send?text=%s %s %s 下单成功,请尽快在30分钟内支付,逾期将失效哦"\
                       %(linecache.getline(r"unifri1cfg.set",37).strip(),times,unifriaccount,unifrigoodsn1),timeout=5)
    except KeyboardInterrupt:
      print("用户中断操作")
      AllinOneExit1()
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      return self.UnifriOrdering1(unifriaccount,unifriheaders1,unifrigoodsn1,unifridata1)
  
  def UnifriMain1(self):
    unifriaccount = linecache.getline(r"unifri1cfg.set",45).strip()
    print("\n正在运行联通超级星期五\n账号为: %s\n"%(unifriaccount))
    unifriheaders1 = {"User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36; unicom{version:android@8.0002}",
                      "ContentType": "application/x-www-form-urlencoded;charset=UTF-8",
                      "Cookie": "%s"%(linecache.getline(r"unifri1cfg.set",48).strip())}
    if int(linecache.getline(r"unifri1cfg.set",24).strip()) == 1:
      unifrigoodsn1,unifrigoodsid1,unifripaypri1,unifrigoodsbt1 = self.UnifriLocalGoods1()
      unifrigoodsq1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/get619Activity/v1?whetherFriday=YES",
                                                     headers=unifriheaders1,timeout=5).json()
      if re.findall(r"未登录",str(unifrigoodsq1)) != []:
        print("返回信息: "+unifrigoodsq1["msg"]+"\n联通登录状态失效了,请重新获取Cookie")
        AllinOneExit1()
    else:
      unifrigoodsmors = self.UnifriNetGoods1(unifriheaders1)
      if len(unifrigoodsmors) == 2:
        unifrigoodsbtl1,unifrimultigoodsl1 = unifrigoodsmors
      else:
        unifrigoodsn1,unifrigoodsid1,unifripaypri1,unifrigoodsbtl1,unifrigoodsbt1 = unifrigoodsmors
        for dirpath,dirnames,filenames in os.walk(os.getcwd()):
          for filename in filenames:
            if re.match(r"%s的商品 %s.*\.ordered"%(unifriaccount,unifrigoodsn1),filename,flags=re.I) != None:
              filemtime = int(os.path.getmtime(filename))
              if int(time.time()) > filemtime+86400:
                os.remove(filename)
              else:
                print("%s的商品: %s 已下单成功了,如果需要再次下单,请先删除目录下对应的.ordered文件"%(unifriaccount,unifrigoodsn1))
                AllinOneExit1()
        unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",'\
                      '"amount":"%s","saleTypes":"C","points":"0","beginTime":"%s",'\
                      '"imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",'\
                      '"sign":"","oneid":"","twoid":"","threeid":"","maxcash":"","floortype":"undefined",'\
                      '"FLSC_PREFECTURE":"SUPER_FRIDAY","launchId":""}'%(unifrigoodsid1,unifripaypri1,unifrigoodsbt1)
    unifriask = input("一次下单不成功后是否需要捡漏,是 输入 y 后按确定,否 直接按确定(多选后务必输入 y ):")
    if unifriask.lower() == "y":
      if int(linecache.getline(r"unifri1cfg.set",15).strip()) == 1:
        self.UnifriTiming1(unifrigoodsbtl1)
        time.sleep(float(linecache.getline(r"unifri1cfg.set",21).strip()))
      try:
        unifrigoodsbt1 = unifrigoodsbtl1[0]
        for i in range(0,len(unifrimultigoodsl1),3):
          unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",'\
                        '"amount":"%s","saleTypes":"C","points":"0","beginTime":"%s",'\
                        '"imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",'\
                        '"sign":"","oneid":"","twoid":"","threeid":"","maxcash":"","floortype":"undefined",'\
                        '"FLSC_PREFECTURE":"SUPER_FRIDAY","launchId":""}'%(unifrimultigoodsl1[i+1],unifrimultigoodsl1[i+2],unifrigoodsbt1)
          self.UnifriGetOrderj1(unifriheaders1,unifridata1)
          time.sleep(float(linecache.getline(r"unifri1cfg.set",29).strip()))
        unifriwporderj1 = requests.get("https://m.client.10010.com/welfare-mall-front/mobile/api/bj2404/v1",
                                       headers=unifriheaders1,params='reqsn=&reqtime=&cliver=&reqdata={"orderState":"00","start":"1","limit":10}',
                                       timeout=5).json()
        if unifriwporderj1["resdata"] != []:
          unifriwpgoodsidl1 = []
          for i in unifriwporderj1["resdata"]:
            unifriwpgoodsidl1.append(i["goodList"][0]["goodsId"])
          for i in unifriwpgoodsidl1:
            print("%s %s 已成功抢购,待支付中,请尽快支付,否则逾期将失效哦"%(unifriaccount,unifrimultigoodsl1[unifrimultigoodsl1.index(i)-1]))
            if int(linecache.getline(r"unifri1cfg.set",35).strip()) == 1:
              times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")
              requests.get("https://sc.ftqq.com/%s.send?text=%s %s %s 已成功抢购,待支付中,请尽快支付,否则逾期将失效哦"\
                           %(linecache.getline(r"unifri1cfg.set",37).strip(),times,unifriaccount,unifrimultigoodsl1[unifrimultigoodsl1.index(i)-1]),
                           timeout=5)
            try:
              del unifrimultigoodsl1[unifrimultigoodsl1.index(i)-1:unifrimultigoodsl1.index(i)+2]
            except ValueError:
              pass
        for i in range(0,len(unifrimultigoodsl1),3):
          unifrigoodsn1 = unifrimultigoodsl1[i]
          print("\n正在抢购 %s\n"%(unifrigoodsn1))
          unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",'\
                        '"amount":"%s","saleTypes":"C","points":"0","beginTime":"%s",'\
                        '"imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",'\
                        '"sign":"","oneid":"","twoid":"","threeid":"","maxcash":"","floortype":"undefined",'\
                        '"FLSC_PREFECTURE":"SUPER_FRIDAY","launchId":""}'%(unifrimultigoodsl1[i+1],unifrimultigoodsl1[i+2],unifrigoodsbt1)
          unifriorderj1 = self.UnifriOrdering1(unifriaccount,unifriheaders1,unifrigoodsn1,unifridata1)
      except UnboundLocalError:
        unifriorderj1 = self.UnifriOrdering1(unifriaccount,unifriheaders1,unifrigoodsn1,unifridata1)
    else:
      try:
        if int(linecache.getline(r"unifri1cfg.set",15).strip()) == 1:
          self.UnifriTiming1(unifrigoodsbtl1)
          time.sleep(float(linecache.getline(r"unifri1cfg.set",21).strip()))
        unifriorders1 = self.UnifriGetOrderj1(unifriheaders1,unifridata1)["msg"]
        if re.findall(r"下单成功",str(unifriorders1)) != []:
          print("%s %s 已下单成功,请尽快在30分钟内支付,逾期将失效哦"%(unifriaccount,unifrigoodsn1))
          with open(unifriaccount+"的商品 "+unifrigoodsn1+" "+\
                        time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"下单成功.ordered","w") as ordered:
            print("已记录%s的商品:%s 下单成功时间"%(unifriaccount,unifrigoodsn1))
          if int(linecache.getline(r"unifri1cfg.set",35).strip()) == 1:
            times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")
            requests.get("https://sc.ftqq.com/%s.send?text=%s %s %s 下单成功,请尽快在30分钟内支付,逾期将失效哦"\
                         %(linecache.getline(r"unifri1cfg.set",37).strip(),times,unifriaccount,unifrigoodsn1),timeout=5)
          time.sleep(10)
        elif re.findall(r"活动太火爆，请稍后再试",str(unifriorders1)) != []:
            unifriappId = unifriorderj1["resdata"]
            input("账号处于半黑状态,需要过一下验证才能继续抢购哦\n按确定键继续用程序过验证...")
            self.UnifriCaptcha(unifriheaders1,unifriappId)
        else:
          print("返回信息: %s"%(unifriorders1))
          time.sleep(30)
      except UnboundLocalError:
        print("多选暂时只支持捡漏模式")
    AllinOneExit1()

class JDCoupon1():
  def JDGetCoupons1(self,jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1):
    try:
      if jdcproleid1 != "0":
        jdgetcouponj1 = requests.get('https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&client=wh5&body={"activityId":"%s","scene":"1","args":"key=%s,roleId=%s"}'%(jdcpactid1,jdcpkeyid1,jdcproleid1),
                                     headers=jdheaders1,timeout=float(linecache.getline(r"jdgetc1cfg.set",22).strip())).json()
      else:
        jdgetcouponj1 = requests.get('https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&client=wh5&body={"activityId":"%s","scene":"3","actKey":"%s"}'%(jdcpactid1,jdcpkeyid1),
                                     headers=jdheaders1,timeout=float(linecache.getline(r"jdgetc1cfg.set",22).strip())).json()
      if re.findall(r"subCodeMsg",str(jdgetcouponj1),flags=re.I) != []:
        jdgetcoupons1 = jdgetcouponj1["subCodeMsg"]
      else:
        jdgetcoupons1 = jdgetcouponj1["errmsg"]
      return jdgetcoupons1
    except:
      return self.JDGetCoupons1(jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1)

  def JDGettime1(self):
    try:
      jdheaders1 = {"User-Agent":"Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"}
      jdtimes1 = requests.get("https://a.jd.com//ajax/queryServerData.html",
                              headers=jdheaders1,timeout=1).json()["serverTime"]
      jdtime1 = datetime.datetime.fromtimestamp(jdtimes1/1000).strftime("%H:%M:%S.%f")[:-3]
      return jdtime1
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      return self.JDGettime1()

  def JDCGetting1(self,jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1):
    try:
      jdgcftime1 = linecache.getline(r"jdgetc1cfg.set",17).strip()
      jdgcftimes1 = 1
      if int(linecache.getline(r"jdgetc1cfg.set",12).strip()) == 1:
        jdrushtime1 = linecache.getline(r"jdgetc1cfg.set",13).strip()
        jdwaittime1 = (datetime.datetime.strptime(jdrushtime1,"%H:%M:%S.%f")+datetime.timedelta(minutes=-30)).strftime("%H:%M:%S.%f")[:-3]
        jdrushtime11 = (datetime.datetime.strptime(jdrushtime1,"%H:%M:%S.%f")+datetime.timedelta(minutes=-1)).strftime("%H:%M:%S.%f")[:-3]
        jdtime1 = self.JDGettime1()
        if jdtime1 > jdwaittime1 and jdtime1 < jdrushtime1:
          print("请勿关闭,程序将在 %s 开抢"%(jdrushtime1))
          while jdtime1 > jdwaittime1 and jdtime1 < jdrushtime1:
            if jdtime1 < jdrushtime11:
              time.sleep(30)
            else:
              time.sleep(0.01)
            jdtime1 = self.JDGettime1()
          time.sleep(float(linecache.getline(r"jdgetc1cfg.set",15).strip()))
      jdgetcoupons1 = self.JDGetCoupons1(jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1)
      while re.findall(r"领取成功",str(jdgetcoupons1)) == []:
        print("返回信息: "+jdgetcoupons1)
        if re.findall(r"领取成功",str(jdgetcoupons1)) != []:
          break
        elif re.findall(r"已经参加过",str(jdgetcoupons1)) != []:
          print("返回信息: %s\n该账号已经领取到优惠券了,请自行查看"%(jdgetcoupons1))
          AllinOneExit1()
        jdgcftimes1 += 1
        if jdgcftimes1 > int(linecache.getline(r"jdgetc1cfg.set",19).strip()):
          print("\n已达到设定的刷新次数\n")
          AllinOneExit1()
        print("没有抢券成功,将在%s秒后第%s次刷新"%(jdgcftime1,jdgcftimes1))
        time.sleep(float(jdgcftime1))
        jdgetcoupons1 = self.JDGetCoupons1(jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1)
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.JDCGetting1(jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1)

  def JDCouponMain1(self):
    print("\n正在运行京东抢任意优惠券\n")
    jdheaders1 = {"User-Agent":"Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
                  "Cookie":"%s"%(linecache.getline(r"jdgetc1cfg.set",30).strip())}
    jdcpactid1 = linecache.getline(r"jdgetc1cfg.set",5).strip()
    jdcpkeyid1 = linecache.getline(r"jdgetc1cfg.set",7).strip()
    jdcproleid1 = linecache.getline(r"jdgetc1cfg.set",9).strip()
    if jdcproleid1 == "0":
      print("当前抢券的 keyid 是: %s\n"%(jdcpkeyid1))
    else:
      print("当前抢券的 keyid 是: %s\nroleid 是: %s\n"%(jdcpkeyid1,jdcproleid1))
    for files in os.walk(os.getcwd()):
      if re.findall("JDCoupon1的优惠券 %s.*\.rushed"%(jdcpkeyid1),str(files),flags=re.I) != []:
        print("该JDCoupon1的优惠券: %s 已抢券成功了,如果需要再次抢券,请先删除目录下对应的.rushed文件"%(jdcpkeyid1))
        AllinOneExit1()
    jdgetcoupons1 = self.JDGetCoupons1(jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1)
    if re.findall(r"not login",str(jdgetcoupons1),flags=re.I) != []:
      print("返回信息: %s\nJD登录状态失效了,请重新获取Cookie"%(jdgetcoupons1))
      AllinOneExit1()
    elif jdgetcoupons1 == None or re.findall(r"activityId invalid",str(jdgetcoupons1),flags=re.I) != []:
      print("返回信息: %s\n活动页面ID错误,请重新获取活动页面ID"%(jdgetcoupons1))
      AllinOneExit1()
    elif re.findall(r"已经参加过",str(jdgetcoupons1)) != []:
      print("返回信息: %s\n该账号已经领取到优惠券了,请自行查看"%(jdgetcoupons1))
      AllinOneExit1()
    elif re.findall(r"来太晚了|结束",str(jdgetcoupons1)) != []:
      print("返回信息: %s\n来晚了,券已过期"%(jdgetcoupons1))
      AllinOneExit1()
    for i in range(5,0,-1):
      print("倒计时 %s 秒"%(i),end="\r")
      time.sleep(1)
    self.JDCGetting1(jdcpactid1,jdcpkeyid1,jdcproleid1,jdheaders1)
    print("%s 抢券成功,请自行查看"%(jdcpkeyid1))
    with open("JDCoupon1的优惠券 "+jdcpkeyid1+" "+\
              time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"抢券成功.rushed","w") as rushed:
      print("已记录JDCoupon1的优惠券:%s 抢券成功时间"%(jdcpkeyid1))
    if int(linecache.getline(r"jdgetc1cfg.set",25).strip()) == 1:
      times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")
      requests.get("https://sc.ftqq.com/%s.send?text=%s %s 抢券成功,请自行查看"\
                   %(linecache.getline(r"jdgetc1cfg.set",27).strip(),times,jdcpkeyid1),timeout=5)
    AllinOneExit1()

def AllinOneMain1():
  funcl = ["1 联通超级星期五 (每周五10点)",
           "2 京东抢任意优惠券"]
  print("功能选择:\n\n"+"\n\n".join(funcl))
  funcsel = input("\n更多整合等待发现,欢迎回复提供\n\n请输入对应数字然后按确定:")
  if funcsel == "" or funcsel == "0":
    funcsel = 1
    print("数字小于1,默认选择第一个 %s"%(funcl[int(funcsel)-1])[2:])
    time.sleep(1)
  if len(funcl)-int(funcsel) >= 0:
    AllinOneClear1()
    if int(funcsel) == 1:
      Unifri1().UnifriMain1()
    elif int(funcsel) == 2:
      JDCoupon1().JDCouponMain1()
  else:
    print("请输入仅列出的数字,1秒后重新输入")
    time.sleep(1)
    AllinOneClear1()
    AllinOneMain1()

try:
  unifrilines1 = len(open(r"unifri1cfg.set",errors="ignore",encoding="UTF-8").readlines())
  if unifrilines1 != 48:
    print("出错了, unifri1cfg.set 的行数不对哦")
    AllinOneExit1()
except FileNotFoundError:
  print("出错了,该目录下没有 unifri1cfg.set 文件哦")
  AllinOneExit1()
try:
  jdgetclines1 = len(open(r"jdgetc1cfg.set",errors="ignore",encoding="UTF-8").readlines())
  if jdgetclines1 != 30:
    print("出错了, jdgetc1cfg.set 的行数不对哦")
    AllinOneExit1()
except FileNotFoundError:
  print("出错了,该目录下没有 jdgetc1cfg.set 文件哦")
  AllinOneExit1()
linecache.updatecache("unifri1cfg.set")
linecache.updatecache("citic3651cfg.set")

if __name__ == "__main__":
  try:
    codedatenow = datetime.datetime.strptime("2021-3-5 19:15","%Y-%m-%d %H:%M")
    codeversionj = requests.get("https://raw.githubusercontent.com/pujie1216/RushCoupon/master/codeversion.json",timeout=5).json()
    codedatenew = datetime.datetime.strptime(codeversionj["codedate"],"%Y-%m-%d %H:%M")
    if codedatenew > codedatenow:
      print("检测到有比较新的代码,更新内容为: \n\n%s"%(codeversionj["changelog"]))
      updateask = input("是否去GitHub更新代码,是 直接按确定键 继续,否 输入 n 后按确定键继续:")
      if updateask == "":
        if sys.platform == "win32":
          os.system("start https://github.com/pujie1216/RushCoupon")
        elif sys.platform == "darwin":
          os.system("open https://github.com/pujie1216/RushCoupon &")
        else:
          os.system("xdg-open https://github.com/pujie1216/RushCoupon &")
        AllinOneExit1()
  except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError) as err:
    print(err)
    print("\n访问GitHub出错,跳过检测更新\n")
  AllinOneMain1()
