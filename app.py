from flask import Flask, jsonify, make_response, request, abort
import pandas as pd
import catboost
import pickle
from flask_cors import CORS,cross_origin
model = pickle.load(open( "model.pkl", "rb"))
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def hello():
  return "Hello World!"

@app.route("/get_prediction", methods=['GET','POST','OPTIONS'])
@cross_origin()
def get_prediction():
    if not request.json:
        abort(400)
    df = pd.DataFrame(request.json, index=[0])
    cols=["CONSOLE","RATING","CRITICS_POINTS","CATEGORY","YEAR","PUBLISHER","USER_POINTS"]
    df = df[cols]
    return jsonify({'result': model.predict(df)[0]}), 201



if __name__ == "__main__":
  app.run(debug=True)