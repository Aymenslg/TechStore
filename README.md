# 🛒 TechStore - Plateforme E-commerce Intelligente & Assistant IA

> **Projet de Fin d'Année (PFA)** présenté et soutenu à l'**École Marocaine des Sciences de l'Ingénieur (EMSI)**  
> **Réalisé par :**  Aymen Sellag  
> **Encadrant :** Pr. Ahmed Azouaqui  
> **Membres du Jury :** Pr. Hind Ouzif & Pr. Asmahane Tahiri  
> **Année Universitaire :** 2025-2026

---

## 📌 Présentation du Projet
**TechStore** est une plateforme e-commerce moderne spécialisée dans la vente de produits électroniques (smartphones, ordinateurs portables, accessoires, etc.). Conçue selon une démarche d'ingénierie rigoureuse (Design Thinking, analyse SWOT, modélisation UML), la plateforme intègre un **assistant virtuel intelligent (Chatbot)** et un système de recommandation prédictive propulsé par l'intelligence artificielle pour éliminer la friction d'achat et guider l'utilisateur en temps réel.

---

## 🏗️ Architecture et Stack Technique

Le projet repose sur une **architecture découplée en N-Tiers (API-Centric)** garantissant une séparation stricte entre la présentation et la logique métier :

* **Frontend (Présentation) :** Développé en **React.js** (Single Page Application - SPA), optimisé en *Responsive Design* pour une fluidité optimale sur ordinateurs, tablettes et smartphones.
* **Backend (Logique Métier & API) :** Propulsé par **Python / Flask** (Micro-framework REST API), gérant le routage, la sécurité et la médiation avec les services d'IA.
* **Base de Données (Persistance) :** **MongoDB Atlas** (Base NoSQL orientée documents), hébergeant un catalogue massif et structuré de **9 530 produits** issus du dataset *Amazon Electronics*.
* **Intelligence Artificielle & NLP :** Modèle de langage **LLaMA (Meta)**, orchestré à ultra-faible latence ($\le 1,5$ s) via l'infrastructure Cloud de **Groq** (puces LPU) pour assurer un support conversationnel instantané sans hallucinations.
* **Sécurité :** Chiffrement des mots de passe par l'algorithme **Bcrypt** et gestion des sessions sécurisées par jetons **JWT (JSON Web Tokens)**.

---

## ✨ Fonctionnalités Principales

1. **Catalogue Interactif & Recherche Avancée :** 
   * Consultation de plus de 9 530 références de produits électroniques.
   * Filtres dynamiques multicritères (par catégorie, prix, marques).
2. **Tunnel d'Achat & Panier Persistant :** 
   * Gestion dynamique du panier et processus de validation de commande linéaire.
   * Suivi de livraison et récapitulatif financier automatisé (TVA, sous-totaux).
3. **Assistant Virtuel Intelligent (TechStore Assistant) :** 
   * Widget de chat flottant accessible $24\text{h}/24$ et $7\text{j}/7$.
   * Traduction des besoins de l'utilisateur en langage naturel en recommandations de produits ciblées.
   * **Redirection UI Automatisée :** L'assistant est capable de piloter l'interface pour rediriger l'internaute vers la fiche produit ou la catégorie correspondante.
4. **Tableau de Bord Administrateur (Back-Office) :** 
   * Gestion complète (CRUD) des appareils, des catégories et des utilisateurs inscrits.

---

## 📊 Méthodologie et Management de Projet

* **Méthode Agile Scrum :** Développement itératif organisé en Sprints successifs (du socle technique jusqu'à la recette finale).
* **Gestion des Risques (Matrice de Pareto) :** Anticipation des goulots d'étranglement (latence du chatbot, intégrité du dataset Amazon, sécurisation des accès) avec plans de mitigation intégrés.

---



