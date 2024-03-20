from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager
from config import Config

# Initialisiert die Flask-Anwendung
app = Flask(__name__)
# Lädt die Konfigurationen aus einer Config-Klasse
app.config.from_object(Config)
# Initialisiert die Datenbank mit SQLAlchemy
db = SQLAlchemy(app)
# Initialisiert Flask-Migrate für Datenbankmigrationen
migrate = Migrate(app, db)
# Initialisiert Flask-Login für die Benutzerauthentifizierung
login = LoginManager(app)
# Definiert die Ansicht, die für nicht authentifizierte Benutzer aufgerufen wird
login.login_view = 'login'

# Importiert die Routen und Modelle der Anwendung
from app import routes, models
