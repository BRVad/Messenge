from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)
db = []


@app.route("/")
def hello():
    return "Hello, World! 123 <a href='/status'>Статус</a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Messenger',
        'time': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        'messeges_count': len(db),
        'users_count': len(set(message['name'] for message in db))
    }


@app.route("/send", methods=['POST'])
def send():
    data = request.json

    db.append({
        'id': len(db),
        'name': data['name'],
        'text': data['text'],
        'timestamp': time.time()
    })

    return {'ok': True}


@app.route("/messages")
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_id'])
    else:
        after_timestamp = 0

    limit = 100

    after_id = 0
    for message in db:
        if message['timestamp'] > after_timestamp:
            break
        after_id += 1

    return {'messages': db[after_id:after_id + limit]}


app.run()
