#!/usr/bin/python3

'''
pip install qrcode, zxing

生成 二维码
解析 二维码

【红色】：red 【橙色】：orange 【黄色】：yellow 【绿】：green 【 蓝】：blue【紫】：purple 
【灰色】：gray 【白色】：white 【粉红色】：pink 【黑色】：black【墨绿色】：dark green 【橙红色】：orange-red
'''


import qrcode
import os
from PIL import Image
import zxing


def create_qr(s, n):

  qr = qrcode.QRCode(
      version=10,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=100,
      border=4,
      )
  qr.add_data(s)
  qr.make(fit=True)

  img = qr.make_image(fill_color="blue", back_color="white")
  img.save(n)


def create_logo_qr(s, n, logo):

  qr = qrcode.QRCode(
      version=5,
      error_correction=qrcode.constants.ERROR_CORRECT_H,
      box_size=20,
      border=4,
      )
  qr.add_data(s)
  qr.make(fit=True)

  img = qr.make_image(fill_color="blue", back_color="white")
  img = img.convert("RGBA")  
 
  if os.path.exists(logo):
    icon = Image.open(logo)
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
      icon_w = size_w
    if icon_h > size_h:
      icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
 
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)
  img.save(n)


def analyze_qr(pn):
  reader = zxing.BarCodeReader()
  barcode = reader.decode(pn)
  print(barcode.parsed)



# create_qr("www.bing.com", "test.png")
create_logo_qr("www.bing.com", "test.png", "1.jpg")
analyze_qr('test.png')




