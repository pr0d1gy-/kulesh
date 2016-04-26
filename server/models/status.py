from models import db


class Status(db.Model):
    """
    Status model.
    """
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(40))
