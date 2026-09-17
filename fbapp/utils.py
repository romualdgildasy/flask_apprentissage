import random
from .models import Content, Gender

def find_content(gender):
    # Cherche tous les contenus correspondant au genre reçu ('male', 'female', etc.)
    contents = Content.query.filter(Content.gender == Gender[gender]).all()
    # Retourne un élément au hasard parmi la liste
    return random.choice(contents)