from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # Relations
    favorites = db.relationship("Favorite", backref="user", lazy=True)

    def __repr__(self):
        return f'<User {self.id}>'

    def serialize(self):
       # print(self.favorites)
        favorites = [favorite.serialize() for favorite in self.favorites]
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": favorites
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    birth_year = db.Column(db.String(20), unique=False, nullable=False)
    height = db.Column(db.String(100), unique=False, nullable=False)
    species = db.Column(db.String(30), unique=False, nullable=False)

    # Relations
    favorites = db.relationship("Favorite", backref="character", lazy=True)

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        favorites = [favorite.serialize() for favorite in self.favorites]
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "species": self.species,
            "favorites": favorites
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=True, nullable=False)
    rotation_period = db.Column(db.String(20), unique=False, nullable=False)
    climate = db.Column(db.String(20), unique=False, nullable=False)

    # Relation
    favorites = db.relationship("Favorite", backref="planet", lazy=True)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "climate": self.climate,
            "favorites": self.favorites
            # do not serialize the password, its a security breach
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), unique=False, nullable=False)
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.id"), unique=False, nullable=True)
    planet_id = db.Column(
        db.Integer, db.ForeignKey("planet.id"), unique=False, nullable=True)

    def __repr__(self):
        return f'<Favorite {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            # do not serialize the password, its a security breach
        }
