import os
import random
import textwrap
from PIL import Image, ImageFont, ImageDraw
from fbapp.models import Content, Gender 

# Dossier de base pour construire des chemins absolus robustes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_content(gender):
    contents = Content.query.filter(Content.gender == Gender[gender]).all()
    return random.choice(contents)

class OpenGraphImage:
    def __init__(self, uid, first_name, description):
        self.location = self._location(uid)
        
        # 1. Création de l'image de fond
        background = self.base()
        
        # 2. Ajout du prénom (taille 70px, position Y 50px)
        self.print_on_img(background, first_name.capitalize(), 70, 50)
        
        # 3. Découpage et écriture de la description
        sentences = textwrap.wrap(description, width=60)
        current_h, pad = 180, 10
        
        for sentence in sentences:
            w, h = self.print_on_img(background, sentence, 40, current_h)
            current_h += h + pad
            
        # 4. Vérification que le dossier static/tmp existe
        save_path = self._path(uid)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 5. Sauvegarde de l'image sur le disque
        background.save(save_path)

    def base(self):
        # Image turquoise 1200x630px
        return Image.new('RGB', (1200, 630), '#18BC9C')

    def print_on_img(self, img, text, size, height):
        font_path = os.path.join(BASE_DIR, 'static', 'fonts', 'Arcon-Regular.otf')
        
        # Chargement de la police avec fallback si le fichier est absent
        try:
            font = ImageFont.truetype(font_path, size)
        except OSError:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(img)
        
        # Mesure du texte compatible avec anciennes et nouvelles versions de Pillow
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            w, h = draw.textsize(text, font)

        position = ((img.width - w) / 2, height)
        
        # Écriture du texte en blanc
        draw.text(position, text, (255, 255, 255), font=font)
        return (w, h)

    def _path(self, uid):
        # Chemin complet vers le fichier static/tmp/
        return os.path.join(BASE_DIR, 'static', 'tmp', f'{uid}.jpg')

    def _location(self, uid):
        # Chemin relatif renvoyé à la vue Flask
        return f'tmp/{uid}.jpg'