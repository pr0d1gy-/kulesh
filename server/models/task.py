from models import db


class Task(db.Model):
    """
    Task model.
    """
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.Text)

    updated = db.Column(db.DateTime)
    # created = db.Column(db.DateTime)

    version = db.Column(db.String(100))

    function_id = db.Column(
        db.Integer, db.ForeignKey('function.id', ondelete='CASCADE')
    )

    function = db.relationship('Function')

    data_id = db.Column(db.Integer, db.ForeignKey('data.id'))

    data = db.relationship('Data')
