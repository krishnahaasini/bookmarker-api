from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = "product_table"
    pass

@app.route("/")
def hello():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
