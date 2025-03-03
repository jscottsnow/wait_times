from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit # type: ignore
import json
import os

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'  
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'wait_times.json')


def load_wait_times():
    with open(JSON_FILE) as f:
        return json.load(f)

def save_wait_times(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f)

wait_times = load_wait_times()

@app.route("/injuries", methods=["GET", "POST"])
def injuries():
    return render_template("injuries.html", injuries_wait_time=wait_times["injuries"])

@app.route("/injury-rechecks", methods=["GET", "POST"])
def injury_rechecks():
    return render_template("injury_rechecks.html", injury_rechecks_wait_time=wait_times["injury_rechecks"])

@app.route("/physicals", methods=["GET", "POST"])
def physicals():
    return render_template("physicals.html", physicals_wait_time=wait_times["physicals"])

@app.route("/drug-screens", methods=["GET", "POST"])
def drug_screens():
    return render_template("drug_screens.html", drug_screens_wait_time=wait_times["drug_screens"])

@app.route("/urgent-care", methods=["GET", "POST"])
def urgent_care():
    return render_template("urgent_care.html", urgent_care_wait_time=wait_times["urgent_care"])


@app.route("/update_wait_time/<category>", methods=["POST"])
def update_wait_time(category):
    wait_times[category] = request.form[f"{category}_wait_time"]
    save_wait_times(wait_times)
    socketio.emit('updated_wait_times', wait_times)
    return redirect(url_for(category))

@app.route("/wait_times_data")
def wait_times_data():
    return jsonify(load_wait_times())  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wait_times")
def display_wait_times():
    return render_template("wait_times.html", wait_times=load_wait_times())

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0") 