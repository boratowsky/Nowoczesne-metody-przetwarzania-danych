import json
from os import getenv
from redis import Redis
from flask import Flask, flash, redirect, render_template, url_for

r = Redis(host='redis-stack', port=6379, decode_responses=True)

def start():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = getenv('FLASK_SECRET_KEY')

    @app.route("/")
    def index():
        keys = ["id", "name", "type", "miasto", "vote"]
        schools = [
            {keys[i]: v for i, v in enumerate(r.hmget(school, keys=keys))}
            for school in r.scan_iter(_type="HASH")
        ]
        return render_template('index.html', schools=schools)

    @app.route("/vote/<id>")
    def vote(id):
        r.hincrby(id, "vote")
        name = r.hmget(id, keys=["name"])[0]
        flash(f"Pomyślnie zarejestrowano głos na \"{name}\"!")
        return redirect(url_for('index'))

    return app