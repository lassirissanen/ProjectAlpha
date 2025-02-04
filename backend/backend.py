from flask import Flask, request, jsonify
from flasgger import Swagger
from open_ai_classifier import open_ai_classifier
from open_ai_classifier import deduce_time
from tensorflow_classifier import tensorflow_classifier
from tensorflow_classifier import tensorflow_test_model 
from flask_cors import CORS # Handles Cross-Origin Resource Sharing (CORS) errors

# Initializing Flask app
app = Flask(__name__)
# Using CORS to handle cross-origin resource sharing errors
CORS(app)

# Creating Swagger object and linking it to the Flask app, using YAML file to specify API documentation
swagger = Swagger(app, template_file="./documentation/api-doc.yaml")

# Default route
@app.route("/")
def hello():
    return "Use /classify-1, /classify-2 or /classify-3 to get an answer from the prototype"

# Endpoint for using TensorFlow classifier
@app.route("/classify-1", methods=['POST'])
def tensorflow():
    body = request.get_json()
    msg = body['message']
    original_suggestion = body['suggestion']
    if msg is not None:
        # Running TensorFlow test model on message with a hard-coded probability margin of 0.2
        knowledge = tensorflow_test_model(msg, 0.2)
        percent = knowledge["classification_probability"] * 100
        list = knowledge["probabilities"]
        
        # Joining the probabilities together to make it a string
        probs = ""
        for i in list:
            probs +=str(i)
        print(probs)

        # Creating a dictionary containing the classification results and returning it as a JSON object
        data =  {
            "verdict": knowledge["verdict"],
            "class": knowledge["class"],
            "classification_probability": str(round(percent, 2)),
            "probabilities": probs
        }
        # deduce time if classification is suggestion
        if data['class'] == 'suggestion':
            time = deduce_time(msg, original_suggestion)
            data['time'] = time
            
        return jsonify(data)
    else:
        return "No message provided"

# Endpoint for using a combination of TensorFlow and OpenAI classifiers
@app.route("/classify-2", methods=['GET', 'POST'])
def combo():
    body = request.get_json()
    msg = body['message']
    original_suggestion = body['suggestion']
    if msg is not None:
        # Running TensorFlow test model on message with a hard-coded probability margin of 0.2
        knowledge = tensorflow_test_model(msg, 0.2)
        percent = knowledge["classification_probability"] * 100
        list = knowledge["probabilities"]

        # If the probability of classification by the TensorFlow model is greater than 60%, return its classification results,
        # otherwise run the message through the OpenAI classifier
        if (percent > 60):
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
            "class": open_ai_classifier(msg, original_suggestion),
            "classification_probability": "-",
            "probabilities": "-"
        }

        # deduce time if classification is suggestion
        if data['class'] == 'suggestion':
            time = deduce_time(msg, original_suggestion)
            data['time'] = time

        return jsonify(data)
    else:
        return "No message provided"

# Endpoint for using OpenAI classifier
@app.route("/classify-3", methods=['GET', 'POST'])
def openai():
    body = request.get_json()
    msg = body['message']
    original_suggestion = body['suggestion']

    if msg is not None:
        # Creating a dictionary containing the classification results and returning it as a JSON object
        data = {
            "verdict": "-",
            "class": open_ai_classifier(msg, original_suggestion),
            "classification_probability": "-",
            "probabilities": "-"
        }

        # deduce time if classification is suggestion
        if data['class'] == 'suggestion':
            time = deduce_time(msg, original_suggestion)
            data['time'] = time

        return jsonify(data)
    else:
        return "No message provided"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")