from datetime import datetime

def commande_model(utilisateur_id, produits, total):
    return {
        "utilisateur_id": utilisateur_id,
        "produits": produits,
        "total": total,
        "statut": "en attente",
        "date": datetime.now()
    }