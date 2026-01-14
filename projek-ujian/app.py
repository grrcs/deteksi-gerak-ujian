# app.py (Di Raspberry Pi)
from flask import Flask, Response, jsonify
from flask_cors import CORS
from camera_ai import ProctorAI

app = Flask(__name__)
CORS(app) 

proctor = ProctorAI()
current_status = "Inisialisasi..."

def gen_frames():
    global current_status
    while True:
        frame, status = proctor.get_frame()
        current_status = status
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_status')
def get_status():
    return jsonify({'status': current_status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)