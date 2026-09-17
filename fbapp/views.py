from flask import Flask

app = Flask(__name__)

# Charge la configuration depuis config.py
app.config.from_object('fbapp.config')

@app.route('/')
def index():
    return "Hello world !"