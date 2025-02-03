from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Restaurant

app = Flask(__name__)
app.config.from_object("config.Config")

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        token = user.generate_token()
        return jsonify({"token": token, "user": {"username": user.username, "email": user.email}})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{"id": r.id, "name": r.name, "location": r.location, "rating": r.rating} for r in restaurants])

if __name__ == "__main__":
    app.run(debug=True)
