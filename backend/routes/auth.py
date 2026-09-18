from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from models.utilisateur import utilisateur_model
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    nom = data.get("nom", "")
    email = data.get("email", "")
    mot_de_passe = data.get("mot_de_passe") or data.get("password", "")

    if not nom or not email or not mot_de_passe:
        return jsonify({"message": "Tous les champs sont obligatoires !"}), 400

    existing_user = db.utilisateurs.find_one({"email": email})
    if existing_user:
        return jsonify({"message": "Email déjà utilisé !"}), 400

    mot_de_passe_chiffre = bcrypt.generate_password_hash(mot_de_passe).decode("utf-8")
    utilisateur = utilisateur_model(nom, email, mot_de_passe_chiffre)
    result = db.utilisateurs.insert_one(utilisateur)

    token = create_access_token(identity=str(result.inserted_id))
    return jsonify({
        "message": "Compte créé avec succès !",
        "token": token,
        "user": {"nom": nom, "email": email, "role": "user"}
    }), 201

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "")
    mot_de_passe = data.get("mot_de_passe") or data.get("password", "")

    utilisateur = db.utilisateurs.find_one({"email": email})
    if not utilisateur:
        return jsonify({"message": "Email incorrect !"}), 401

    if not bcrypt.check_password_hash(utilisateur["mot_de_passe"], mot_de_passe):
        return jsonify({"message": "Mot de passe incorrect !"}), 401

    token = create_access_token(identity=str(utilisateur["_id"]))
    return jsonify({
        "token": token,
        "user": {
            "nom": utilisateur["nom"],
            "email": utilisateur["email"],
            "role": utilisateur.get("role", "user")
        }
    }), 200

@auth_bp.route("/api/auth/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    try:
        utilisateur = db.utilisateurs.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "mot_de_passe": 0})
        if not utilisateur:
            return jsonify({"message": "Utilisateur non trouvé"}), 404
        return jsonify({"user": utilisateur}), 200
    except Exception as e:
        return jsonify({"message": "Erreur serveur"}), 500