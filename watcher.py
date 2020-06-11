import time
import requests
import os
import urllib.request
from bs4 import BeautifulSoup
#import ffmpeg
import shutil
from pathlib import Path
import numpy as np
import math
import imageio
from datetime import datetime
from PIL import Image
from pytz import timezone
import io
from time import perf_counter
import pytz
import colorsys

# observatory at Calar Alto
vidurl = "http://150.214.222.103/mjpg/video.mjpg"
# London
#vidurl = "http://167.98.130.231:8080/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"

res = 2000
C = int(math.pi*res)

def step (r,g,b, repetitions=1):
    lum = math.sqrt( .241 * r + .691 * g + .068 * b )
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)
    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum
    return (h2, lum, v2)

def dimensions():
    r = requests.get(vidurl, stream=True)
    if(r.status_code == 200):
        try:

            bytes=b''
            for chunk in r.iter_content(chunk_size=1024):
                bytes += chunk
                finda = bytes.find(b'\xff\xd8')
                findb = bytes.find(b'\xff\xd9')
                if finda != -1 and findb != -1:
                    jpg = bytes[finda:findb+2]
                    bytes = bytes[findb+2:]
                    image = Image.open(io.BytesIO(jpg))
                    left = 0
                    top = 25
                    right = image.size[0]
                    bottom = image.size[1]
                    image = image.crop((left, top, right, bottom))
                    w, h = image.size
                    print(image.size)
                    height = int(math.sqrt((res*h)/(w)))
                    width = int(math.sqrt((res*w)/(h)))
                    dim = (width, height)
                    return dim
        except:
            print("error")

def colorSort(img, self):

    progress = update(self)
    if progress < 1:
        return

    imd = img.resize(self.dim, resample=0)
    im = np.array(imd)
    np.shape(im)
    im = im.reshape((self.dim[0]*self.dim[1],3))
    imList = im.tolist()
    imList.sort(key=lambda rgb: step(*rgb,8) )
    imsort = np.array(imList)
    imsorted = np.expand_dims(imsort, axis=0).astype(np.uint8)
    imsorted = np.tile(imsorted,(progress,1,1))

    abs_file_path = self.path + "/" + self.day + ".png"

    if not os.path.isfile(abs_file_path):
        file = abs_file_path
        imageio.imwrite(file, imsorted)
    else:
    # elseif np.shape(data)[0] > 500
    # else: keep on adding to whatever abs_file_path
        data = imageio.imread(abs_file_path)
        print(np.shape(data)[0])
        if np.shape(data)[0] > 100:
            print("this")
            length = str(len([name for name in os.listdir(self.path) if self.day in name]))
            file = self.path + '/' + self.day + '_' + length + ".png"
            imageio.imwrite(file, data)
            imageio.imwrite(abs_file_path, imsorted)
        else:
            data = np.vstack((imsorted, data))
            imageio.imwrite(abs_file_path, data)
        print(np.shape(data)[0], end='\r')
#         command = "convert " + day + ".png" + " -flip -rotate 90 -virtual-pixel Black -background Black +distort Polar '" + str(res/2) + ",0 0,0 180,-180' +repage  " + "segment" + day + ".png && convert segment" + day + ".png -transparent black polar" + day + ".png"
#         subprocess.call(command, shell=True)

    date = None
    imsort = None
    imList = None
    im = None
    imsorted = None

def paint(self):
#     abs_file_path = filename()
    r = requests.get(vidurl, stream=True)
    if(r.status_code == 200):
        while True:
            try:
                bytes=b''
                for chunk in r.iter_content(chunk_size=1024):
                    bytes += chunk
                    finda = bytes.find(b'\xff\xd8')
                    findb = bytes.find(b'\xff\xd9')
                    if finda != -1 and findb != -1:
                        jpg = bytes[finda:findb+2]
                        bytes = bytes[findb+2:]
                        image = Image.open(io.BytesIO(jpg))
                        left = 0
                        top = 25
                        right = image.size[0]
                        bottom = image.size[1]
                        image = image.crop((left, top, right, bottom))
                        colorSort(image, self)
                    # need to set this to a better value
                        time.sleep(1)
                        if uktz.localize(datetime.now()) > self.end:
                            return
            except:
                print("error")

def folder():
    now = datetime.now()
    if now.hour < 12:
        sun = "dawn"
    else:
        sun = "dusk"
    day = str(now.year) + str(now.month) + str(now.day)
    path = Path.cwd()
    rel_path = day + sun
    abs_folder_path = str(path) + '/' + rel_path
    os.mkdir(abs_folder_path)
    return abs_folder_path, day

# returns the number of rows to fill
def update(self):
    now = uktz.localize(datetime.now())
    start = self.start
    end = self.end
    delta = (now - start).seconds / (end - start).seconds
    progress = int(delta*self.layers)
    toFill = progress - self.fill
    self.fill = progress
    return toFill

uktz=pytz.timezone('Europe/London')
estz=pytz.timezone('Europe/Madrid')

sunset = datetime(2020, 6, 11, 20, 51, 0)
night = datetime(2020, 6, 11, 23, 19, 0)

sunrise = datetime(2020, 6, 12, 4, 58, 0)
morning = datetime(2020, 6, 12, 7, 27, 0)
# sunrise = datetime.datetime(2020, 6, 7, 4, 59, 0)
# morning = datetime.datetime(2020, 6, 7, 7, 29, 0)
# y = datetime.datetime.now()

sunset = estz.localize(sunset)
night = estz.localize(night)
# sunrise = estz.localize(sunrise)
# morning = estz.localize(morning)

sunrise = estz.localize(sunrise)
morning = estz.localize(morning)
# sunrise = uktz.localize(sunrise)
# morning = uktz.localize(morning)

#dates = [[sunrise, morning], [sunset, night]]
dates = [[sunset, night],[sunrise, morning]]

class picture:
    # class attributes
    layers = C
    # instance attributes
    def __init__(self, path, day, fill, start, end, dim):
        self.start = start
        self.end = end
        self.path = path
        self.day = day
        self.fill = fill
        self.dim = dim

while True:
    print("go")
    if uktz.localize(datetime.now()) > dates[1][1]:
        break
    for date in dates:
        if date[0] < uktz.localize(datetime.now()) < date[1]:
            path, day = folder()
            dim = dimensions()
            pic = picture(path, day, 0, date[0], date[1], dim)
            paint(pic)
            # sometimes this is erroring and going back to beginning
    print("wait")
    time.sleep(15)
