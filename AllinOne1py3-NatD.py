# -*- coding: UTF-8 -*-
# Written by xizhi

import os
import platform
import re
import requests
import linecache
import time

def AllinOneExit1():
  print("程序5秒后自动退出")
  linecache.clearcache()
  time.sleep(5)
  os._exit(0)

def AllinOneClear1():
  OS = platform.system()
  if re.findall(r"Windows",OS,flags=re.I) != []:
    os.system("cls")
  else:
    os.system("clear")
      
class Unifri1():
  def UnifriNetGoods1(self):
    global unifrigoodsn1,unifrigoodsid1,unifripaypri1
    try:
      unifrigoodsq1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/get619Activity/v1?whetherFriday=YES",
                                                    cookies=unifricookies1,headers=unifriheaders1,timeout=3).json()
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.UnifriNetGoods1()
    if re.findall(r"未登录",str(unifrigoodsq1)) != []:
      print("返回信息: "+unifrigoodsq1["msg"]+"\n联通登录状态失效了,请重新获取Cookie")
      AllinOneExit1()
    unifriactL1 = unifrigoodsq1["resdata"]["activityList"]
    unifrigoodsnl1 = []
    unifrigoodsnl11 = []
    unifrigoodsidl1 = []
    unifripaypril1 = []
    a = 0
    unifristate1 = {"10":"立即抢购","20":"去查看","30":"","40":"已抢光","50":"未开始"}
    for b in range(0,len(unifriactL1)):
      for i,goods in enumerate(unifriactL1[b]["goodsList"],a+1):
        unifrigoodsnl11.append(str(i)+" "+unifriactL1[b]["navClock"]+\
                              unifristate1.get(goods["state"])+" "+goods["goodsName"])
        unifrigoodsnl1.append(goods["goodsName"])
      a = i
      for goods in unifriactL1[b]["goodsList"]:
        unifrigoodsidl1.append(goods["goodsId"])
      for goods in unifriactL1[b]["goodsList"]:
        unifripaypril1.append(goods["price"]+"0")
    if re.findall(r"legalRightGoodsList",str(unifrigoodsq1),flags=re.I) != []:
      for i,goods in enumerate(unifrigoodsq1["resdata"]["legalRightGoodsList"],i+1):
        unifrigoodsnl1.append(str(i)+" "+goods["gOODS_NAME"]) 
      for goods in unifrigoodsq1["resdata"]["legalRightGoodsList"]:
        unifrigoodsidl1.append(goods["gOODS_SKU_ID"])
    unifrigoodsn1 = "\n".join(unifrigoodsnl11)
    print(unifrigoodsq1["msg"]+"\n\n"+unifrigoodsn1)
    unifrigoodss1 = input("\n请输入对应的数字选择商品:")
    if unifrigoodss1 == "" or unifrigoodss1 == "0":
      unifrigoodss1 = 1
    try:
      unifrigoodsn1 = unifrigoodsnl1[int(unifrigoodss1)-1]
      unifrigoodsid1 = unifrigoodsidl1[int(unifrigoodss1)-1]
      unifripaypri1 = unifripaypril1[int(unifrigoodss1)-1]
      print("已选择商品名称: %s\n对应的商品ID: %s\n对应的商品价格: %s\n"\
               %(unifrigoodsn1,unifrigoodsid1,unifripaypri1))
    except IndexError:
      print("请输入仅列出的数字,1秒后重新输入")
      time.sleep(1)
      AllinOneClear1()
      self.UnifriNetGoods1()

  def UnifriLocalGoods1(self):
    global unifrigoodsn1,unifrigoodsid1,unifripaypri1
    unifrigoodsid1 = linecache.getline(r"unifri1cfg.set",22).strip()
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
    else:
      unifrigoodsn1 = "月卡"
      unifripaypri1 = "4.90"
    print("已选择商品: %s\n对应商品ID: %s\n"%(unifrigoodsn1,unifrigoodsid1))

  def UnifriGetOrders1(self):
    try:
      global unifriorders1
      unifriorderj1 = requests.post("https://m.client.10010.com/welfare-mall-front/mobile/api/bj2402/v1",
                                                   headers=unifriheaders1,params=unifridata1,cookies=unifricookies1,
                                                   timeout=float(linecache.getline(r"unifri1cfg.set",30).strip())).json()
      unifriorders1 = unifriorderj1["msg"]
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      self.UnifriGetOrders1()

  def UnifriGettime1(self):
    try:
      global unifritime1
      unifritimes1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/getCurrentTimeMillis/v2",
                                                headers=unifriheaders1,timeout=3).json()["resdata"]["currentTime"]
      unifritime1 = time.strftime("%H:%M:%S",time.localtime(unifritimes1/1000))
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.UnifriGettime1()

  def UnifriOrdering1(self):
    try:
      unifriftime1 = linecache.getline(r"unifri1cfg.set",27).strip()
      unifriftimes1 = 1
      if int(linecache.getline(r"unifri1cfg.set",15).strip()) == 1:
        self.UnifriGettime1()
        if unifritime1 < "10:00:00":
          print("请勿关闭,程序将在10点0秒开抢")
          while unifritime1 < "10:00:00":
            self.UnifriGettime1()
            time.sleep(0.01)
          time.sleep(float(linecache.getline(r"unifri1cfg.set",17).strip()))
        elif unifritime1 > "11:30:00" and unifritime1 < "12:00:00":
          print("请勿关闭,程序将在12点0秒开抢")
          while unifritime1 < "12:00:00":
            self.UnifriGettime1()
            time.sleep(0.01)
          time.sleep(float(linecache.getline(r"unifri1cfg.set",17).strip()))
        elif unifritime1 > "15:30:00" and unifritime1 < "16:00:00":
          print("请勿关闭,程序将在16点0秒开抢")
          while unifritime1 < "16:00:00":
            self.UnifriGettime1()
            time.sleep(0.01)
          time.sleep(float(linecache.getline(r"unifri1cfg.set",17).strip()))
      while re.findall(r"[^(下单成功|此商品你已达到购买数量限制了~)]",unifriorders1) != []:
        print("返回信息: %s\n没有下单成功,将在%s秒后第%s次刷新"%(unifriorders1,unifriftime1,unifriftimes1))
        self.UnifriGetOrders1()
        if re.findall(r"下单成功",unifriorders1) != []:
          break
        time.sleep(float(unifriftime1))
        unifriftimes1 += 1
      print("%s 已下单成功,请尽快在30分钟内支付,逾期将失效哦"%(unifrigoodsn1))
      with open("Unifri1的商品 "+unifrigoodsn1+" "+\
                      time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"下单成功.ordered","w") as ordered:
        print("已记录Unifri1的商品:%s 下单成功时间"%(unifrigoodsn1))
      if int(linecache.getline(r"unifri1cfg.set",33).strip()) == 1:
        times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")   #加入时间,避免造成重复消息导致Server酱无法推送
        requests.get("https://sc.ftqq.com/%s.send?text=%s %s 下单成功,请尽快在30分钟内支付,逾期将失效哦"\
                            %(linecache.getline(r"unifri1cfg.set",35).strip(),times,unifrigoodsn1))
      AllinOneExit1()
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.UnifriOrdering1()
  
  def UnifriMain1(self):
    global unifriheaders1,unifricookies1,unifridata1
    rechangeno1 = linecache.getline(r"unifri1cfg.set",24).strip()
    print("\n正在运行联通超级星期五 - 国庆节特供\n当前配置的对应手机号为: %s\n"%(rechangeno1))
    unifriheaders1 = {"User-Agent":"Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/\
                                537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36; \
                                unicom{version:android@7.0500}"}
    unifricookies1 = {"Cookies":"%s"%(linecache.getline(r"unifri1cfg.set",38).strip())}
    if int(linecache.getline(r"unifri1cfg.set",20).strip()) == 1:
      self.UnifriLocalGoods1()
      unifrigoodsq1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/get619Activity/v1?whetherFriday=YES",
                                                       cookies=unifricookies1,headers=unifriheaders1,timeout=3).json()
      if re.findall(r"未登录",str(unifrigoodsq1)) != []:
        print("返回信息: "+unifrigoodsq1["msg"]+"\n联通登录状态失效了,请重新获取Cookie")
        AllinOneExit1()
    else:
      self.UnifriNetGoods1()
    for files in os.walk(os.getcwd()):
      if re.findall("Unifri1的商品 %s.*\.ordered"%(unifrigoodsn1),str(files),flags=re.I) != []:
        print("该Unifri1的商品: %s 已下单成功了,如果需要再次下单,请先删除目录下对应的.ordered文件"%(unifrigoodsn1))
        AllinOneExit1()
    unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",\
                         "amount":"%s","reChangeNo":"%s","saleTypes":"C","points":"0","beginTime":"",\
                         "imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",\
                         "maxcash":"","floortype":"undefined"}'%(unifrigoodsid1,unifripaypri1,rechangeno1)
    self.UnifriGetOrders1()
    if re.findall(r"已结束",unifriorders1) != []:
      print("返回信息: "+unifriorders1)
      print("如果活动未开始却显示已结束请直接按确定继续运行\n如果活动真的已结束请输入 e 然后按确定退出程序")
      unifriask1 = input()
      if unifriask1.lower() == "e":
        AllinOneExit1()
    elif re.findall(r"达到上限",unifriorders1) != []:
      print("返回信息: "+unifriorders1)
      print("该账号已不能再次购买\n")
      AllinOneExit1()
    self.UnifriOrdering1()
    
class Citic3651():
  def Citic365LocalGoods1(self):
    global citic365skun1,citic365skuid1
    citic365skuid1 = linecache.getline(r"citic3651cfg.set",10).strip()
    if citic365skuid1 == "37202008130178662128":
      citic365skun1 = "必胜客100元"
    elif citic365skuid1 == "37202008171706774789":
      citic365skun1 = "呷哺呷哺50元"
    elif citic365skuid1 == "37202008111875724259":
      citic365skun1 = "肯德基30元"
    else:
      citic365skun1 = "自定义电子券"
    print("已选择商品: %s\n对应商品ID: %s\n"%(citic365skun1,citic365skuid1))

  def Citic365GetOrders1(self):
    try:
      global citic365orders1
      citic365orderj1 = requests.post("https://mtp.creditcard.ecitic.com/citiccard/mtp-locallife-app/order/add",
                                                        headers=citic365headers1,cookies=citic365cookies1,json=citic365data1,
                                                        timeout=float(linecache.getline(r"citic3651cfg.set",16).strip())).json()
      citic365orders1 = citic365orderj1["retMsg"]
    except requests.exceptions.Timeout:
      self.Citic365GetOrders1()

  def Citic365Ordering1(self):
    try:
      citic365ftime1 = linecache.getline(r"citic3651cfg.set",13).strip()
      citic365ftimes1 = 1
      while re.findall(r"[^处理成功]",citic365orders1) != []:
        print("返回信息: %s\n没有下单成功,将在%s秒后第%s次刷新"%(citic365orders1,citic365ftime1,citic365ftimes1))
        self.Citic365GetOrders1()
        if re.findall(r"下单成功",citic365orders1) != []:
          break
        time.sleep(float(citic365ftime1))
        citic365ftimes1 += 1
      print("%s 下单成功,请尽快在15分钟内支付,逾期将失效哦"%(citic365skun1))
      with open("Citic3651的商品 "+citic365skun1+" "+\
                       time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"下单成功.ordered","w") as ordered:
        print("已记录Citic3651的商品:%s 下单成功时间"%(citic365skun1))
      if int(linecache.getline(r"citic3651cfg.set",19).strip()) == 1:
        times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")   #加入时间,避免造成重复消息导致Server酱无法推送
        requests.get("https://sc.ftqq.com/%s.send?text=%s %s 下单成功,请尽快在15分钟内支付,逾期将失效哦"\
                            %(linecache.getline(r"citic3651cfg.set",21).strip(),times,citic365skun1))
      AllinOneExit1()
    except requests.exceptions.Timeout:
      self.Citic365Ordering1()

  def Citic365Main1(self):
    global citic365headers1,citic365cookies1,citic365data1
    print("\n正在运行中信365\n")
    citic365headers1 = {
      "User-Agent":"Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
      "Connection":"keep-alive",
      "Content-Type":"application/json; charset=UTF-8"
      }
    citic365cookies1 = {"Cookies":"%s"%(linecache.getline(r"citic3651cfg.set",24).strip())}
    self.Citic365LocalGoods1()
    for files in os.walk(os.getcwd()):
      if re.findall("Citic3651的商品 %s.*\.ordered"%(citic365skun1),str(files),flags=re.I) !=[]:
        print("该Citic3651的商品: %s 已下单成功了,如果需要再次下单,请先删除目录下对应的.ordered文件"%(citic365skun1))
        AllinOneExit1()
    citic365data1 = {"skuId":"%s"%(citic365skuid1),"skuNum":1}
    try:
      self.Citic365GetOrders1()
    except ValueError:
      print("可能中信登录状态失效了,请先尝试重新获取Cookie,之后还提示这个的话就是程序有问题了")
      AllinOneExit1()
    if re.findall(r"不在抢购时间内",citic365orders1) != []:
      print("返回信息: "+citic365orders1)
      print("如果活动未开始却显示不在抢购时间内请直接按确定继续运行\n如果活动真的已结束且不在抢购时间内请输入 e 然后按确定退出程序")
      citic365ask1 = input()
      if citic365ask1.lower() == "e":
        AllinOneExit1()
    self.Citic365Ordering1()

def AllinOneMain1():
  funcl = ["1 联通超级星期五 - 国庆节特供",
               "2 中信365 (每周三周六11点)",
               "3 中行RMB电子券 (每周二10点)",
               "4 中行99积分电子券 (每周四10点)",
               "5 龙卡星期六 (每周六11点)"]
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
      Citic3651().Citic365Main1()
    elif int(funcsel) == 3:
      print("等待整合中\n")
      AllinOneExit1()
    elif int(funcsel) == 4:
      print("等待整合中\n")
      AllinOneExit1()
    elif int(funcsel) == 5:
      print("等待整合中\n")
      AllinOneExit1()
  else:
    print("请输入仅列出的数字,1秒后重新输入")
    time.sleep(1)
    AllinOneClear1()
    AllinOneMain1()

try:
  unifrilines1 = len(open(r"unifri1cfg.set",errors="ignore",encoding="UTF-8").readlines())
  if unifrilines1 != 38:
    print("出错了, unifri1cfg.set 的行数不对哦")
    AllinOneExit1()
except FileNotFoundError:
  print("出错了,该目录下没有 unifri1cfg.set 文件哦")
  AllinOneExit1()
try:
  citic365lines1 = len(open(r"citic3651cfg.set",errors="ignore",encoding="UTF-8").readlines())
  if citic365lines1 != 24:
    print("出错了, citic3651cfg.set 的行数不对哦")
    AllinOneExit1()
except FileNotFoundError:
  print("出错了,该目录下没有 citic3651cfg.set 文件哦")
  AllinOneExit1()
linecache.updatecache("unifri1cfg.set")
linecache.updatecache("citic3651cfg.set")

AllinOneMain1()
