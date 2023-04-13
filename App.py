 # coding=utf8
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys,os
import threading
from engineio.async_drivers import gevent
import datetime
import shutil,webview
from engineio.payload import Payload
import win32gui, win32con

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)


# ระบุ path ของโฟลเดอร์ templates ภายใน Flask application
template_folder = os.path.abspath('templates')
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')

app = Flask(__name__)
app.config['SECRET_KEY'] = "dev2077"
app = Flask(__name__, static_url_path=r'/static')
app = Flask(__name__, template_folder=template_folder)
socketio = SocketIO(app)

msg = ''

def Remove_Temp(days, path):
    global msg
    # กำหนด path ของ folder Temp ที่ต้องการลบไฟล์

    folder_path = r''+path

    if os.path.isdir(folder_path):
        pass
        # print(f"The folder '{folder_path}' exists.")

    else:
        # print(f"The folder '{folder_path}' does not exist.")
        msg = f"The folder '{folder_path}' does not exist."
        return 404
    

    # วันที่ปัจจุบัน
    now = datetime.datetime.now()

    # วันที่ที่ต้องการลบไฟล์ออกทั้งหมด
    days_to_keep = 7
    delta_days = datetime.timedelta(days=days_to_keep)
    date_to_keep = now - delta_days

    # วนลูปเพื่อค้นหาและลบไฟล์และโฟลเดอร์ที่ไม่มีการใช้งานเกินจำนวนวันที่กำหนด
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            # ตรวจสอบวันที่ของไฟล์
            file_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            if file_date < date_to_keep:
                print('remove file:', file_path)
                msg = 'remove file:', file_path
                try:
                    os.remove(file_path)
                except:
                    print('Error removing file:', file_path)
                    msg = 'Error removing file:', file_path

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # ตรวจสอบวันที่ของโฟลเดอร์
            dir_date = datetime.datetime.fromtimestamp(os.path.getctime(dir_path))
            if dir_date < date_to_keep:
                print('remove folder:', dir_path)
                msg = 'remove file:', file_path
                try:
                    shutil.rmtree(dir_path)
                except:
                    print('Error removing folder:', dir_path)
                    msg = 'Error removing file:', file_path

    msg = 'เสร็จสิน'

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@socketio.on("Remove_Temp")
def Remove_Temp_api(data):
    days = data['days']
    path = data['path']
    # print(days,path)
    Remove_Temp(days,path)

@socketio.on("data")
def on_data(data):
    emit('my response', msg)

def start_server():
    socketio.run(app, port=80)

if __name__ == '__main__':

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    webview.create_window("Temporary Files ", "http://localhost/")
    webview.start()
    sys.exit()




