from flask import Flask

app = Flask(__name__)
app.config.from_object('fbapp.config')

# L'import des vues se fait APPRÈS la création de l'objet app
from . import views