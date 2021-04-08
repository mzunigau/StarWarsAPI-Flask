from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorites_planets= db.Table('favorites_planets', db.Column("user_id", db.Integer, db.ForeignKey("usuarios.id")),db.Column("planet_id", db.Integer, db.ForeignKey("planetas.id")))
favorites_characters= db.Table('favorites_characters', db.Column("user_id", db.Integer, db.ForeignKey("usuarios.id")),db.Column("character_id", db.Integer, db.ForeignKey("personajes.id")))

class User(db.Model):
    __tablename__='usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets = db.relationship("Planet" , secondary=favorites_planets)
    characters = db.relationship("Character", secondary=favorites_characters)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "email": self.email,
            "planets": list(map(lambda x: x.serialize(), self.planets)),
            "characters": list(map(lambda x: x.serialize(), self.characters))
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }


        
class Character(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }



