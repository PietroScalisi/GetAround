# Importation des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration pour les graphiques (utilisation d'un style Seaborn prédefini)
sns.set_style('darkgrid')  # Utilisation du style 'darkgrid'
sns.set(font_scale=1.2)

# Chargement des données
donnees = pd.read_csv("get_around_pricing_project.csv", encoding="utf_8")

# Affichage des premières lignes pour comprendre la structure
print("Aperçu des données:")
print(donnees.head())

# Informations générales sur le dataset
print("\nInformations sur le dataset:")
print(donnees.info())

# Statistiques descriptives
print("\nStatistiques descriptives:")
print(donnees.describe())

# Analyse des valeurs manquantes
print("\nValeurs manquantes par colonne:")
print(donnees.isnull().sum())

# Visualisation de la distribution des prix de location
plt.figure(figsize=(10, 6))
sns.histplot(donnees["rental_price_per_day"], bins=30, kde=True)
plt.title("Distribution des Prix de Location Journaliers")
plt.xlabel("Prix (€)")
plt.ylabel("Fréquence")
plt.savefig("distribution_prix.png")

# Analyse des prix moyens par marque
prix_moyen_par_marque = donnees.groupby("model_key")["rental_price_per_day"].mean().sort_values(ascending=False)
print("\nPrix moyen par marque:")
print(prix_moyen_par_marque)

# Visualisation des prix moyens par marque
plt.figure(figsize=(12, 6))
prix_moyen_par_marque.plot(kind="bar")
plt.title("Prix Moyen de Location par Marque")
plt.xlabel("Marque")
plt.ylabel("Prix Moyen (€)")
plt.savefig("prix_par_marque.png")

# Relation entre kilométrage et prix
plt.figure(figsize=(10, 6))
sns.scatterplot(data=donnees, x="mileage", y="rental_price_per_day", hue="model_key", alpha=0.7)
plt.title("Relation entre Kilométrage et Prix de Location")
plt.xlabel("Kilométrage")
plt.ylabel("Prix (€)")
plt.savefig("kilometrage_vs_prix.png")

print("\nAnalyse terminée. Les graphiques ont été sauvegardés.")

