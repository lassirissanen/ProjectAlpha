from flask import Flask, request, redirect, url_for
app = Flask(__name__)
#the api takes you direclty to the tensorflow or open ai solution if you wish,
#or decides itself based on the length of the message
#http://localhost:5000/api?message=<random marks> takes you to one, based on the amount of marks
#we added two endpoints for openai and tensorflow as well, to follow the diagram, but they dont account the
#message yet
#http://localhost:5000/api?message=tensor takes you to the tensorlow solution
#http://localhost:5000/api?message=openai takes you to the openai solution

@app.before_request
def check_url_and_redirect():
    if request.path[1:] == 'api':
        if request.args.get('message') == "tensor":
            return redirect(url_for('tensorflow'))
        elif request.args.get('message') == "openai":
            return redirect(url_for('openai'))
#if the message has over 20 marks, it goes to openai
        if(len(request.args.get('message'))<20):
            return redirect(url_for('tensorflow'))
        else:
            return redirect(url_for('openai'))


@app.route("/")
def hello():
    return "please input a message!"

@app.route("/tensorflow")
def tensorflow():
    return "tensori"

@app.route("/openai")
def openai():
    return "ouppeni"


if __name__ == "__main__":
    app.run(debug=True)