from models import db


class Function(db.Model):
    """
    Function model.
    """
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    created = db.Column(db.DateTime)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )

    user = db.relationship('User')
