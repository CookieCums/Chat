from flask import Flask, request, jsonify, render_template, send_from_directory
import time
import os

app = Flask(__name__, template_folder='templates')
MSG_FILE = 'messages.dat'
MAX_MSGS = 100

def get_messages(since=0):
    if not os.path.exists(MSG_FILE):
        return []
    with open(MSG_FILE, 'r') as f:
        lines = f.read().splitlines()
    messages = [line.split('|', 2) for line in lines]
    return messages[since:]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_msg():
    msg = f"{time.time()}|{request.data.decode()}\n"
    with open(MSG_FILE, 'a') as f:
        f.write(msg)
    if os.path.getsize(MSG_FILE) > 1024 * 10:
        with open(MSG_FILE, 'r') as f:
            lines = f.read().splitlines()[MAX_MSGS // 2:]
        with open(MSG_FILE, 'w') as f:
            f.write('\n'.join(lines) + "\n")
    return 'OK'

@app.route('/updates')
def get_updates():
    since = int(request.args.get('since', 0))
    start_time = time.time()
    timeout = 30
    while True:
        msgs = get_messages(since)
        if msgs:
            return jsonify(msgs)
        if time.time() - start_time > timeout:
            return jsonify([])
        time.sleep(0.5)

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(threaded=True, debug=False, host='0.0.0.0', port=5000)
