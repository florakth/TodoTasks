
from .__init__ import db


class TodoTasks(db.Model):
    __tablename__ = 'todoTasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    is_done = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, is_done):
        self.name = name
        self.is_done = is_done

    def __repr__(self):
        return '<TodoTasks: %r>' % self.name



