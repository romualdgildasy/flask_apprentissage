from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Charge la configuration depuis fbapp/config.py
app.config.from_object('fbapp.config')

# L'objet db DOIT être instancié ici pour que models.py puisse l'importer
db = SQLAlchemy(app)

from . import models

@app.cli.command("init-db")
def init_db():
    models.init_db()
    print("Base de données initialisée !")

from . import views