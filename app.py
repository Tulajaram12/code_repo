from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return 'How are you, Rapyder!'

@app.route('/webapp/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        user_data = request.form['data']
        return f'Data received: {user_data}'
    return 'Submit data via POST request.'

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # REQUIRED for Docker / Kubernetes / ALB
        port=5000,       # Must match containerPort
        debug=True
    )

