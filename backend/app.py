from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)
CORS(app)

try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["techstore"]
    client.server_info()
    print("✅ MongoDB connecté avec succès !")
except Exception as e:
    print(f"❌ Erreur MongoDB : {e}")

from routes.produits import produits_bp
from routes.auth import auth_bp
from routes.commandes import commandes_bp
from routes.chatbot import chatbot_bp

app.register_blueprint(produits_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(commandes_bp)
app.register_blueprint(chatbot_bp)

if __name__ == "__main__":
    app.run(debug=True)