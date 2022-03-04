from datetime import datetime
from flask_login import UserMixin
from MyFitnessPup import db


class DogFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    brandName = db.Column(db.String(50), nullable=False)
    calories = db.Column(db.Integer, default=300, nullable=False)
    meal = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Food %r>" % self.id


class UserInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pets = db.relationship("Pets", backref="user_info", lazy=True)


class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user_info.id"), nullable=False)
    food = db.relationship("DogFood", backref="dog_food", lazy=True)
    weight = db.relationship("PetWeight", backref="pet_weight", lazy=True)


class PetWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    weight = db.Column(db.Integer, nullable=False, default=0)
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)
