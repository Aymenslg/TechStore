from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.commande import commande_model

commandes_bp = Blueprint("commandes", __name__)

@commandes_bp.route("/api/commandes", methods=["POST"])
@jwt_required()
def add_commande():
    data = request.json
    utilisateur_id = get_jwt_identity()
    produits = data.get("produits", [])
    total = data.get("total", 0)
    commande = commande_model(utilisateur_id, produits, total)
    db.commandes.insert_one(commande)
    return jsonify({"message": "Commande passée avec succès !"}), 201

@commandes_bp.route("/api/commandes", methods=["GET"])
@jwt_required()
def get_commandes():
    utilisateur_id = get_jwt_identity()
    commandes = list(db.commandes.find(
        {"utilisateur_id": utilisateur_id},
        {"_id": 0}
    ))
    return jsonify(commandes), 200