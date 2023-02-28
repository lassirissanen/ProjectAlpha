from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Use /classify-1/[your message], /classify-2/[your message] or /classify-3/[your message] to get an answer from the prototype "

@app.route("/classify-1/<msg>", methods=['GET', 'POST'])
def tensorflow(msg):
    #result = lassis_genius_bot(message)
    return "from api 1 (tensorflow) with " + msg

@app.route("/classify-2/<msg>", methods=['GET', 'POST'])
def combo(msg):
    if(len(msg)<20):
        #result = lassis_genius_bot(msg)
        return "from api 2 (tensorflow) with " + msg
    
    #result = ermyas_genius_bot(msg)
    return "from api 2 (open ai) with " + msg

@app.route("/classify-3/<msg>", methods=['GET', 'POST'])
def openai(msg):
    #result = ermyas_genius_bot(msg)
    return "from api 3 (openai) with " + msg


if __name__ == "__main__":
    app.run(debug=True)