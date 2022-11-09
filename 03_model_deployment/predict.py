import pickle
import os

from flask import Flask
from flask import request
from flask import jsonify

import warnings
warnings.filterwarnings("ignore")


with open("model_v1", 'rb') as f_in:
    dv, rf = pickle.load(f_in)  

app = Flask('music_classification')
@app.route('/predict', methods=['POST'] )
def predict():
    music = request.get_json()
    print(music)
    X = dv.fit_transform([music])
    y_pred = rf.predict_proba(X)[0,1]
    rock_music = y_pred >= 0.5

    result = {
        "prediction_probability": float(y_pred),
        "rock music": bool(rock_music)
    }
    
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=9698)

# Port for cloud run
# port=int(os.environ.get("PORT", 8080))
# port=9698