from flask import Flask, request, jsonify
from open_ai_classifier import open_ai_classifier
from tensorflow_classifier import tensorflow_classifier
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Use /classify-1, /classify-2 or /classify-3 to get an answer from the prototype"

@app.route("/classify-1", methods=['GET', 'POST'])
def tensorflow():
    #msg = request.form.get('message') #This receives texts
    msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        data =  {
            "classification": tensorflow_classifier(msg)
        }
        return jsonify(data)
    else:
        return "No message provided"

@app.route("/classify-2", methods=['GET', 'POST'])
def combo():
    #msg = request.form.get('message') #This receives texts
    msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        res = tensorflow_classifier(msg)
        if res != "unknown":
            #result = lassis_genius_bot(msg)
            data = {
                "classification": res
            }
            return jsonify(data)
        data = {
                "classification": open_ai_classifier(msg)
            }
        return jsonify(data)
    else:
        return "No message provided"

@app.route("/classify-3", methods=['GET', 'POST'])
def openai():
    #msg = request.form.get('message') #This receives texts
    msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        #result = ermyas_genius_bot(msg)
        data = {
            "classification": open_ai_classifier(msg)
        }
        return jsonify(data)
    else:
        return "No message provided"

if __name__ == "__main__":
    app.run(debug=True)