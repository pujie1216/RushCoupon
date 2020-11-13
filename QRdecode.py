# -*- coding: UTF-8 -*-
# Written by xizhi

import os
import time
try:
  from pyzbar.pyzbar import decode
except ImportError:
  print("pyzbar 模块没有安装好哦\n5秒后自动退出")
  time.sleep(5)
  os._exit(0)
try:
  from PIL import Image
except ImportError:
  print("pyzbar 模块的依赖库 pillow 没有安装好哦\n5秒后自动退出")
  time.sleep(5)
  os._exit(0)

print("\n请复制粘贴二维码的图片路径(含后缀)或拖拽二维码的图片到该窗口"\
      "\n如果不想每次都输入路径请将二维码的图片移动到该目录下,然后名字强制改为 q.png ,名字需要完全一样,直接按确定即可"\
      "\n如果一个图片包含多个二维码的会批量解析完")
qrdecodeimg = input("支持常见的图片后缀(gif,png,jpg等):").replace("\"","").replace("\'","")
if qrdecodeimg == "":
  qrdecodeimg = "q.png"
try:
  Image.open(qrdecodeimg).convert("RGBA").save(qrdecodeimg)
  qrdecodel = []
  qrdecode = decode(Image.open(qrdecodeimg))
  for content in qrdecode:
    qrdecodel.append(content.data.decode("utf-8"))
  qrdecode = "\n".join(qrdecodel)
  print("\n解码内容为:\n\n%s\n\n将以上内容各自复制粘贴到需要的地方即可,程序30秒后自动退出"%(qrdecode))
  time.sleep(30)
  os._exit(0)
except FileNotFoundError:
  print("\n该目录下没有 %s 文件哦\n5秒后自动退出"%(qrdecodeimg))
  time.sleep(5)
  os._exit(0)
