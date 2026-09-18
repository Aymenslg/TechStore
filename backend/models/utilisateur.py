def utilisateur_model(nom, email, mot_de_passe):
    return {
        "nom": nom,
        "email": email,
        "mot_de_passe": mot_de_passe,
        "commandes": []
    }