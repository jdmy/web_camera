from flask import Flask, render_template, Response, send_from_directory, send_file, g, request
from camera import Camera
import time, threading
from PIL import Image, ImageStat
from types import MethodType

app = Flask(__name__)
SLEEP_TIME_LONG = 0.1

ff = 3


def brightness(im_file):
    # im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im_file)
    mm = stat._getextrema()
    return stat.mean[0]


@app.before_request
def before_request():
    global ff


@app.route('/')
def index():
    return render_template('index.html')


def sleep_s(f):
    global cnt
    while True:
        # with app.app_context():
        #     g.cnt += 1
        cnt += 1
        time.sleep(1 / f)


def gen(camera, f):
    global ff
    global cnt
    cnt = 0
    tmpcnt = 0

    frame = camera.get_frame()
    flag = 1
    last = time.time()
    frame1 = open('test6.jpg', 'rb').read()
    im = Image.open('test1.jpg').convert('L')
    stat = ImageStat.Stat(im)
    mm = stat._getextrema()
    print(mm)
    # print(frame)
    while True:
        f = ff
        a = time.time()
        interval = 0.1
        # print(f)
        if interval > a - last > 0:
            # print(a, last, 111111111111)
            temp = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n'
            yield temp
        elif interval + f > a - last >= interval:
            # print(a, last, 222222222222)
            frame, grey = camera.get_frame()
            ngrey = brightness(grey)

            # print(ngrey)
            ff = (ngrey+10) / 100
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        elif a - last >= interval + f:
            last = time.time()
            # print(a, last, 333333333333)


@app.route('/vid/eo_feed/f/<float:f>')
def video_f(f):
    return Response(gen(Camera(), f),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/process_data")
def process_data():
    global ff
    f = float(request.args.get('f', 10)) / 5
    ff = f
    print(ff)
    return "200 OK"


@app.route('/video_feed')
def video_feed():
    # t = threading.Thread(target=gen(), name='LoopThread')
    return Response(gen(Camera(), 10),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/v/<filename>')
def get_file(filename):
    return send_file("./static/" + filename)


if __name__ == '__main__':
    cnt = 0
    app.run(host='0.0.0.0', threaded=True)
