# -*- coding: UTF-8 -*-
# Written by xizhi

import os
import platform
import re
import requests
import linecache
import time
import tkinter.messagebox

def AllinOneExit1():
  print("程序5秒后自动退出")
  linecache.clearcache()
  time.sleep(5)
  os._exit(0)

def AllinOneClear1():
  OS = platform.platform()
  if re.findall(r"Windows",OS,flags=re.I) != []:
    os.system("cls")
  else:
    os.system("clear")
      
class Unifri1():  
  def UnifriNetGoods1(self):
    global unifrigoodsn1,unifrigoodsid1,unifripaypri1
    try:
      unifrigoodsidq1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/get619Activity/v1?whetherFriday=YES",cookies=unifricookies1,headers=unifriheaders1,timeout=3).json()
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.UnifriNetGoods1()
    if re.findall(r"未登录",str(unifrigoodsidq1)) != []:
      print("返回信息: "+unifrigoodsidq1["msg"]+"\n联通登录状态失效了,请重新获取Cookie")
      AllinOneExit1()
    unifrigoodsnl1 = []
    unifrigoodsidl1 = []
    for i,goods in enumerate(unifrigoodsidq1["resdata"]["goodsList"],1):
      unifrigoodsnl1.append(str(i)+" "+goods["gOODS_NAME"]) 
    for goods in unifrigoodsidq1["resdata"]["goodsList"]:
      unifrigoodsidl1.append(goods["gOODS_SKU_ID"])
    if re.findall(r"legalRightGoodsList",str(unifrigoodsidq1),flags=re.I) != []:
      for i,goods in enumerate(unifrigoodsidq1["resdata"]["legalRightGoodsList"],i+1):
        unifrigoodsnl1.append(str(i)+" "+goods["gOODS_NAME"]) 
      for goods in unifrigoodsidq1["resdata"]["legalRightGoodsList"]:
        unifrigoodsidl1.append(goods["gOODS_SKU_ID"])
    unifrigoodsn1 = "\n".join(unifrigoodsnl1)
    print(unifrigoodsidq1["msg"]+"\n\n"+unifrigoodsn1)
    unifrigoodss1 = input("\n请输入对应的数字选择商品:")
    if unifrigoodss1 == "" or unifrigoodss1 == "0":
      unifrigoodss1 = 1
      print("数字小于1,默认选择第一个 %s"%(unifrigoodsnl1[int(unifrigoodss1)-1][2:]))
      time.sleep(1)
    try:
      unifrigoodsn1 = unifrigoodsnl1[int(unifrigoodss1)-1][2:]
      unifrigoodsid1 = unifrigoodsidl1[int(unifrigoodss1)-1]
      print("对应的商品ID: "+unifrigoodsid1+"\n")
    except IndexError:
      print("请输入仅列出的数字,1秒后重新输入")
      time.sleep(1)
      AllinOneClear1()
      self.UnifriNetGoods1()
    try:
      unifripaypri1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/getGoodsTradePrice/v1",cookies=unifricookies1,headers=unifriheaders1,timeout=3).json()["resdata"][unifrigoodsid1]
    except:
      pass

  def UnifriLocalGoods1(self):
    global unifrigoodsn1,unifrigoodsid1,unifripaypri1
    unifrigoodsid1 = linecache.getline(r"unifri1cfg.set",20).strip()
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
      unifriorderj1 = requests.post("https://m.client.10010.com/welfare-mall-front/mobile/api/bj2402/v1",headers=unifriheaders1,params=unifridata1,cookies=unifricookies1,timeout=float(linecache.getline(r"unifri1cfg.set",28).strip())).json()
      unifriorders1 = unifriorderj1["msg"]
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,ValueError):
      self.UnifriGetOrders1()

  def UnifriGettime1(self):
    try:
      global unifritime1
      unifritimes1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/getCurrentTimeMillis/v2",headers=unifriheaders1,timeout=3).json()["resdata"]["currentTime"]
      unifritime1 = time.strftime("%H:%M:%S",time.localtime(unifritimes1/1000))
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.UnifriGettime1()

  def UnifriOrdering1(self):
    try:
      unifriftime1 = linecache.getline(r"unifri1cfg.set",25).strip()
      unifriftimes1 = 1
      if int(linecache.getline(r"unifri1cfg.set",15).strip()) == 1:
        self.UnifriGettime1()
        if unifritime1 < "10:00:00":
          print("请勿关闭,程序将在10点0秒开抢")
          while unifritime1 < "10:00:00":
            self.UnifriGettime1()
            time.sleep(0.01)
        elif unifritime1 > "15:00:00":
          print("请勿关闭,程序将在16点0秒开抢")
          while unifritime1 < "16:00:00":
            self.UnifriGettime1()
            time.sleep(0.01)
      while re.findall(r"[^下单成功]",unifriorders1) != []:
        print("返回信息: %s\n没有下单成功,将在%s秒后第%s次刷新"%(unifriorders1,unifriftime1,unifriftimes1))
        self.UnifriGetOrders1()
        if re.findall(r"下单成功",unifriorders1) != []:
          break
        time.sleep(float(unifriftime1))
        unifriftimes1 += 1
      print("%s 下单成功,请尽快在30分钟内支付,逾期将失效哦"%(unifrigoodsn1))
      with open("Unifri1的商品 "+unifrigoodsn1+" "+time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"下单成功.ordered","w") as ordered:
        print("已记录Unifri1的商品:%s 下单成功时间"%(unifrigoodsn1))
      if int(linecache.getline(r"unifri1cfg.set",31).strip()) == 1:
        times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")   #加入时间,避免造成重复消息导致Server酱无法推送
        requests.get("https://sc.ftqq.com/%s.send?text=%s %s 下单成功,请尽快在30分钟内支付,逾期将失效哦"%(linecache.getline(r"unifri1cfg.set",33).strip(),times,unifrigoodsn1))
      AllinOneExit1()
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
      self.UnifriOrdering1()
  
  def UnifriMain1(self):
    global unifriheaders1,unifricookies1,unifridata1
    rechangeno1 = linecache.getline(r"unifri1cfg.set",22).strip()
    print("正在运行联通超级星期五\n当前配置的对应手机号为: %s\n"%(rechangeno1))
    unifriheaders1 = {"User-Agent":"Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36; unicom{version:android@7.0500}"}
    unifricookies1 = {"Cookies":"%s"%(linecache.getline(r"unifri1cfg.set",36).strip())}
    if int(linecache.getline(r"unifri1cfg.set",18).strip()) == 1:
      self.UnifriLocalGoods1()
      unifrigoodsidq1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/get619Activity/v1?whetherFriday=YES",cookies=unifricookies1,headers=unifriheaders1,timeout=3).json()
      if re.findall(r"未登录",str(unifrigoodsidq1)) != []:
        print("返回信息: "+unifrigoodsidq1["msg"]+"\n联通登录状态失效了,请重新获取Cookie")
        AllinOneExit1()
    else:
      self.UnifriNetGoods1()
    for files in os.walk(os.getcwd()):
      if re.findall("Unifri1的商品 %s.*\.ordered"%(unifrigoodsn1),str(files),flags=re.I) != []:
        print("该Unifri1的商品: %s 已下单成功了,如果需要再次下单,请先删除目录下对应的.ordered文件"%(unifrigoodsn1))
        AllinOneExit1()
    unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01","amount":"%s","reChangeNo":"%s","saleTypes":"C","points":"0","beginTime":"","imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"","maxcash":"","floortype":"undefined"}'%(unifrigoodsid1,unifripaypri1,rechangeno1)
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
      citic365orderj1 = requests.post("https://mtp.creditcard.ecitic.com/citiccard/mtp-locallife-app/order/add",headers=citic365headers1,cookies=citic365cookies1,json=citic365data1,timeout=float(linecache.getline(r"citic3651cfg.set",16).strip())).json()
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
      with open("Citic3651的商品 "+citic365skun1+" "+time.strftime("%H{}%M{}%S{}").format("时","分","秒")+"下单成功.ordered","w") as ordered:
        print("已记录Citic3651的商品:%s 下单成功时间"%(citic365skun1))
      if int(linecache.getline(r"citic3651cfg.set",19).strip()) == 1:
        times = time.strftime("%H{}%M{}%S{}").format("时","分","秒")   #加入时间,避免造成重复消息导致Server酱无法推送
        requests.get("https://sc.ftqq.com/%s.send?text=%s %s 下单成功,请尽快在15分钟内支付,逾期将失效哦"%(linecache.getline(r"citic3651cfg.set",21).strip(),times,citic365skun1))
      AllinOneExit1()
    except requests.exceptions.Timeout:
      self.Citic365Ordering1()

  def Citic365Main1(self):
    global citic365headers1,citic365cookies1,citic365data1
    print("正在运行中信365\n")
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
  funcl = ["1 联通超级星期五 (每周五10点和16点)","2 中信365 (每周三周六11点)","3 中行RMB电子券 (每周二10点)","4 中行99积分电子券 (每周四10点)"]
  print("\n\n".join(funcl))
  funcsel = input("\n更多整合等待发现,欢迎回帖提供\n\n请输入对应数字然后按确定:")
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
  else:
    print("请输入仅列出的数字,1秒后重新输入")
    time.sleep(1)
    AllinOneClear1()
    AllinOneMain1()

unifrilines1 = len(open(r"unifri1cfg.set",errors="ignore",encoding="UTF-8").readlines())
if unifrilines1 != 36:
  tkinter.messagebox.showerror("出错了","unifri1cfg.set的行数不对哦\n按确定后自动退出")
  os._exit(0)
citic365lines1 = len(open(r"citic3651cfg.set",errors="ignore",encoding="UTF-8").readlines())
if citic365lines1 != 24:
  tkinter.messagebox.showerror("出错了","citic3651cfg.set的行数不对哦\n按确定后自动退出")
  os._exit(0)
linecache.updatecache("unifri1cfg.set")
linecache.updatecache("citic3651cfg.set")


AllinOneMain1()
