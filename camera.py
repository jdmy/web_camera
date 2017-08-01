# camera.py

from VideoCapture import Device
from PIL import Image
from win32api import GetSystemMetrics
import time
import sys, pygame

# pygame.init()

# size = width, height = 620, 485
# speed = [2, 2]
# black = 0, 0, 0

# pygame.display.set_caption('视频窗口@dyx1024')
# screen = pygame.display.set_mode(size)

# 抓取频率，抓取一次
SLEEP_TIME_LONG = 0.1


# 初始化摄像头





class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    cam = Device(devnum=0, showVideoWindow=0)

    def __init__(self):
        # self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

        pass

    def get_frame(self):
        width = GetSystemMetrics(0)
        nwidth = int(width * 0.9)
        height = GetSystemMetrics(1)
        nheight = int(height * 0.9)
        mi=min(width,height)
        self.cam.saveSnapshot('test_raw.jpg', timestamp=3, boldfont=1, quality=75)
        im = Image.open("test_raw.jpg")
        out = im.resize((mi, mi))
        out.save("test.jpg")
        a = open('test.jpg', 'rb').read()
        b = Image.open('test.jpg', 'r').convert('L')
        return a, b

        # while True:
        #     # 抓图
        #     cam.saveSnapshot('test.jpg', timestamp=3, boldfont=1, quality=75)
        #
        #     # 加载图像
        #     image = pygame.image.load('test.jpg')
        #
        #     # 传送画面
        #     screen.blit(image, speed)
        #
        #     # 显示图像
        #     pygame.display.flip()
        #     # 休眠一下，等待一分钟
        #     time.sleep(SLEEP_TIME_LONG)
