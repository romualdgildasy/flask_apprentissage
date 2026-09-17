import os

# Calcule le chemin absolu du dossier fbapp
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "#d#JCqTTW\nilK\\7m\x0bp#\tj~#H"
FB_APP_ID = 1200420960103822

# Indique le chemin du fichier SQLite app.db
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')