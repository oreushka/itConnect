from . import db
from flask_login import UserMixin
from sqlalchemy import func

def really_secret_key():
    return "asafonova2002@gmail.com"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = data = db.Column(db.String(100))
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    flag = db.Column(db.Integer)
    #   user.id пишется с маленькой буквы, так как мы используем db.ForeignKey а в нём в названии класса большие буквы превращаются в маленькие
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin): #User Mixin для пихания класса User в flask
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # Note пишется с большой буквы так как мы пишем название класса в db.relationship
    # db.relationship испольхуется тогда,
    # когда мы должны настроить множественное отнощение( Один пользователь имеет много постов)
    rank = db.Column(db.Integer, db.ForeignKey('rank.id'), default = 0)
    notes = db.relationship('Note', backref="Owner")

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users_with_rank = db.relationship("User", backref="RankOfUser")
