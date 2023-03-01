from flask import Flask, request
from open_ai_classifier import open_ai_classifier

app = Flask(__name__)

@app.route("/")
def hello():
    return "Use /classify-1, /classify-2 or /classify-3 to get an answer from the prototype"

@app.route("/classify-1", methods=['GET', 'POST'])
def tensorflow():
    msg = request.form.get('message') #This receives texts
    #msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        #result = lassis_genius_bot(message)
        return "from API 1 (tensorflow) with a message: " + msg 
    else:
        return "No message provided"

@app.route("/classify-2", methods=['GET', 'POST'])
def combo():
    msg = request.form.get('message') #This receives texts
    #msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        if (len(msg) < 20):
            #result = lassis_genius_bot(msg)
            return "from API 2 (tensorflow) with a message: " + msg
        #result = ermyas_genius_bot(msg)
        return "from API 2 (openAI) with a message: " + msg
    else:
        return "No message provided"

@app.route("/classify-3", methods=['GET', 'POST'])
def openai():
    msg = request.form.get('message') #This receives texts
    #msg = request.get_json()['message'] #This receives JSON format
    if msg is not None:
        #result = ermyas_genius_bot(msg)
        return open_ai_classifier(msg)
    else:
        return "No message provided"

if __name__ == "__main__":
    app.run(debug=True)