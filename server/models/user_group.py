from models import db


class UserGroup(db.Model):
    """
    User Group model.
    """
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
