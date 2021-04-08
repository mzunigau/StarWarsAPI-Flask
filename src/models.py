from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

planets_favorites = db.Table('planets_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'))
)
   

characters_favorites = db.Table('characters_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planets = db.relationship('Planet', secondary=planets_favorites, back_populates='users')
    characters = db.relationship('Character', secondary=characters_favorites, back_populates='users')
    
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship("User", secondary="planets_favorites", back_populates="planets")


    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship("User", secondary="characters_favorites", back_populates="characters")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }