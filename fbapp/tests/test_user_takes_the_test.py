import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from flask_testing import LiveServerTestCase
from flask import url_for

from .. import app, models


class TestUserTakesTheTest(LiveServerTestCase):
    def create_app(self):
        # Charge la configuration propre aux tests
        app.config.from_object('fbapp.tests.config')
        return app

    def setUp(self):
        """Initialisation du navigateur et de la base de données avant chaque test"""
        # Utilisation de Firefox (nécessite geckodriver) ou Chrome via webdriver.Chrome()
        self.driver = webdriver.Firefox()
        self.wait = ui.WebDriverWait(self.driver, 10)
        
        # Initialise la base de données de test SQLite
        with app.app_context():
            models.init_db()

        # URL cible attendue en fin de parcours
        with app.test_request_context():
            self.result_page = url_for(
                'result',
                first_name=app.config['FB_USER_NAME'],
                id=app.config['FB_USER_ID'],
                gender=app.config['FB_USER_GENDER'],
                _external=True
            )

    def tearDown(self):
        """Fermeture du navigateur après chaque test"""
        self.driver.quit()

    def get_el(self, selector):
        return self.driver.find_element_by_css_selector(selector)

    def enter_text_field(self, selector, text):
        text_field = self.get_el(selector)
        text_field.clear()
        text_field.send_keys(text)

    def clicks_on_login(self):
        # Attente du chargement de l'iframe du bouton Facebook Login
        self.wait.until(lambda driver: self.driver.find_element_by_tag_name("iframe").is_displayed())
        button = self.get_el(".fb-login-button")
        ActionChains(self.driver).click(button).perform()

    def sees_login_page(self):
        # Attente de l'ouverture de la nouvelle fenêtre pop-up Facebook
        self.wait.until(lambda driver: len(self.driver.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        # Attente du champ email
        self.wait.until(lambda driver: self.get_el('#email'))
        assert self.driver.current_url.startswith('https://www.facebook.com/login.php')

    def submits_form(self):
        # Remplissage des identifiants dans la pop-up Facebook
        self.enter_text_field('#email', app.config['FB_USER_EMAIL'])
        self.enter_text_field('#pass', app.config['FB_USER_PW'])
        self.get_el('#loginbutton input[name=login]').click()

    def test_user_login(self):
        # 1. L'utilisateur navigue sur la page d'accueil
        self.driver.get(self.get_server_url())
        
        # 2. Clic sur le bouton de connexion Facebook
        self.clicks_on_login()
        
        # 3. Ouverture de la pop-up d'authentification
        self.sees_login_page()
        
        # 4. Soumission des identifiants
        self.submits_form()
        
        # 5. Retour sur la fenêtre principale et attente de la fermeture de la pop-up
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.wait.until(lambda driver: len(self.driver.window_handles) == 1)
        
        # 6. Attente de la redirection finale vers la page de résultat
        self.wait.until(lambda driver: '?' in self.driver.current_url)
        assert self.driver.current_url == self.result_page