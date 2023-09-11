from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class TaskTwo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)