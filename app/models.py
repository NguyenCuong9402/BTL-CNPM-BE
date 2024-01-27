
from app.extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(250))
    password = db.Column(db.String(250))
    email = db.Column(db.String(250))
    sex = db.Column(db.Integer()) # 0: nữ, 1 : nam
    birth = db.Column(db.Date)
    language = db.Column(db.String(50))
    news = db.Column(db.String(50))







