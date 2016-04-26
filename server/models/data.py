from models import db


class Data(db.Model):
    """
    Data model.
    """
    id = db.Column(db.Integer, primary_key=True)

    data = db.Column(db.Text)

    link = db.Column(db.Text)
