::Written by xizhi
@echo off
title 安装额外模块
python -m ensurepip
python -m pip install requests
python -m pip install rsa
python -m pip install qrcode
python -m pip install Pillow
echo.&echo 没有红色错误就按任意键完成安装&pause>nul
