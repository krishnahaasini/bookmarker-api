from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path


BASEDIR = Path(__file__).resolve().parent.parent
TEST_DB_PATH = BASEDIR / "test.sqlite"
DB_URI = "sqlite:///" + str(TEST_DB_PATH)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from my_app.catalog.views import catalog

app.register_blueprint(catalog)

with app.app_context():
    db.create_all()


