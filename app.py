from flask import Flask, render_template, Response, send_from_directory, send_file
from camera import Camera
import time,threading

app = Flask(__name__)
SLEEP_TIME_LONG = 0.1


@app.route('/')
def index():
    return render_template('index.html')




def gen(camera, f):
    threading.Thread
    while True:
        if f != 0:
            temp=(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1 / f)
        frame = camera.get_frame()
        time.sleep(SLEEP_TIME_LONG)
        # print('*************')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/f/<int:f>')
def video_f(f):
    return Response(gen(Camera(), f),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    # t = threading.Thread(target=gen(), name='LoopThread')
    return Response(gen(Camera(),0),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/v/<filename>')
def get_file(filename):
    return send_file("./static/" + filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
