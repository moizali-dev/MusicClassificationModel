import sys
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

print(os.getcwd())
sys.path.append("../")

import pandas as pd

from utils.spotifyclient import SpotifyClient

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import jsonify

import warnings
warnings.filterwarnings("ignore")

with open("model_v1", 'rb') as f_in:
    dv, mdl = pickle.load(f_in)  

Target_Mapping = {'Hip-Hop':0, 'Pop':1, 'Country':2, 'Rock':3, 'R&B':4, 'Dance/Electronic':5,
       'Indie':6, 'Sleep':7, 'Jazz':8, 'Soul':9}

app = Flask('music_classification')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()

sc = SpotifyClient(os.environ["SPOTIFY_TOKEN"],os.environ["SPOTIFY_USER"])
print(sc)

@app.route('/', methods=['GET'] )
def index():

    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():

    track_content = request.form['trackid']

    print(track_content)
    new_track = Todo(content=track_content)

    db.session.add(new_track)
    db.session.commit()

    # get the track features
    print(os.environ["SPOTIFY_TOKEN"])

    # loop until features are found and timeout is over
    features = ''
    while len(features) < 2:
        features = sc.get_track_features(str(track_content))
    
    print(features)
    print(len(features))
    keys_contains = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness",
    "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    
    features_new = {}
    for k,v in features.items():
        if k in keys_contains:
            features_new[k] = v

    print(features_new)

    # Predict track features
    X = pd.json_normalize(features_new)
    # y_pred = mdl.predict_proba(X)[0,1]
    y_pred = mdl.predict(X)
    y_pred_proba = mdl.predict_proba(X)
    
    prediction_category = list(Target_Mapping.keys())[list(Target_Mapping.values()).index(y_pred)]
    
    AllTrack = Todo.query.all()

    return render_template('index.html', prediction=prediction_category)        
    
    # return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)