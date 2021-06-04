import os
import re
import cv2
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import cloudinary.uploader
import urllib.request
import numpy as np


filename = "arapova.jpg"



global imgs
imgs = []

hi = 0
wi = 0
bb = 0
cloudinary.config(
  cloud_name = 'dnevycmvy',  
  api_key = '561873719248581',  
  api_secret = '6WprD1-g9yjnZON65Eh9sqTz7so'  
)

def mouse_press(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        os.startfile(imgs[param])
        print(imgs[param])

arap = cloudinary.uploader.upload(filename)['secure_url']
#arap = "https://res.cloudinary.com/dnevycmvy/image/upload/v1622811323/fdq08sd5sord9qxdxrgz.jpg" #del
url = r'https://yandex.ru/images/search?source=collections&rpt=imageview&url={}'.format(arap)

soup = BeautifulSoup(requests.get(url).text, 'lxml')
similar = soup.find_all('li', class_='cbir-similar__thumb')

for i in similar:
    out = f"https://yandex.ru{i.find('a').get('href')}\n"
    imgs.append(unquote(out))


for a in range(0, len(imgs)):

    r = re.search(r'(?<=&img_url\=).*?(?=&rpt\=)', imgs[a])[0]
    try:
        req = urllib.request.urlopen(r)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    except Exception as e:
        print(e)
    n = cv2.imdecode(arr, -1)
    gray = cv2.cvtColor(n, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('dev/haarcascade_frontalface_alt2.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        try:
            faces = n[y:y + h + 90, x:x + w + 90]
        except Exception as e:
            print(str(e))
                
                
    cv2.namedWindow(str(a), cv2.WINDOW_NORMAL)
    cv2.resizeWindow(str(a), 300,300)
    cv2.setMouseCallback(str(a), mouse_press, a)
    try:
        
        if (bb+1) % 11 != 0:
            cv2.moveWindow(str(a), hi + (300 * bb),wi)
            cv2.imshow(str(a), faces)
            bb = bb + 1
        else:
            wi = wi + 330
            cv2.moveWindow(str(a), hi + (300 * 0),wi)
            cv2.imshow(str(a), faces)
            bb = 1
    except Exception as e:
        if (bb+1) % 11 != 0:
            cv2.moveWindow(str(a), hi + (300 * bb),wi)
            bb = bb + 1
        else:
            cv2.moveWindow(str(a), hi + (300 * 0),wi)
            bb = 1


while(1):
    key = cv2.waitKey(20) & 0xFF
    if key == ord('\r'):
        print("enter")
    elif key == 32:
        print("space")
    elif key == ord('\t'):
        print("tab")
    elif key == 27:
        break
