from flask import Blueprint, jsonify, request
from app import db
from groq import Groq
import os
import re

chatbot_bp = Blueprint("chatbot", __name__)
client_ai = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extraire_prix(prix_str):
    if not prix_str:
        return 0
    nombre = re.sub(r'[^0-9.]', '', str(prix_str))
    try:
        return float(nombre) * 0.13
    except:
        return 0

@chatbot_bp.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    message = data["message"]

    categories = ["telephone", "laptop", "pc", "tv", "audio",
                  "camera", "tablette", "montre", "accessoire"]

    produits_text = ""
    for cat in categories:
        produits_cat = list(db.produits.find(
            {"categorie": cat},
            {"_id": 0, "nom": 1, "prix_reduit": 1, "prix_original": 1,
             "categorie": 1, "note": 1, "nombre_avis": 1}
        ).limit(10))
        for p in produits_cat:
            prix_dh = round(extraire_prix(p.get('prix_reduit', '0')))
            note = p.get('note', 'N/A')
            produits_text += f"- {p['nom']} | prix: {prix_dh} DH | note: {note} | categorie: {p['categorie']}\n"

    prompt = f"""
    Tu es un assistant pour TechStore, une boutique d'électronique marocaine.
    Les prix sont en Dirhams marocains (DH).

    Voici un échantillon de produits disponibles :
    {produits_text}

    Le client dit : "{message}"

    Instructions :
    1. Réponds en français avec un paragraphe utile et naturel
    2. Si le client demande "le plus cher" → recommande le produit avec le prix le plus élevé
    3. Si le client demande "le moins cher" → recommande le produit avec le prix le plus bas
    4. Si le client demande "proche de X DH" → recommande le produit dont le prix est le plus proche de X
    5. Si le client demande "bonne qualité" → recommande les produits avec la meilleure note
    6. Si le client demande "bonne qualité bon prix" → recommande les produits avec bonne note ET prix raisonnable
    7. Mentionne toujours le nom exact du produit, son prix en DH et sa note

    À la fin indique la catégorie concernée parmi :
    telephone, laptop, pc, tv, audio, camera, tablette, montre, accessoire
    Format: CATEGORIE: <nom_categorie>

    Et indique le type de filtre appliqué :
    FILTRE: plus_cher | moins_cher | proche_prix | bonne_qualite | qualite_prix | normal
    Et si proche prix indique: PRIX_CIBLE: <montant>
    """

    response = client_ai.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    texte = response.choices[0].message.content

    # Extraire catégorie
    categorie = None
    if "CATEGORIE:" in texte:
        ligne = [l for l in texte.split("\n") if "CATEGORIE:" in l]
        if ligne:
            cat = ligne[0].split("CATEGORIE:")[-1].strip().lower()
            if cat in categories:
                categorie = cat
            texte = texte.replace(ligne[0], "").strip()

    # Extraire filtre
    filtre = "normal"
    if "FILTRE:" in texte:
        ligne_filtre = [l for l in texte.split("\n") if "FILTRE:" in l]
        if ligne_filtre:
            filtre = ligne_filtre[0].split("FILTRE:")[-1].strip().lower()
            texte = texte.replace(ligne_filtre[0], "").strip()

    # Extraire prix cible
    prix_cible = None
    if "PRIX_CIBLE:" in texte:
        ligne_prix = [l for l in texte.split("\n") if "PRIX_CIBLE:" in l]
        if ligne_prix:
            try:
                prix_cible = float(re.sub(r'[^0-9.]', '', ligne_prix[0].split("PRIX_CIBLE:")[-1]))
            except:
                prix_cible = None
            texte = texte.replace(ligne_prix[0], "").strip()

    # Filtrer les produits selon le filtre
    produits_filtres = []
    if categorie:
        tous_produits = list(db.produits.find(
            {"categorie": categorie},
            {"_id": 0}
        ))

        # Ajouter prix et note en numérique
        for p in tous_produits:
            p['prix_dh'] = extraire_prix(p.get('prix_reduit', '0'))
            try:
                note_str = re.sub(r'[^0-9.]', '', str(p.get('note', '0') or '0'))
                p['note_num'] = float(note_str) if note_str else 0
            except:
                p['note_num'] = 0

        if filtre == "plus_cher":
            tous_produits.sort(key=lambda x: x['prix_dh'], reverse=True)
            produits_filtres = tous_produits[:10]

        elif filtre == "moins_cher":
            tous_produits_valides = [p for p in tous_produits if p['prix_dh'] > 0]
            tous_produits_valides.sort(key=lambda x: x['prix_dh'])
            produits_filtres = tous_produits_valides[:10]

        elif filtre == "proche_prix" and prix_cible:
            tous_produits_valides = [p for p in tous_produits if p['prix_dh'] > 0]
            tous_produits_valides.sort(key=lambda x: abs(x['prix_dh'] - prix_cible))
            produits_filtres = tous_produits_valides[:10]

        elif filtre == "bonne_qualite":
            tous_produits_valides = [p for p in tous_produits if p['note_num'] > 0]
            tous_produits_valides.sort(key=lambda x: x['note_num'], reverse=True)
            produits_filtres = tous_produits_valides[:10]

        elif filtre == "qualite_prix":
            tous_produits_valides = [p for p in tous_produits if p['prix_dh'] > 0 and p['note_num'] > 0]
            tous_produits_valides.sort(key=lambda x: x['note_num'] / x['prix_dh'], reverse=True)
            produits_filtres = tous_produits_valides[:10]

        else:
            produits_filtres = tous_produits[:10]

        # Nettoyer les champs temporaires
        for p in produits_filtres:
            p.pop('prix_dh', None)
            p.pop('note_num', None)

    return jsonify({
        "reponse": texte.strip(),
        "categorie": categorie,
        "produits": produits_filtres,
        "filtre": filtre
    }), 200