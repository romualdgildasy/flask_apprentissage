from flask import Flask, render_template, url_for
from . import app

@app.route('/')
@app.route('/index/')
def index():
    description = """
        Toi, tu n'as pas peur d'être seul ! Les grands espaces et les aventures sont faits pour toi. D'ailleurs, Koh Lanta est ton émission préférée ! Bientôt tu partiras les cheveux au vent sur ton radeau. Tu es aussi un idéaliste chevronné. Quelle chance !
    """
    return render_template(
        'index.html',
        user_name='Julien',
        user_image=url_for('static', filename='img/profile.png'),
        description=description,
        blur=True
    )

@app.route('/result/')
def result():
    description = """
        Toi, tu n'as pas peur d'être seul ! Les grands espaces et les aventures sont faits pour toi. D'ailleurs, Koh Lanta est ton émission préférée ! Bientôt tu partiras les cheveux au vent sur ton radeau. Tu es aussi un idéaliste chevronné. Quelle chance !
    """
    return render_template(
        'result.html',
        user_name='Tom',
        user_image=url_for('static', filename='img/profile.png'),
        description=description
    )