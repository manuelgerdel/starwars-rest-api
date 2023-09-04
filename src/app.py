"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
# from werkzeug.security import generate_password_hash
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Users


@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()
    print(users)
    serialized_users = [user.serialize() for user in users]
    return jsonify({"Users": serialized_users}), 200


# Characters

@app.route('/character', methods=['POST'])
def add_character():
    data = request.get_json()
    data_name = data.get("name", None)
    data_gender = data.get("gender", None)
    data_birth = data.get("birth_year", None)
    data_height = data.get("height", None)
    data_species = data.get("species", None)

    new_character = Character(name=data_name, gender=data_gender,
                              birth_year=data_birth, height=data_height, species=data_species)

    print(new_character)
    try:
        db.session.add(new_character)
        db.session.commit()
        print(new_character.serialize())
        return jsonify(new_character.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify({"Characters": serialized_characters}), 200


@app.route('/character/<int:id>', methods=['GET'])
def get_character_by_id(id):
    current_character = Character.query.get(id)
    if not current_character:
        return jsonify({"error": "Character not found"}), 404

    return jsonify({"Character": current_character.serialize()}), 200


@app.route('/character/<int:id>', methods=['PUT'])
def update_character_by_id(id):
    data = request.get_json()
    name = data.get("name", None)
    gender = data.get("gender", None)
    birth = data.get("birth_year", None)
    height = data.get("height", None)
    species = data.get("species", None)
    # favorite = data.get("favorite", None)

    updated_character = Character.query.get(id)
    if not updated_character:
        return jsonify({"error": "That character doesn't exist"}), 404

    try:
        updated_character.name = name
        updated_character.gender = gender
        updated_character.birth_year = birth
        updated_character.height = height
        updated_character.species = species
       # updated_character.favorite = favorite

        db.session.commit()
        return jsonify({"Updated Character": updated_character.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"message": error.args}), 500


@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character_by_id(id):
    character_to_delete = Character.query.get(id)
    if not character_to_delete:
        return jsonify({"error": "That character is not in the system"}), 404

    try:
        db.session.delete(character_to_delete)
        db.session.commit()
        return jsonify("Your character wass deleted successfully!"), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"message": error.args}), 500


# Planets

@app.route('/planet', methods=['POST'])
def add_planet():
    data = request.get_json()
    data_name = data.get("name", None)
    data_population = data.get("population", None)
    data_rotation_period = data.get("rotation_period", None)
    data_climate = data.get("climate", None)

    new_planet = Planet(name=data_name, population=data_population,
                        rotation_period=data_rotation_period, climate=data_climate)

    # print(new_planet)
    try:
        db.session.add(new_planet)
        db.session.commit()
        # print(new_planet.serialize())
        return jsonify(new_planet.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return error, 500


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify({"Planets": serialized_planets}), 200


@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    current_planet = Planet.query.get(id)
    if not current_planet:
        return jsonify({"error": "Planet not found"}), 404

    return jsonify({"Planet": current_planet.serialize()}), 200


@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet_by_id(id):
    data = request.get_json()
    name = data.get("name", None)
    population = data.get("population", None)
    rotation_period = data.get("rotation_period", None)
    climate = data.get("climate", None)

    updated_planet = Planet.query.get(id)
    if not updated_planet:
        return jsonify({"error": "That planet doesn't exist"}), 404

    try:
        updated_planet.name = name
        updated_planet.population = population
        updated_planet.rotation_period = rotation_period
        updated_planet.climate = climate

        db.session.commit()
        return jsonify({"Updated Planet": updated_planet.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"message": error.args}), 500


@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet_by_id(id):
    planet_to_delete = Planet.query.get(id)
    if not planet_to_delete:
        return jsonify({"error": "That planet is not in the system"}), 404

    try:
        db.session.delete(planet_to_delete)
        db.session.commit()
        return jsonify("Your planet wass deleted successfully!"), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"message": error.args}), 500


# Favorites

@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_favorites_by_user_id(id):

    favorites = Favorite.query.filter_by(user_id=id).all()
    if not favorites:
        return jsonify({"error": "No favorites available for that user"}), 404

    serialized_favorites = [favorite.serialize() for favorite in favorites]

    return jsonify({"Favorites": serialized_favorites})


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    data = request.get_json()
    data_user = data.get("user_id", None)

    favorite_character = Favorite(
        user_id=data_user, character_id=character_id)

    try:
        db.session.add(favorite_character)
        db.session.commit()
        return jsonify({"Favorite added": favorite_character.serialize()}), 201

    except Exception as error:
        db.session.rollback()
        print(error.args)
        return jsonify({"message": error.args}), 500


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character_by_id(character_id):
    data = request.get_json()
    data_user_id = data.get("user_id")
    character_to_delete = Favorite.query.filter_by(
        user_id=data_user_id, character_id=character_id).first()
    if not character_to_delete:
        return jsonify({"error": "That character or user is not in the system"}), 404

    try:
        db.session.delete(character_to_delete)
        db.session.commit()
        return jsonify("Your character was deleted successfully"), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"message": error.args}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    data_user = data.get("user_id", None)

    favorite_planet = Favorite(
        user_id=data_user, planet_id=planet_id)

    try:
        db.session.add(favorite_planet)
        db.session.commit()
        return jsonify({"Favorite added": favorite_planet.serialize()}), 201

    except Exception as error:
        db.session.rollback()
        print(error.args)
        return jsonify({"message": error.args}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet_by_id(planet_id):
    data = request.get_json()
    data_user_id = data.get("user_id")
    planet_to_delete = Favorite.query.filter_by(
        user_id=data_user_id, planet_id=planet_id).first()
    if not planet_to_delete:
        return jsonify({"error": "That planet or user is not in the system"}), 404

    try:
        db.session.delete(planet_to_delete)
        db.session.commit()
        return jsonify("Your planet was deleted successfully"), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"message": error.args}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
