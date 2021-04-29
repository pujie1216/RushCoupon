# -*- coding: utf-8 -*-
# Written by xizhi

import sys
import time
try:
    import requests
except (ImportError, ModuleNotFoundError):
    print("请先安装 requests 模块哦,5秒后自动退出")
    time.sleep(5)
    sys.exit()
import os
import re
import linecache
import datetime
import ast

requests.packages.urllib3.disable_warnings()

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

class Notification():
    def getWorkwxtoken(self, corpid, corpsecret):
        resp = requests.get(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (corpid, corpsecret),
            timeout=5).json()
        if resp["errcode"] == 0:
            access_token = resp["access_token"]
            with open("workwx.token", "w") as token:
                token.write(access_token)
            print("企业微信的token已本地记录")
            return access_token
        else:
            print("企业微信的token获取失败: " + resp["errmsg"])
            time.sleep(10)
            sys.exit()

    def sendWorkwxmsg(self, agentid, access_token, message):
        workwxdata = '{"touser":"@all",' \
                     '"msgtype":"text",' \
                     '"agentid":"%s",' \
                     '"text":{"content":"%s"}}' % (agentid, message)
        resp = requests.post("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % (access_token),
                             data=workwxdata.encode("utf-8"), timeout=5).json()
        if resp["errcode"] == 0:
            print("企业微信的推送消息发送成功")
        else:
            print("企业微信的推送消息发送失败: " + resp["errmsg"])

    def WorkwxnoticMain(self, noticsetpath, message):
        workwxidl = linecache.getline(noticsetpath, 8).strip().split(".")
        corpid = workwxidl[0]
        corpsecret = workwxidl[1]
        agentid = workwxidl[2]
        if os.path.isfile("workwx.token"):
            tokengettime = int(os.path.getmtime("workwx.token"))
            tokenexptime = tokengettime + 7200
            if tokenexptime < int(time.time()):
                print("企业微信的本地token可能已过期,正在自动重新获取")
                access_token = self.getWorkwxtoken(corpid, corpsecret)
            else:
                print("企业微信的本地token还在有效期内,继续使用")
                access_token = linecache.getline("workwx.token", 1).strip()
        else:
            access_token = self.getWorkwxtoken(corpid, corpsecret)
        self.sendWorkwxmsg(agentid, access_token, message)

    def BarknoticMain(self, noticsetpath, message):
        try:
            barkey = linecache.getline(noticsetpath, 11).strip()
            requests.get("https://api.day.app/%s/%s" % (barkey, message), timeout=5)
            print("Bark的推送消息发送成功")
        except Exception:
            self.BarknoticMain(noticsetpath, message)

    def DingtalknoticMain(self, noticsetpath, message):
        keyword = linecache.getline(noticsetpath, 14).strip()
        access_token = linecache.getline("notic.set", 15).strip()
        dingtalkdata = '{"msgtype":"text",' \
                       '"text":{"content": "%s\n%s"}}' % (keyword, message)
        resp = requests.post("https://oapi.dingtalk.com/robot/send?access_token=%s" % (access_token),
                             headers={"Content-Type": "application/json;charset=UTF-8"},
                             data=dingtalkdata.encode("utf-8"), timeout=5).json()
        if resp["errcode"] == 0:
            print("钉钉的推送消息发送成功")
        else:
            print("钉钉的推送消息发送失败: " + resp["errmsg"])

    def NoticMain(self, noticsetpath, message):
        notictype = linecache.getline(noticsetpath, 5).strip()
        if notictype == "0":
            print("推送通知没有开启哦\n")
        else:
            message = "%s %s" % (time.strftime("%H{}%M{}%S{}").format("时", "分", "秒"), message)
            if notictype == "1":
                print("当前使用 企业微信 推送通知")
                self.WorkwxnoticMain(noticsetpath, message)
            elif notictype == "2":
                print("当前使用 Bark 推送通知")
                self.BarknoticMain(noticsetpath, message)
            elif notictype == "3":
                print("当前使用 钉钉 推送通知")
                self.DingtalknoticMain(noticsetpath, message)

class Unifri1():
    def UnifriNetGoods1(self, unifriheaders1, unifriacId):
        try:
            unifrigoodsq1 = requests.get(
                "https://m.client.10010.com/welfare-mall-front-activity/super/five/get619Activity/v1?acId=%s" % (
                    unifriacId),
                headers=unifriheaders1, verify=False, timeout=5).json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, ValueError) as err:
            return self.UnifriNetGoods1(unifriheaders1, unifriacId)
        if re.findall(r"获取用户信息异常", str(unifrigoodsq1)) != []:
            print("返回信息: " + unifrigoodsq1["msg"] + "\n联通登录状态失效了,请重新获取Cookie")
            AllinOneExit1()
        unifritabL1 = unifrigoodsq1["resdata"]["tabList"]
        unifrigoodsnl1 = []
        unifrigoodsnl11 = []
        unifrigoodsidl1 = []
        unifripaypril1 = []
        unifrigoodsbtl1 = []
        a = 0
        unifristate1 = {"00": "未开始", "10": "抢购", "20": "查看", "30": "无法抢购",
                        "40": "抢光", "50": "待支付", "60": "处理中"}
        for b in range(0, len(unifritabL1)):
            for i, goods in enumerate(unifritabL1[b]["goodsList"], a + 1):
                unifrigoodsnl11.append(str(i).rjust(2) + " " + unifritabL1[b]["timeNav"] + \
                                       unifristate1.get(goods["state"], "未知状态").ljust(4) + " " + goods["goodsName"])
                unifrigoodsnl1.append(goods["goodsName"])
                nowdate1 = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
                actLtimes1 = int(time.mktime(time.strptime(nowdate1 + " " + unifritabL1[b]["timeNav"] + ":00",
                                                           "%Y-%m-%d %H:%M:%S")) * 1000)
                unifrigoodsbtl1.append(actLtimes1)
            a = i
            for goods in unifritabL1[b]["goodsList"]:
                unifrigoodsidl1.append(goods["goodsId"])
            for goods in unifritabL1[b]["goodsList"]:
                if re.findall(r"\.", str(goods["price"])) != []:
                    unifripaypril1.append(str(goods["price"]) + "0")
                else:
                    unifripaypril1.append(str(goods["price"]) + ".00")
        unifrigoodsn1 = "\n".join(unifrigoodsnl11)
        print(unifrigoodsq1["msg"] + "\n\n" + unifrigoodsn1)
        unifrigoodss1 = input("\n请输入对应的数字选择商品(多选要用 . 分割,如 1.2.3):")
        if unifrigoodss1 == "" or unifrigoodss1 == "0":
            unifrigoodss1 = 1
        elif re.findall("\.", unifrigoodss1) != []:
            print("已多选,抢购一开始将会按输入顺序先全部抢购一次,然后再单个抢购,成功后自动切换下一个商品\n多选建议从比较好抢到比较难抢的顺序输入(看不懂或不知道的无视这句)\n")
            unifrimultigoodsl1 = []
            unifrigoodsbtl2 = []
            for num in re.findall("\d+", unifrigoodss1):
                unifrigoodsbtl2.append(unifrigoodsbtl1[int(num) - 1])
                unifrimultigoodsl1.extend(
                    [unifrigoodsnl1[int(num) - 1], unifrigoodsidl1[int(num) - 1], unifripaypril1[int(num) - 1]])
            return unifrigoodsbtl2, unifrimultigoodsl1
        try:
            unifrigoodsn1 = unifrigoodsnl1[int(unifrigoodss1) - 1]
            unifrigoodsid1 = unifrigoodsidl1[int(unifrigoodss1) - 1]
            unifripaypri1 = unifripaypril1[int(unifrigoodss1) - 1]
            if int(unifrigoodss1) > int(a):
                unifrigoodsbt1 = unifrigoodsbtl1[0]
            else:
                unifrigoodsbt1 = unifrigoodsbtl1[int(unifrigoodss1) - 1]
            print("已选择商品名称: %s\n对应的商品ID: %s\n对应的商品价格: %s\n" \
                  % (unifrigoodsn1, unifrigoodsid1, unifripaypri1))
            return unifrigoodsn1, unifrigoodsid1, unifripaypri1, unifrigoodsbtl1, unifrigoodsbt1
        except IndexError:
            print("请输入仅列出的数字,1秒后重新输入")
            time.sleep(1)
            AllinOneClear1()
            return self.UnifriNetGoods1(unifriheaders1, unifriacId)

    def UnifriLocalGoods1(self):
        unifrigoodsid1 = linecache.getline(r"unifri1cfg.set", 32).strip()
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
        print("已选择商品: %s\n对应商品ID: %s\n" % (unifrigoodsn1, unifrigoodsid1))
        return unifrigoodsn1, unifrigoodsid1, unifripaypri1, unifrigoodsbt1

    def UnifriGettime1(self):
        if int(linecache.getline(r"unifri1cfg.set", 18).strip()) == 0:
            unifritime1 = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        else:
            try:
                unifriheaders1 = {
                    "User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36; unicom{version:android@8.0002}"}
                unifritimes1 = requests.get(
                    "https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/getCurrentTimeMillis/v2",
                    headers=unifriheaders1, verify=False, timeout=1).json()["resdata"]["currentTime"]
                unifritime1 = time.strftime("%H:%M:%S", time.localtime(unifritimes1 / 1000)) + "." + str(unifritimes1)[
                                                                                                     -3:]
                return unifritime1
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, ValueError):
                print(("可能网络出错了, %s 正在重新尝试对时" % (datetime.datetime.now().strftime("%M:%S"))).ljust(50), end="\r")
                return self.UnifriGettime1()
            except Exception as err:
                print(err)
                return self.UnifriGettime1()
        return unifritime1

    def UnifriTiming1(self, unifrigoodsbtl1):
        unifrirt1 = []
        for times in unifrigoodsbtl1:
            timef = datetime.datetime.fromtimestamp(times / 1000).strftime("%H:%M:%S.%f")[:-3]
            if not timef in unifrirt1:
                unifrirt1.append(timef)
        unifritime1 = self.UnifriGettime1()
        for timef in unifrirt1:
            unifriet1 = linecache.getline(r"unifri1cfg.set", 25).strip()
            unifriwm1 = linecache.getline(r"unifri1cfg.set", 23).strip()
            unifriwt1 = (datetime.datetime.strptime(timef, "%H:%M:%S.%f") + datetime.timedelta(
                minutes=-int(unifriwm1))).strftime("%H:%M:%S.%f")[:-3]
            unifriwt11 = (datetime.datetime.strptime(timef, "%H:%M:%S.%f") + datetime.timedelta(minutes=-1)).strftime(
                "%H:%M:%S.%f")[:-3]
            if unifritime1 >= unifriwt1 and unifritime1 < timef:
                timef = (datetime.datetime.strptime(timef, "%H:%M:%S.%f") + datetime.timedelta(
                    milliseconds=-int(unifriet1))).strftime("%H:%M:%S.%f")[:-3]
                print("请勿关闭,程序将在 %s 开抢" % (timef))
                while unifritime1 > unifriwt1 and unifritime1 < timef:
                    if unifritime1 < unifriwt11:
                        print("当前的时间是: %s ,每隔30秒刷新时间" % (unifritime1), end="\r")
                        time.sleep(30)
                    else:
                        print("当前的时间是: %s ,每隔0.01秒刷新时间" % (unifritime1), end="\r")
                        time.sleep(0.01)
                    unifritime1 = self.UnifriGettime1()

    def UnifriGetOrderj1(self, unifriheaders1, unifridata1):
        try:
            unifriorderj1 = requests.get("https://m.client.10010.com/welfare-mall-front/mobile/api/bj2402/v1",
                                         headers=unifriheaders1, params=unifridata1, verify=False,
                                         timeout=float(linecache.getline(r"unifri1cfg.set", 38).strip())).json()
            return unifriorderj1
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, ValueError):
            print(("可能网络出错了, %s 正在重新尝试下单" % (datetime.datetime.now().strftime("%M:%S"))).ljust(50), end="\r")
            return self.UnifriGetOrderj1(unifriheaders1, unifridata1)
        except Exception as err:
            print(err)
            return self.UnifriGetOrderj1(unifriheaders1, unifridata1)

    def UnifriCaptcha(self, unifriheaders1, unifriappId):
        try:
            imagep = requests.get(
                "https://act.10010.com/riskService?appId=%s&method=send&riskCode=image" % (r"" + unifriappId),
                headers=unifriheaders1, verify=False, timeout=5).content.decode("utf-8")
            imagepj = ast.literal_eval(imagep)
            imageUrl = imagepj.get("imageUrl")
            if imageUrl is None:
                print("无法获取验证码了")
            else:
                imageUrl = imageUrl.replace("\\", "")
                image = requests.get(imageUrl, headers=unifriheaders1, verify=False, timeout=5)
                with open("unifricaptcha.jpg", "wb") as jpg:
                    jpg.write(image.content)
                    print("验证码 unifricaptcha.jpg 已下载到该目录下,如果没有自动打开图片,请手动打开图片查看")
                if sys.platform == "win32":
                    os.system('start "" "unifricaptcha.jpg"')
                elif sys.platform == "darwin":
                    os.system('open "unifricaptcha.jpg"')
                else:
                    os.system('xdg-open "unifricaptcha.jpg"')
                captcha = input("输入验证码(不区分大小写)后按确定:")
                riskr = requests.get(
                    "https://act.10010.com/riskService?appId=%s&method=check&riskCode=image&checkCode=%s&systemCode=19991" % (
                        r"" + unifriappId, captcha),
                    headers=unifriheaders1, verify=False, timeout=5).content.decode("utf-8")
                riskrj = ast.literal_eval(riskr)
                if riskrj.get("token") is not None:
                    print("号码已正常,可以继续抢购了")
                else:
                    print("验证码出错,重新获取后再输入")
                    self.UnifriCaptcha(unifriheaders1, unifriappId)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            print("该网址有概率访问不了,5秒后重新尝试验证...")
            time.sleep(5)
            self.UnifriCaptcha(unifriheaders1, unifriappId)
        except Exception as err:
            print(err)
            self.UnifriCaptcha(unifriheaders1, unifriappId)

    def UnifriOrdering1(self, noticsetpath, unifriaccount, unifriheaders1, unifrigoodsn1, unifridata1):
        try:
            unifriftime1 = linecache.getline(r"unifri1cfg.set", 35).strip()
            unifriftimes1 = 1
            unifriorderj1 = self.UnifriGetOrderj1(unifriheaders1, unifridata1)
            unifriorders1 = unifriorderj1["msg"]
            while re.findall(r"下单成功", str(unifriorders1)) == []:
                print("返回信息: " + unifriorders1)
                if unifriftimes1 % 20 == 0:
                    try:
                        unifriwporderj1 = requests.get(
                            "https://m.client.10010.com/welfare-mall-front/mobile/api/bj2404/v1",
                            headers=unifriheaders1,
                            params='reqsn=&reqtime=&cliver=&reqdata={"orderState":"00","start":"1","limit":10}',
                            verify=False,
                            timeout=5).json()
                        unifriwporders1 = unifriwporderj1["resdata"]
                        if unifriwporders1 != []:
                            print("%s有未支付订单,请尽快支付,逾期将失效哦" % (unifriaccount))
                            unifriwpgoodsnl1 = []
                            for i in unifriwporders1:
                                unifriwpgoodsnl1.append(i["goodList"][0]["proName"])
                            if unifrigoodsn1 in unifriwpgoodsnl1:
                                unifriorders1 = "下单成功"
                                break
                        else:
                            print("%s已查询未支付订单,但未发现有未支付订单,如有需要,请手动在APP查看" % (unifriaccount))
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        pass
                    except (TypeError, ValueError):
                        print("%s查询未支付订单出错了,可能刷新间隔过短导致限制访问一段时间或联通服务器出现问题,请手动查看是否有未支付订单" % (unifriaccount))
                if re.findall(r"达到上限|数量限制|次数限制|最大限制", str(unifriorders1)) != []:
                    print("%s已有订单或不能再次购买该商品\n" % (unifriaccount))
                    break
                elif re.findall(r"无法购买请稍候再试", str(unifriorders1)) != [] and int(
                        linecache.getline(r"unifri1cfg.set", 43).strip()) == 0:
                    print("%s可能已被限制当天所有活动,请下次再参加\n" % (unifriaccount))
                    AllinOneExit1()
                elif re.findall(r"活动太火爆，请稍后再试|系统开小差了", str(unifriorders1)) != [] and int(
                        linecache.getline(r"unifri1cfg.set", 41).strip()) == 1:
                    message = "%s处于半黑状态,需要过一下验证才能继续抢购哦" % (unifriaccount)
                    if noticsetpath != "false":
                        Notification().NoticMain(noticsetpath, message)
                    unifriappId = unifriorderj1["resdata"]
                    input("%s\n按确定键继续用程序过验证..." % (message))
                    self.UnifriCaptcha(unifriheaders1, unifriappId)
                unifriftimes1 += 1
                print("没有下单成功,将在%s秒后第%s次刷新" % (unifriftime1, unifriftimes1))
                time.sleep(float(unifriftime1))
                unifriorderj1 = self.UnifriGetOrderj1(unifriheaders1, unifridata1)
                unifriorders1 = unifriorderj1["msg"]
            if re.findall(r"下单成功", str(unifriorders1)) != []:
                message = "%s %s 已下单成功,请尽快在30分钟内支付,逾期将失效哦" % (unifriaccount, unifrigoodsn1)
                print(message)
                with open(unifriaccount + "的商品 " + unifrigoodsn1 + " " + \
                          time.strftime("%H{}%M{}%S{}").format("时", "分", "秒") + "下单成功.ordered", "w"):
                    print("已记录%s的商品:%s 下单成功时间" % (unifriaccount, unifrigoodsn1))
                if noticsetpath != "false":
                    Notification().NoticMain(noticsetpath, message)
        except KeyboardInterrupt:
            print("用户中断操作")
            AllinOneExit1()
        except Exception as err:
            print(err)
            self.UnifriOrdering1(noticsetpath, unifriaccount, unifriheaders1, unifrigoodsn1, unifridata1)

    def UnifriMain1(self):
        noticpath = linecache.getline(r"unifri1cfg.set", 52).strip()
        noticsetpath = noticpath + "/notic.set"
        try:
            noticlines = len(open(noticsetpath, errors="ignore", encoding="UTF-8").readlines())
            if noticlines != 15:
                print("出错了, notic.set 的行数不对,将无法开启推送通知哦")
                noticsetpath = "false"
        except FileNotFoundError:
            print("该目录下没有 notic.set 文件,将无法开启推送通知哦")
            noticsetpath = "false"
        if noticsetpath != "false":
            linecache.updatecache(noticsetpath)
        unifriaccount = linecache.getline(r"unifri1cfg.set", 46).strip()
        print("\n正在运行联通超级星期五\n账号为: %s\n" % (unifriaccount))
        unifriheaders1 = {
            "User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36; unicom{version:android@8.0002}",
            "ContentType": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cookie": "%s" % (linecache.getline(r"unifri1cfg.set", 49).strip())}
        unifriacId = linecache.getline(r"unifri1cfg.set", 15).strip()
        if unifriacId == "auto":
            acIdpt = requests.post("https://m.client.10010.com/h5-web_pro/interface/service_0005_0002",
                                   headers=unifriheaders1, data='{"id":"88888","_su_pass":"_sunc_vl"}',
                                   timeout=5).text
            unifriacId = re.match(r'.*\\"activityNumber\\":\\"(.*?\d+)\\".*', acIdpt, flags=re.I).group(1)
        if int(linecache.getline(r"unifri1cfg.set", 30).strip()) == 1:
            unifrigoodsn1, unifrigoodsid1, unifripaypri1, unifrigoodsbt1 = self.UnifriLocalGoods1()
            unifrigoodsq1 = requests.get(
                "https://m.client.10010.com/welfare-mall-front-activity/super/five/get619Activity/v1?acId=%s" % (
                    unifriacId),
                headers=unifriheaders1, verify=False, timeout=5).json()
            if re.findall(r"获取用户信息异常", str(unifrigoodsq1)) != []:
                print("返回信息: " + unifrigoodsq1["msg"] + "\n联通登录状态失效了,请重新获取Cookie")
                AllinOneExit1()
        else:
            unifrigoodsmors = self.UnifriNetGoods1(unifriheaders1, unifriacId)
            if len(unifrigoodsmors) == 2:
                unifrigoodsbtl1, unifrimultigoodsl1 = unifrigoodsmors
            else:
                unifrigoodsn1, unifrigoodsid1, unifripaypri1, unifrigoodsbtl1, unifrigoodsbt1 = unifrigoodsmors
                for dirpath, dirnames, filenames in os.walk(os.getcwd()):
                    for filename in filenames:
                        if re.match(r"%s的商品 %s.*\.ordered" % (unifriaccount, unifrigoodsn1), filename,
                                    flags=re.I) is not None:
                            filemtime = int(os.path.getmtime(filename))
                            if int(time.time()) > (filemtime + 86400):
                                os.remove(filename)
                            else:
                                print("%s的商品: %s 已下单成功了,如果需要再次下单,请先删除目录下对应的.ordered文件" % (unifriaccount, unifrigoodsn1))
                                AllinOneExit1()
                unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",' \
                              '"amount":"%s","saleTypes":"C","points":"0","beginTime":"%s",' \
                              '"imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",' \
                              '"sign":"","oneid":"","twoid":"","threeid":"","maxcash":"","floortype":"undefined",' \
                              '"FLSC_PREFECTURE":"SUPER_FRIDAY","launchId":"","platAcId":"%s"}' % (
                                  unifrigoodsid1, unifripaypri1, unifrigoodsbt1, unifriacId)
        unifriask = input("一次下单不成功后是否需要捡漏,是 输入 y 后按确定,否 直接按确定(多选后务必输入 y ):")
        if unifriask.lower() == "y":
            if int(linecache.getline(r"unifri1cfg.set", 21).strip()) == 1:
                self.UnifriTiming1(unifrigoodsbtl1)
                time.sleep(float(linecache.getline(r"unifri1cfg.set", 27).strip()))
            try:
                unifrigoodsbt1 = unifrigoodsbtl1[0]
                for i in range(0, len(unifrimultigoodsl1), 3):
                    unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",' \
                                  '"amount":"%s","saleTypes":"C","points":"0","beginTime":"%s",' \
                                  '"imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",' \
                                  '"sign":"","oneid":"","twoid":"","threeid":"","maxcash":"","floortype":"undefined",' \
                                  '"FLSC_PREFECTURE":"SUPER_FRIDAY","launchId":"","platAcId":"%s"}' % (
                                      unifrimultigoodsl1[i + 1], unifrimultigoodsl1[i + 2], unifrigoodsbt1, unifriacId)
                    self.UnifriGetOrderj1(unifriheaders1, unifridata1)
                    time.sleep(float(linecache.getline(r"unifri1cfg.set", 35).strip()))
                unifriwporderj1 = requests.get("https://m.client.10010.com/welfare-mall-front/mobile/api/bj2404/v1",
                                               headers=unifriheaders1,
                                               params='reqsn=&reqtime=&cliver=&reqdata={"orderState":"00","start":"1","limit":10}',
                                               verify=False,
                                               timeout=5).json()
                if unifriwporderj1["resdata"] != []:
                    unifriwpgoodsidl1 = []
                    for i in unifriwporderj1["resdata"]:
                        unifriwpgoodsidl1.append(i["goodList"][0]["goodsId"])
                    for i in unifriwpgoodsidl1:
                        message = "%s %s 已成功抢购,待支付中,请尽快支付,否则逾期将失效哦" % (
                            unifriaccount, unifrimultigoodsl1[unifrimultigoodsl1.index(i) - 1])
                        print(message)
                        if noticsetpath != "false":
                            Notification().NoticMain(noticsetpath, message)
                        try:
                            del unifrimultigoodsl1[unifrimultigoodsl1.index(i) - 1:unifrimultigoodsl1.index(i) + 2]
                        except ValueError:
                            pass
                for i in range(0, len(unifrimultigoodsl1), 3):
                    unifrigoodsn1 = unifrimultigoodsl1[i]
                    print("\n正在抢购 %s\n" % (unifrigoodsn1))
                    unifridata1 = 'reqsn=&reqtime=&cliver=&reqdata={"goodsId":"%s","payWay":"01",' \
                                  '"amount":"%s","saleTypes":"C","points":"0","beginTime":"%s",' \
                                  '"imei":"undefined","sourceChannel":"","proFlag":"","scene":"","pormoterCode":"",' \
                                  '"sign":"","oneid":"","twoid":"","threeid":"","maxcash":"","floortype":"undefined",' \
                                  '"FLSC_PREFECTURE":"SUPER_FRIDAY","launchId":"","platAcId":"%s"}' % (
                                      unifrimultigoodsl1[i + 1], unifrimultigoodsl1[i + 2], unifrigoodsbt1, unifriacId)
                    self.UnifriOrdering1(noticsetpath, unifriaccount, unifriheaders1, unifrigoodsn1, unifridata1)
            except UnboundLocalError:
                self.UnifriOrdering1(noticsetpath, unifriaccount, unifriheaders1, unifrigoodsn1, unifridata1)
        else:
            try:
                if int(linecache.getline(r"unifri1cfg.set", 21).strip()) == 1:
                    self.UnifriTiming1(unifrigoodsbtl1)
                    time.sleep(float(linecache.getline(r"unifri1cfg.set", 27).strip()))
                unifriorderj1 = self.UnifriGetOrderj1(unifriheaders1, unifridata1)
                unifriorders1 = unifriorderj1["msg"]
                if re.findall(r"下单成功", str(unifriorders1)) != []:
                    message = "%s %s 已下单成功,请尽快在30分钟内支付,逾期将失效哦" % (unifriaccount, unifrigoodsn1)
                    print(message)
                    with open(unifriaccount + "的商品 " + unifrigoodsn1 + " " + \
                              time.strftime("%H{}%M{}%S{}").format("时", "分", "秒") + "下单成功.ordered", "w"):
                        print("已记录%s的商品:%s 下单成功时间" % (unifriaccount, unifrigoodsn1))
                    if noticsetpath != "false":
                        Notification().NoticMain(noticsetpath, message)
                    time.sleep(10)
                elif re.findall(r"活动太火爆，请稍后再试|系统开小差了", str(unifriorders1)) != [] and int(
                        linecache.getline(r"unifri1cfg.set", 41).strip()) == 1:
                    unifriappId = unifriorderj1["resdata"]
                    input("账号处于半黑状态,需要过一下验证才能继续抢购哦\n按确定键继续用程序过验证...")
                    self.UnifriCaptcha(unifriheaders1, unifriappId)
                else:
                    print("返回信息: %s" % (unifriorders1))
                    time.sleep(30)
            except UnboundLocalError:
                print("多选暂时只支持捡漏模式")
        AllinOneExit1()

class JDCoupon1():
    def JDGetCoupons1(self, jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1):
        try:
            if jdcproleid1 != "0":
                jdgetcouponj1 = requests.get(
                    'https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&client=wh5&body={"activityId":"%s","scene":"1","args":"key=%s,roleId=%s"}' % (
                        jdcpactid1, jdcpkeyid1, jdcproleid1),
                    headers=jdheaders1, timeout=float(linecache.getline(r"jdgetc1cfg.set", 22).strip())).json()
            else:
                jdgetcouponj1 = requests.get(
                    'https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&client=wh5&body={"activityId":"%s","scene":"3","actKey":"%s"}' % (
                        jdcpactid1, jdcpkeyid1),
                    headers=jdheaders1, timeout=float(linecache.getline(r"jdgetc1cfg.set", 22).strip())).json()
            if re.findall(r"subCodeMsg", str(jdgetcouponj1), flags=re.I) != []:
                jdgetcoupons1 = jdgetcouponj1["subCodeMsg"]
            else:
                jdgetcoupons1 = jdgetcouponj1["errmsg"]
            return jdgetcoupons1
        except Exception:
            return self.JDGetCoupons1(jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1)

    def JDGettime1(self, errcount):
        try:
            jdheaders1 = {
                "User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"}
            jdtimes1 = requests.get("https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5",
                                    headers=jdheaders1, timeout=1).json()["currentTime2"]
            # 已失效的旧时间接口:https://a.jd.com//ajax/queryServerData.html
            jdtime1 = datetime.datetime.fromtimestamp(int(jdtimes1) / 1000).strftime("%H:%M:%S.%f")[:-3]
            errcount = 0
            return jdtime1, errcount
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return self.JDGettime1(errcount)
        except (ValueError):
            errcount += 1
            if errcount > 2:
                jdtime1 = datetime.datetime.fromtimestamp(int(time.time() * 1000) / 1000).strftime("%H:%M:%S.%f")[:-3]
                print("京东时间接口可能失效,已改用本地时间,自行校准时间")
                return jdtime1, errcount
            return self.JDGettime1(errcount)

    def JDCGetting1(self, jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1):
        try:
            jdgcftime1 = linecache.getline(r"jdgetc1cfg.set", 17).strip()
            jdgcftimes1 = 1
            if int(linecache.getline(r"jdgetc1cfg.set", 12).strip()) == 1:
                jdrushtime1 = linecache.getline(r"jdgetc1cfg.set", 13).strip()
                jdwaittime1 = (datetime.datetime.strptime(jdrushtime1, "%H:%M:%S.%f") + datetime.timedelta(
                    minutes=-30)).strftime("%H:%M:%S.%f")[:-3]
                jdrushtime11 = (datetime.datetime.strptime(jdrushtime1, "%H:%M:%S.%f") + datetime.timedelta(
                    minutes=-1)).strftime("%H:%M:%S.%f")[:-3]
                errcount = 0
                jdtime1, errcount = self.JDGettime1(errcount)
                if jdtime1 > jdwaittime1 and jdtime1 < jdrushtime1:
                    print("请勿关闭,程序将在 %s 开抢" % (jdrushtime1))
                    while jdtime1 > jdwaittime1 and jdtime1 < jdrushtime1:
                        if jdtime1 < jdrushtime11:
                            print("当前京东的时间是: %s ,每隔30秒刷新时间" % (jdtime1), end="\r")
                            time.sleep(30)
                        else:
                            print("当前京东的时间是: %s ,每隔0.01秒刷新时间" % (jdtime1), end="\r")
                            time.sleep(0.01)
                        jdtime1, errcount = self.JDGettime1(errcount)
                    time.sleep(float(linecache.getline(r"jdgetc1cfg.set", 15).strip()))
            jdgetcoupons1 = self.JDGetCoupons1(jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1)
            while re.findall(r"领取成功", str(jdgetcoupons1)) == []:
                print("返回信息: " + jdgetcoupons1)
                if re.findall(r"领取成功", str(jdgetcoupons1)) != []:
                    break
                elif re.findall(r"已经参加过", str(jdgetcoupons1)) != []:
                    print("返回信息: %s\n该账号已经领取到优惠券了,请自行查看" % (jdgetcoupons1))
                    AllinOneExit1()
                jdgcftimes1 += 1
                if jdgcftimes1 > int(linecache.getline(r"jdgetc1cfg.set", 19).strip()):
                    print("\n已达到设定的刷新次数\n")
                    AllinOneExit1()
                print("没有抢券成功,将在%s秒后第%s次刷新" % (jdgcftime1, jdgcftimes1))
                time.sleep(float(jdgcftime1))
                jdgetcoupons1 = self.JDGetCoupons1(jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.JDCGetting1(jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1)

    def JDCouponMain1(self):
        noticpath = linecache.getline(r"jdgetc1cfg.set", 28).strip()
        noticsetpath = noticpath + "/notic.set"
        try:
            noticlines = len(open(noticsetpath, errors="ignore", encoding="UTF-8").readlines())
            if noticlines != 15:
                print("出错了, notic.set 的行数不对,将无法开启推送通知哦")
                noticsetpath = "false"
        except FileNotFoundError:
            print("该目录下没有 notic.set 文件,将无法开启推送通知哦")
            noticsetpath = "false"
        if noticsetpath != "false":
            linecache.updatecache(noticsetpath)
        print("\n正在运行京东抢任意优惠券\n")
        jdheaders1 = {
            "User-Agent": "Mozilla/5.0 (Linux;Android 10;GM1910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
            "Cookie": "%s" % (linecache.getline(r"jdgetc1cfg.set", 25).strip())}
        jdcpactid1 = linecache.getline(r"jdgetc1cfg.set", 5).strip()
        jdcpkeyid1 = linecache.getline(r"jdgetc1cfg.set", 7).strip()
        jdcproleid1 = linecache.getline(r"jdgetc1cfg.set", 9).strip()
        if jdcproleid1 == "0":
            print("当前抢券的 keyid 是: %s\n" % (jdcpkeyid1))
        else:
            print("当前抢券的 keyid 是: %s\nroleid 是: %s\n" % (jdcpkeyid1, jdcproleid1))
        for files in os.walk(os.getcwd()):
            if re.findall(r"JDCoupon1的优惠券 %s.*\.rushed" % (jdcpkeyid1), str(files), flags=re.I) != []:
                print("该JDCoupon1的优惠券: %s 已抢券成功了,如果需要再次抢券,请先删除目录下对应的.rushed文件" % (jdcpkeyid1))
                AllinOneExit1()
        jdgetcoupons1 = self.JDGetCoupons1(jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1)
        if re.findall(r"not login", str(jdgetcoupons1), flags=re.I) != []:
            print("返回信息: %s\nJD登录状态失效了,请重新获取Cookie" % (jdgetcoupons1))
            AllinOneExit1()
        elif jdgetcoupons1 is None or re.findall(r"activityId invalid", str(jdgetcoupons1), flags=re.I) != []:
            print("返回信息: %s\n活动页面ID错误,请重新获取活动页面ID" % (jdgetcoupons1))
            AllinOneExit1()
        elif re.findall(r"已经参加过", str(jdgetcoupons1)) != []:
            print("返回信息: %s\n该账号已经领取到优惠券了,请自行查看" % (jdgetcoupons1))
            AllinOneExit1()
        elif re.findall(r"来太晚了|结束", str(jdgetcoupons1)) != []:
            print("返回信息: %s\n来晚了,券已过期" % (jdgetcoupons1))
            AllinOneExit1()
        # 删除倒计时5秒,有需要自行打开
        """
        for i in range(5,0,-1):
          print("倒计时 %s 秒"%(i),end="\r")
          time.sleep(1)
        """
        self.JDCGetting1(jdcpactid1, jdcpkeyid1, jdcproleid1, jdheaders1)
        message = "%s 抢券成功,请自行查看" % (jdcpkeyid1)
        print(message)
        with open("JDCoupon1的优惠券 " + jdcpkeyid1 + " " + \
                  time.strftime("%H{}%M{}%S{}").format("时", "分", "秒") + "抢券成功.rushed", "w"):
            print("已记录JDCoupon1的优惠券:%s 抢券成功时间" % (jdcpkeyid1))
        if noticsetpath != "false":
            Notification().NoticMain(noticsetpath, message)
        AllinOneExit1()

def AllinOneMain1():
    funcl = ["1 联通超级星期五 (每周五10点起)",
             "2 京东抢任意优惠券"]
    print("功能选择:\n\n" + "\n\n".join(funcl))
    funcsel = input("\n更多整合等待发现,欢迎回复提供\n\n请输入对应数字然后按确定:")
    if funcsel == "" or funcsel == "0":
        funcsel = 1
        print("数字小于1,默认选择第一个 %s" % (funcl[int(funcsel) - 1])[2:])
        time.sleep(1)
    if len(funcl) - int(funcsel) >= 0:
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
    unifrilines1 = len(open(r"unifri1cfg.set", errors="ignore", encoding="UTF-8").readlines())
    if unifrilines1 != 52:
        print("出错了, unifri1cfg.set 的行数不对哦")
        AllinOneExit1()
except FileNotFoundError:
    print("出错了,该目录下没有 unifri1cfg.set 文件哦")
    AllinOneExit1()
try:
    jdgetclines1 = len(open(r"jdgetc1cfg.set", errors="ignore", encoding="UTF-8").readlines())
    if jdgetclines1 != 28:
        print("出错了, jdgetc1cfg.set 的行数不对哦")
        AllinOneExit1()
except FileNotFoundError:
    print("出错了,该目录下没有 jdgetc1cfg.set 文件哦")
    AllinOneExit1()
linecache.updatecache("unifri1cfg.set")
linecache.updatecache("jdgetc1cfg.set")

try:
    codedatenow = datetime.datetime.strptime("2021-4-29 22:00", "%Y-%m-%d %H:%M")
    codeversionj = requests.get("https://raw.githubusercontent.com/pujie1216/RushCoupon/master/codeversion.json",
                                timeout=5).json()
    codedatenew = datetime.datetime.strptime(codeversionj["codedate"], "%Y-%m-%d %H:%M")
    if codedatenew > codedatenow:
        print("检测到有比较新的代码,更新内容为:\n\n%s" % (codeversionj["changelog"]))
        updateask = input("是否去GitHub更新代码,是 直接按确定键 继续,否 输入 n 后按确定键继续:")
        if updateask == "":
            if sys.platform == "win32":
                os.system("start https://github.com/pujie1216/RushCoupon")
            elif sys.platform == "darwin":
                os.system("open https://github.com/pujie1216/RushCoupon &")
            else:
                os.system("xdg-open https://github.com/pujie1216/RushCoupon &")
            AllinOneExit1()
except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, ValueError) as err:
    print(err)
    print("\n访问GitHub出错,跳过检测更新\n")
AllinOneMain1()
