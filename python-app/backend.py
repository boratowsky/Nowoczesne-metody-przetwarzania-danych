import json
from os import getenv
from redis import Redis
from flask import Flask

r = Redis(host='redis-stack', port=6379, decode_responses=True)

def load_data():
    with open('uczelnie.json') as f:
        uczelnie = json.loads(f.read())
        print(uczelnie)
        for u in uczelnie["uczelnie"]:
            r.hset(u["id"], mapping=u)

def start():
    app = Flask(__name__)
    app.secret_key = getenv('FLASK_SECRET_KEY')

    @app.route("/")
    def index():
        return '{"ok":1}'

    load_data()
    return app