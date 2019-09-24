import os
import json
from flask import Flask, render_template

app = Flask(__name__, root_path=os.path.dirname(os.path.abspath(__file__)), static_folder='static')


@app.route('/')
def index():
    recommendations = []
    recs_folder = os.path.join(os.path.dirname(app.root_path), 'Your Recommendations')
    for rec_folder in os.listdir(recs_folder):
        if not os.path.isdir(os.path.join(recs_folder, rec_folder)):
            continue
        with open(os.path.join(recs_folder, rec_folder, 'data.json'), 'r') as data_fd:
            rec = json.load(data_fd)
        recommendations.append(rec)
    return render_template('index.html', recommendations=recommendations)
