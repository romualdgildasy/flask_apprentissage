from flask import Flask

from .views import app
from . import models

# Crée la commande 'flask init-db' pour le terminal
@app.cli.command("init-db")
def init_db():
    models.init_db()