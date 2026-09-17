from flask import Flask

app = Flask(__name__)

# Charge la configuration depuis fbapp/config.py
app.config.from_object('fbapp.config')

from . import models

@app.cli.command("init-db")
def init_db():
    models.init_db()
    print("Base de données initialisée !")

from . import views