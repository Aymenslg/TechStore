import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["techstore"]

df = pd.read_csv("electronics_product.csv")
df = df.dropna(subset=["name", "actual_price"])


def detecter_categorie(nom):
    nom = str(nom).lower()

    # EXCLUSIONS PRIORITAIRES — toujours accessoire
    exclusions = [
        "cleaning", "cleaner", "dust", "wipe", "cloth", "spray", "blower",
        "case for", "cover for", "back cover", "flip cover", "bumper case",
        "tempered glass", "screen guard", "screen protector", "screen filter",
        "pouch for", "bag for", "stand for", "holder for", "mount for",
        "cable", "charger", "adapter", "hub", "converter", "otg",
        "power bank", "extension board", "surge protector",
        "memory card", "sd card", "pen drive", "usb drive", "hard disk",
        "keyboard cover", "laptop skin", "laptop sleeve", "laptop bag",
        "camera bag", "camera case", "camera strap", "camera lens cap",
        "lens filter", "lens hood", "tripod", "gimbal", "selfie stick",
        "ring light", "microphone", "gaming chair", "desk mat",
        "monitor stand", "phone stand", "tablet stand",
        "wall mount", "tv bracket", "remote control",
        "battery", "ink cartridge", "toner", "printer paper"
    ]

    if any(x in nom for x in exclusions):
        return "accessoire"

    # LAPTOP
    if any(x in nom for x in [
        "laptop", "macbook", "notebook", "chromebook",
        "vivobook", "thinkpad", "ideapad", "pavilion",
        "inspiron", "zenbook", "surface laptop", "legion",
        "predator helios", "rog strix", "swift ", "spin ",
        "aspire ", "nitro 5", "victus"
    ]):
        return "laptop"

    # TABLETTE
    elif any(x in nom for x in [
        "tablet", "ipad", "kindle", "galaxy tab",
        "fire hd", "tab lite", "tab ultra", "matebook"
    ]):
        return "tablette"

    # MONTRE
    elif any(x in nom for x in [
        "smart watch", "smartwatch", "fitness band",
        "fire-boltt", "fire boltt", "boat watch",
        "noise watch", "mi band", "fitbit", "amazfit",
        "fossil gen", "garmin", "polar watch", "withings",
        "noise colorfit", "pebble smartwatch", "titan smart",
        "fastrack reflex", "health watch", "activity tracker"
    ]):
        return "montre"

    # TV
    elif any(x in nom for x in [
        "smart tv", "qled", "oled tv", "led tv",
        "android tv", "fire tv stick", "television",
        "4k tv", "full hd tv", "ultra hd tv",
        "google tv", "roku tv", "webos tv"
    ]):
        return "tv"

    # AUDIO
    elif any(x in nom for x in [
        "earphone", "earbuds", "headphone", "airpods",
        "speaker", "soundbar", "neckband", "tws",
        "in-ear", "over-ear", "on-ear", "wired earphone",
        "bluetooth earphone", "noise cancelling",
        "home theatre", "subwoofer", "party speaker"
    ]):
        return "audio"

    # CAMERA — uniquement appareils photo vrais
    elif any(x in nom for x in [
        "dslr", "mirrorless camera", "action camera",
        "gopro hero", "webcam hd", "security camera",
        "cctv camera", "ip camera", "dash cam",
        "dashcam", "trail camera", "360 camera",
        "instant camera", "polaroid camera",
        "digital camera", "point and shoot"
    ]):
        return "camera"

    # PC
    elif any(x in nom for x in [
        "desktop pc", "gaming desktop", "all-in-one pc",
        "imac", "mini pc", "nuc ", "workstation",
        "monitor ", "gaming monitor", "curved monitor",
        "mechanical keyboard", "gaming mouse",
        "wireless keyboard", "wireless mouse"
    ]):
        return "pc"

    # TELEPHONE — en dernier pour éviter les faux positifs
    elif any(x in nom for x in [
        "iphone ", "samsung galaxy s", "samsung galaxy m",
        "samsung galaxy a", "samsung galaxy f",
        "redmi note", "redmi ", "poco x", "poco m",
        "oneplus nord", "oneplus ", "realme narzo",
        "realme ", "vivo v", "vivo y", "vivo t",
        "oppo reno", "oppo a", "oppo f",
        "nokia g", "nokia c", "motorola moto",
        "pixel 6", "pixel 7", "pixel 8",
        "lava blaze", "lava agni", "iqoo ",
        "infinix note", "infinix hot", "infinix zero",
        "tecno spark", "tecno pop", "tecno camon",
        "nothing phone", "asus rog phone",
        "5g smartphone", "4g smartphone"
    ]):
        return "telephone"

    else:
        return "accessoire"


produits = []
for _, row in df.iterrows():
    produit = {
        "nom": str(row["name"]),
        "categorie": detecter_categorie(str(row["name"])),
        "sous_categorie": str(row["sub_category"]),
        "image": str(row["image"]),
        "lien": str(row["link"]),
        "note": str(row["ratings"]),
        "nombre_avis": str(row["no_of_ratings"]),
        "prix_reduit": str(row["discount_price"]),
        "prix_original": str(row["actual_price"]),
    }
    produits.append(produit)

db.produits.drop()
db.produits.insert_many(produits)
print(f"✅ {len(produits)} produits importés !")
print("\n📦 Résultats par catégorie :")
categories = ["telephone", "laptop", "pc", "tv", "audio", "camera", "tablette", "montre", "accessoire"]
for cat in categories:
    count = db.produits.count_documents({"categorie": cat})
    print(f"  {cat}: {count} produits")