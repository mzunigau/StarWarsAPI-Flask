from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets = db.relationship("Planet" , secondary= "planets_favorites")
    characters = db.relationship("Character", secondary="characters_favorites")
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship("User", secondary="planets_favorites")


    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship("User", secondary="characters_favorites")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
class Favorites_Planets(db.Model):
    __tablename__ = 'planets_favorites'
    user_id = db.Column( db.Integer , db.ForeignKey('users.id'), primary_key = True)
    planet_id = db.Column( db.Integer , db.ForeignKey('planets.id'), primary_key = True)
    user = db.relationship(User, backref=backref("planets_favorites", cascade="all, delete-orphan"))
    planet = db.relationship(Planet, backref=backref("planets_favorites", cascade="all, delete-orphan"))
    
    def __repr__(self):
        return '<Favorites_Planets %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            # do not serialize the password, its a security breach
        }

class Favorites_Characters(db.Model): 
    __tablename__ = 'characters_favorites'  
    user_id = db.Column( db.Integer, db.ForeignKey('users.id'), primary_key = True)
    character_id = db.Column( db.Integer, db.ForeignKey('characters.id'), primary_key = True)
    user = db.relationship(User, backref=backref("characters_favorites", cascade="all, delete-orphan"))
    character = db.relationship(Character, backref=backref("characters_favorites", cascade="all, delete-orphan"))
    
    def __repr__(self):
        return '<Favorites_Characters %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }
    

