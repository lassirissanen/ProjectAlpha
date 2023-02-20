from flask import Flask

app = Flask(__name__)

@app.route('/something/<string:input_message>')

def something(input_message):
    return 'Received message:' + input_message

if __name__ == '__main__':
    app.run(debug=True, port=5000)