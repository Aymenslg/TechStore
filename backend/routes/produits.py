from flask import Blueprint, jsonify, request
from app import db
import re

produits_bp = Blueprint("produits", __name__)

@produits_bp.route("/api/produits", methods=["GET"])
def get_produits():
    query = {}
    categorie = request.args.get('categorie')
    search = request.args.get('search')
    filtre = request.args.get('filtre', 'normal')
    prix_cible = request.args.get('prix_cible')
    page = int(request.args.get('page', 1))
    limit = 50
    skip = (page - 1) * limit

    if categorie:
        query["categorie"] = categorie
    if search:
        query["nom"] = {"$regex": search, "$options": "i"}

    def extraire_prix(prix_str):
        if not prix_str:
            return 0
        nombre = re.sub(r'[^0-9.]', '', str(prix_str))
        try:
            return float(nombre) * 0.13
        except:
            return 0

    def extraire_note(note_str):
        try:
            note_str = re.sub(r'[^0-9.]', '', str(note_str or '0'))
            return float(note_str) if note_str else 0
        except:
            return 0

    produits = list(db.produits.find(query, {"_id": 0}))

    if filtre == "plus_cher":
        produits.sort(key=lambda x: extraire_prix(x.get('prix_reduit', '0')), reverse=True)

    elif filtre == "moins_cher":
        produits = [p for p in produits if extraire_prix(p.get('prix_reduit', '0')) > 0]
        produits.sort(key=lambda x: extraire_prix(x.get('prix_reduit', '0')))

    elif filtre == "proche_prix" and prix_cible:
        try:
            prix_cible_num = float(prix_cible)
            produits = [p for p in produits if extraire_prix(p.get('prix_reduit', '0')) > 0]
            produits.sort(key=lambda x: abs(extraire_prix(x.get('prix_reduit', '0')) - prix_cible_num))
        except:
            pass

    elif filtre == "bonne_qualite":
        produits = [p for p in produits if extraire_note(p.get('note', '0')) > 0]
        produits.sort(key=lambda x: extraire_note(x.get('note', '0')), reverse=True)

    elif filtre == "qualite_prix":
        produits = [p for p in produits if extraire_prix(p.get('prix_reduit', '0')) > 0 and extraire_note(p.get('note', '0')) > 0]
        produits.sort(key=lambda x: extraire_note(x.get('note', '0')) / extraire_prix(x.get('prix_reduit', '0')), reverse=True)

    total = len(produits)
    total_pages = (total + limit - 1) // limit
    produits_page = produits[skip:skip + limit]

    return jsonify({
        "produits": produits_page,
        "total": total,
        "page": page,
        "total_pages": total_pages
    })

@produits_bp.route("/api/produits/categories", methods=["GET"])
def get_categories():
    categories = db.produits.distinct("categorie")
    return jsonify(categories)

@produits_bp.route("/api/produits/brands", methods=["GET"])
def get_brands():
    brands = db.produits.distinct("marque")
    return jsonify(brands)

@produits_bp.route("/api/produits/detail", methods=["GET"])
def get_produit():
    nom = request.args.get('nom', '')
    if not nom:
        return jsonify({"message": "Nom manquant"}), 400

    # Recherche exacte d'abord
    produit = db.produits.find_one({"nom": nom}, {"_id": 0})
    if produit:
        return jsonify(produit)

    # Nettoyer le nom tronqué
    nom_court = nom.replace('...', '').strip()

    # Recherche par début de nom
    produit = db.produits.find_one(
        {"nom": {"$regex": "^" + re.escape(nom_court[:60]), "$options": "i"}},
        {"_id": 0}
    )
    if produit:
        return jsonify(produit)

    # Recherche partielle si toujours pas trouvé
    produit = db.produits.find_one(
        {"nom": {"$regex": re.escape(nom_court[:40]), "$options": "i"}},
        {"_id": 0}
    )
    if produit:
        return jsonify(produit)

    return jsonify({"message": "Produit non trouvé"}), 404