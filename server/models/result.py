from models import db


class Result(db.Model):
    """
    Result model.
    """
    id = db.Column(db.Integer, primary_key=True)

    date_start = db.Column(db.DateTime)

    date_end = db.Column(db.DateTime)

    task_id = db.Column(
        db.Integer, db.ForeignKey('task.id', ondelete='CASCADE')
    )

    task = db.relationship('Task')

    result = db.Column(db.Text)

    status_id = db.Column(
        db.Integer, db.ForeignKey('status.id', ondelete='CASCADE')
    )

    status = db.relationship('Status')
