from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import csv
import pandas as pd  
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from threading import Thread

# 获取当前文件的绝对路径，并设置 Flask 静态文件夹的路径
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=os.path.join(basedir, 'static'))

def chooseI(directory, frame):
    matched_files = []
    for j in range(1, 7):
        path_len = os.path.join(directory, str(j))
        photo_name = f'len{j}_screenshot_{frame:04d}.jpg'
        file_path = os.path.join(path_len, photo_name)
        if os.path.isfile(file_path):
            relative_path = os.path.relpath(file_path, start=basedir).replace('\\', '/')
            matched_files.append(relative_path)
        else:
            print('Fail to find the path.')
    return matched_files, frame + 1

def run_flask():
    app.run(port=5000)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://localhost:5000/"))
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        
        self.setLayout(layout)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Flask + PyQt')
        self.show()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    directory = request.form['directory']
    ab_directory = os.path.abspath(directory)
    global dict_file, max_files, index_frame
    dict_file = directory
    if max_files == 0:
        for root, dirs, files in os.walk(ab_directory):
            file_count = len(files)
            if file_count > max_files:
                max_files = file_count
    if os.path.exists(ab_directory) and os.path.isdir(ab_directory):
        images, index_frame = chooseI(ab_directory, index_frame)
        return render_template('gallery.html', images=images, directory=directory)
    else:
        return "文件夹不存在，请输入正确的路径。", 400

@app.route('/next_image', methods=['POST'])
def next_image():
    image_name = request.form.get('image_name')
    if not image_name:
        return jsonify({'error': 'Missing image name'}), 400
    write_image_to_csv(image_name)
    global dict_file, index_frame
    ab_directory = os.path.abspath(dict_file)
    next_image_path, index_frame = chooseI(ab_directory, index_frame)
    if next_image_path:
        return jsonify(images=next_image_path, image_group_index=index_frame - 1)
    else:
        return jsonify(image=None)

@app.route('/<path:filename>')
def send_image(filename):
    print('Serving file:', filename)
    try:
        return send_from_directory(app.static_folder, filename)
    except Exception as e:
        print('Failed to serve file:', e)
        return "文件未找到", 404

@app.route('/image_click', methods=['POST'])
def image_click():
    image_name = request.form['image_name']
    return jsonify({"message": f"点击的图片: {image_name}"})

def write_image_to_csv(filename):
    label, frame, name = extract_info_from_filename(filename)
    if label is not None and frame is not None and name is not None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'label.csv')
        with open(csv_file_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([frame, label, name])
        write_frame_to_log(frame + 1)

def extract_info_from_filename(filename):
    basename = os.path.basename(filename)
    parts = basename.split('_')
    if len(parts) >= 3 and parts[0].startswith('len'):
        label = parts[0][3:]
        frame = int(parts[-1].split('.')[0])
        return label, frame, basename
    return None, None, None

def write_frame_to_log(index_frame):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'log.csv')
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([index_frame])

def csv_init():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, 'log.csv')
    label_file_path = os.path.join(script_dir, 'label.csv')
    for path in [log_file_path, label_file_path]:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['0'] if path == log_file_path else ['frame', 'label', 'name'])

if __name__ == '__main__':
    dict_file = ''
    max_files = 0
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, 'log.csv')
    index_frame = 0
    if os.path.isfile(csv_file_path):
        df = pd.read_csv(csv_file_path, header=None)
        index_frame = int(df.iloc[0, 0])
    csv_init()
    thread = Thread(target=run_flask)
    thread.start()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
