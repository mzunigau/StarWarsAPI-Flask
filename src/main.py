"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
import json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')  # Change this "super secret" with something else!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    user = User.filter.get(current_user_id)
    
    return jsonify({"id": user.id, "username": user.username }), 200

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
@jwt_required()
def indexUsers():
    usuarios = User.query.all()
    usuarios = list(map(lambda x: x.serialize(), usuarios))
    return jsonify(usuarios), 200


@app.route('/planets', methods=['GET'])
def indexPlanets():
    planets = Planet.query.all()
    planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets), 200

@app.route('/users', methods=['POST'])
def createUser():
    body = request.get_json() # get the request body content
    userNew = User(username=body['username'], first_name=body['first_name'], last_name=body['last_name'],email=body['email'],password=body['password'], is_active=body['is_active'])
    db.session.add(userNew)
    db.session.commit()
    return jsonify(serialize(userNew)), 200    

@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    body = request.get_json()
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    #For para recorrer el listado del JSON
    for char in body["characters"]:
        #query para buscar el personaje
        charNew = Character.query.get(char["id"]) 
        #append para agregar el personaje al listado del user       
    
    db.session.commit()   
    return "POK", 200

@app.route('/users/<int:id>', methods=['GET'])
def getUser(id):
    user = User.query.get(id)
    return jsonify(serialize(user)), 200        

@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUsers(id):
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
