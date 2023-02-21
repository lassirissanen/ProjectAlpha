'''
Start an application with a command python backend.py
The application can be tested with a browser 
localhost:5000/api?message=joo
localhost:5000/api?message=ei
localhost:5000/api?message=vaihda
localhost:5000/api?message=something else
Route '/confused' will be deleted from the final version
'''
from flask import Flask, request, redirect, url_for
app = Flask(__name__)

@app.before_request
def check_url_and_redirect():
    if request.path[1:] == 'api':
        if request.args.get('message') == "joo":
            return redirect(url_for('joo'))
        elif request.args.get('message') == "ei":
            return redirect(url_for('ei'))
        elif request.args.get('message') == "vaihda":
            return redirect(url_for('vaihda'))
        else:
            return redirect(url_for('confused'))
            
@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/joo")
def joo():
    return "aika varattu"
    
@app.route("/ei")
def ei():
    return "ei sitte"

@app.route("/vaihda")
def vaihda():
    return "Mikäs aika sopis?"

@app.route("/confused")
def confused():
    return "Nyt en ymmärtäny"
    
if __name__ == "__main__":
    app.run(debug=True)