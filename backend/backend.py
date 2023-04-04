from flask import Flask, request, jsonify
from open_ai_classifier import open_ai_classifier
from tensorflow_classifier import tensorflow_classifier
from tensorflow_classifier import tensorflow_test_model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Use /classify-1, /classify-2 or /classify-3 to get an answer from the prototype"

@app.route("/classify-1", methods=['GET', 'POST'])
def tensorflow():
    msg = request.get_json()['message'] #This receives JSON format
    print(msg)
    if msg is not None:
        #prob_margin is hard coded for now
        knowledge = tensorflow_test_model(msg, 0.2)
        percent = knowledge["classification_probability"] * 100
        list = knowledge["probabilities"]
        probs = ""
        for i in list:
            probs +=str(i)
        print(probs)
        data =  {
            "verdict": knowledge["verdict"],
            "class": knowledge["class"],
            "classification_probability": str(round(percent, 2)),
            "probabilities": probs
        }
        return jsonify(data)
    else:
        return "No message provided"

@app.route("/classify-2", methods=['GET', 'POST'])
def combo():
    msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        #prob_margin is hard coded for now
        knowledge = tensorflow_test_model(msg, 0.2)
        percent = knowledge["classification_probability"] * 100
        list = knowledge["probabilities"]
        if(percent>60):
            probs = ""
            for i in list:
                probs +=str(i)
            print(probs)
            data =  {
                "verdict": knowledge["verdict"],
                "class": knowledge["class"],
                "classification_probability": str(round(percent, 2)),
                "probabilities": probs
            }
        else:
            data = {
            "verdict": "-",
            "class": open_ai_classifier(msg),
            "classification_probability": "-",
            "probabilities": "-"
        }
        return jsonify(data)
    else:
        return "No message provided"

@app.route("/classify-3", methods=['GET', 'POST'])
def openai():
    msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        data = {
            "verdict": "-",
            "class": open_ai_classifier(msg),
            "classification_probability": "-",
            "probabilities": "-"
        }
        return jsonify(data)
    else:
        return "No message provided"

if __name__ == "__main__":
    app.run(debug=True)