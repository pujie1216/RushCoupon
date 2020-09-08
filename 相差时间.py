import os
import requests
import time
import datetime

dtimel1 = []
for i in range(0,10):
  unitimes1 = requests.get("https://m.client.10010.com/welfare-mall-front-activity/mobile/activity/getCurrentTimeMillis/v2",timeout=5).json()["resdata"]["currentTime"]
  localtimes1 = int(time.time()*1000)
  dtime1 = (unitimes1-localtimes1)/1000
  dtimel1.append(dtime1)
unitime1 = datetime.datetime.fromtimestamp(unitimes1/1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
localtime1 = datetime.datetime.fromtimestamp(localtimes1/1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
print("\n联通时间: %s\n本地时间: %s"%(unitime1,localtime1))
dtime1 = float(sum(dtimel1)/len(dtimel1))
if dtime1 > 0:
  print("本地时间比联通时间平均慢: %.3f 秒"%(abs(dtime1)))
else:
  print("本地时间比联通时间平均快: %.3f 秒"%(abs(dtime1)))
time.sleep(5)
os._exit(0)
