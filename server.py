from flask import Flask, request, jsonify, render_template
import time
import os

app = Flask(__name__)
MSG_FILE = 'messages.dat'
MAX_MSGS = 100

def get_messages(since=0):
    if not os.path.exists(MSG_FILE):
        return []
    with open(MSG_FILE, 'r') as f:
        lines = f.read().splitlines()
    # Split each line into [timestamp, user, message]
    messages = [line.split('|', 2) for line in lines]
    return messages[since:]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_msg():
    # Create a message string with the timestamp and the posted data
    msg = f"{time.time()}|{request.data.decode()}\n"
    with open(MSG_FILE, 'a') as f:
        f.write(msg)
    # Rotate messages if file exceeds 10KB to keep it small
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
    timeout = 30  # seconds
    # Wait until new messages appear or until timeout is reached.
    while True:
        msgs = get_messages(since)
        if msgs:
            return jsonify(msgs)
        if time.time() - start_time > timeout:
            return jsonify([])  # return an empty list after timeout
        time.sleep(0.5)  # sleep briefly to reduce CPU load

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=10000)
