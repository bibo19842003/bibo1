import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont
# import numpy as np
from hyperlpr import *

# 调用摄像头摄像头
cap = cv2.VideoCapture(0)

framex = cap.get(3)
framey = cap.get(4)

#font = cv2.FONT_HERSHEY_SIMPLEX
font = ImageFont.truetype('jdjls.ttf', 40)

while(True):
    # 获取摄像头拍摄到的画面
    ret, frame = cap.read()
    img = frame

    img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    carinfors = HyperLPR_plate_recognition(img)
    for carinfor in carinfors:
        carnum = carinfor[0]
        caraccuracy = carinfor[1]
        rect = carinfor[2]
        img = cv2.rectangle(img,(rect[0], rect[1]),(rect[2], rect[3]),(255,0,0),2)
#        cv2.putText(img, carnum, (rect[0], rect[1]), font, 0.7,(255,255,255),2,cv2.LINE_AA)
        img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # 文字颜色
        fillColor = (255,0,0)
    # 文字输出位置
        position = (rect[0], rect[3])
    # 输出内容
        strc = carnum
    # 需要先把输出的中文字符转换成Unicode编码形式
        if not isinstance(strc, str):
            strc = strc.decode('utf8')
 
        draw = ImageDraw.Draw(img_PIL)
        draw.text(position, strc, font=font, fill=fillColor)

        img = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR)



    cv2.imshow('frame2',img)
    # 每5毫秒监听一次键盘动作
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# 最后，关闭所有窗口
cap.release()
cv2.destroyAllWindows()



