from flask import render_template, url_for, request
from . import app
from .utils import find_content, OpenGraphImage

@app.route('/')
@app.route('/index/')
def index():
    description = """
        Toi, tu n'as pas peur d'être seul ! Les grands espaces et les aventures sont faits pour toi. D'ailleurs, Koh Lanta est ton émission préférée !
    """
    
    # 1. Vérifie si une image de résultat spécifique est passée dans l'URL
    if 'img' in request.args:
        img = request.args['img']
        og_url = url_for('index', img=img, _external=True)
        og_image = url_for('static', filename=img, _external=True)
    else:
        og_url = url_for('index', _external=True)
        og_image = url_for('static', filename='tmp/sample.jpg', _external=True)
        
    page_title = "Le test ultime"
    og_description = "Découvre qui tu es vraiment en faisant le test ultime !"
    
    return render_template(
        'index.html',
        user_name='Julio',
        user_image=url_for('static', filename='img/profile.png'),
        description=description,
        blur=True,
        page_title=page_title,
        og_url=og_url,
        og_image=og_image,
        og_description=og_description
    )

@app.route('/result/')
def result():
    gender = request.args.get('gender', 'male')
    user_name = request.args.get('first_name', 'Aventurier')
    uid = request.args.get('id', '123456')

    profile_pic = f'http://graph.facebook.com/{uid}/picture?type=large'
    description = find_content(gender).description
    
    ## Génération et récupération du chemin de la photo dynamique
    img = OpenGraphImage(uid, user_name, description).location
    
    # URL absolue de redirection pour le bouton de partage Facebook
    # Construction de l'URL absolue OpenGraph pour la page d'accueil avec le paramètre img
    og_url = url_for('index', img=img, _external=True)

    return render_template(
        'result.html',
        user_name=user_name,
        user_image=profile_pic,
        description=description,
        og_url=og_url
    )