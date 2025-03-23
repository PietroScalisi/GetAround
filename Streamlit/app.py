import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="GetAround Dashboard", layout="wide")

# Titre et introduction
st.title("Analyse des Locations GetAround")
st.markdown("""
Cette dashboard permet d'analyser l'impact du délai minimum entre deux locations et leur prix de location.
""")

# Chargement des données CSV
@st.cache_data
def charger_donnees_csv():
    """
    Charge les données CSV et retourne un DataFrame
    """
    donnees_csv = pd.read_csv("get_around_pricing_project.csv", encoding="utf_8")
    return donnees_csv

# Chargement des données Excel
@st.cache_data
def charger_donnees_excel():
    """
    Charge les données Excel et retourne un DataFrame
    """
    donnees_excel = pd.read_excel(r"C:\Users\pietr\OneDrive\Desktop\FullStack\GetAround\API\get_around_delay_analysis.xlsx")
    return donnees_excel

# Charger les données des deux fichiers
donnees_csv = charger_donnees_csv()
donnees_excel = charger_donnees_excel()

# Aperçu des données
st.subheader("Aperçu des Données prix de location")
st.dataframe(donnees_csv.head())
st.write(f"Nombre de lignes dans le dataset de prix : **{len(donnees_csv)}**")

st.subheader("Aperçu des Données d'analyse")
st.dataframe(donnees_excel.head())
st.write(f"Nombre de lignes dans le dataset d'analyse : **{len(donnees_excel)}**")

# Utiliser les données réelles de retard et éliminer les valeurs aberrantes
donnees_retard = donnees_excel[['delay_at_checkout_in_minutes']].copy()
Q1 = donnees_retard['delay_at_checkout_in_minutes'].quantile(0.25)
Q3 = donnees_retard['delay_at_checkout_in_minutes'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
donnees_retard = donnees_retard[(donnees_retard['delay_at_checkout_in_minutes'] >= lower_bound) & 
                                (donnees_retard['delay_at_checkout_in_minutes'] <= upper_bound)]

donnees_retard['impact_location_suivante'] = donnees_retard['delay_at_checkout_in_minutes'] > 0
donnees_retard['annulation_location_suivante'] = donnees_retard['delay_at_checkout_in_minutes'] > 60

# Paramètres de seuil
st.sidebar.header("Paramètres")
seuil_minutes = st.sidebar.slider("Seuil de délai minimum (minutes)", 0, 120, 30, 5)
scope = st.sidebar.radio("Portée de la fonctionnalité", ["Toutes les voitures", "Seulement Connect"])

# Analyse des retards
st.subheader("Analyse des Retards")
col1, col2 = st.columns(2)

# Graphique : Distribution des Retards
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(donnees_retard['delay_at_checkout_in_minutes'], bins=20, kde=True, ax=ax)
    ax.axvline(x=seuil_minutes, color='red', linestyle='--', label=f'Seuil: {seuil_minutes} min')
    ax.set_title("Distribution des Retards (sans valeurs aberrantes)")
    ax.set_xlabel("Retard (minutes)")
    ax.set_ylabel("Fréquence")
    ax.legend()
    st.pyplot(fig)

# Impact sur les revenus et annulations
impact_revenus = (donnees_retard['delay_at_checkout_in_minutes'] < seuil_minutes).mean() * 100
impact_annulations = (donnees_retard['annulation_location_suivante']).mean() * 100
locations_affectees = (donnees_retard['delay_at_checkout_in_minutes'] >= seuil_minutes).sum()

with col2:
    st.metric("Impact sur les Revenus", f"{impact_revenus:.1f}% préservés")
    st.metric("Taux d'Annulations Évitées", f"{impact_annulations:.1f}%")
    st.metric("Locations Affectées par le Seuil", locations_affectees)

# Nombre de voitures par marque
st.subheader("Nombre de Voitures par Marque")
voitures_par_marque = donnees_csv['model_key'].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
voitures_par_marque.plot(kind='bar', ax=ax)
ax.set_title("Nombre de Voitures par Marque")
ax.set_xlabel("Marque")
ax.set_ylabel("Nombre de Voitures")
plt.xticks(rotation=45, ha='right')

# Ajout du nombre exact de voitures au-dessus de chaque barre
for i, v in enumerate(voitures_par_marque):
    ax.text(i, v, str(v), ha='center', va='bottom')

st.pyplot(fig)


# Prix moyen par marque
st.subheader("Prix Moyen par Marque")
prix_moyen = donnees_csv.groupby('model_key')['rental_price_per_day'].mean().sort_values(ascending=False)
moyenne_globale = donnees_csv['rental_price_per_day'].mean()

fig, ax = plt.subplots(figsize=(12, 6))
prix_moyen.plot(kind='bar', ax=ax)
ax.axhline(y=moyenne_globale, color='red', linestyle='--', label=f'Moyenne: {moyenne_globale:.2f}€')
ax.set_title("Prix Moyen de Location par Marque")
ax.set_xlabel("Marque")
ax.set_ylabel("Prix Moyen (€)")
plt.xticks(rotation=45, ha='right')
ax.legend()
st.pyplot(fig)


# Distribution des Prix de Location
st.subheader("Distribution des Prix de Location Journaliers")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(donnees_csv["rental_price_per_day"], bins=30, kde=True, ax=ax)
ax.set_title("Distribution des Prix de Location Journaliers")
ax.set_xlabel("Prix (€)")
ax.set_ylabel("Fréquence")
st.pyplot(fig)

# Relation entre Kilométrage et Prix de Location
st.subheader("Relation entre Kilométrage et Prix de Location")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=donnees_csv, x="mileage", y="rental_price_per_day", hue="model_key", alpha=0.7, ax=ax)
ax.set_title("Relation entre Kilométrage et Prix de Location")
ax.set_xlabel("Kilométrage")
ax.set_ylabel("Prix (€)")
st.pyplot(fig)

# Conclusion et recommandations
st.subheader("Recommandations")
st.write(f"""
Basé sur l'analyse des données (sans valeurs aberrantes):

1. Cette mesure affecterait **{locations_affectees}** locations sur notre échantillon.
2. Impact estimé sur les revenus: **{100-impact_revenus:.1f}%** de réduction potentielle.

Recommandation: {'Implémenter pour toutes les voitures' if scope == "Toutes les voitures" else 'Implémenter uniquement pour les voitures Connect'} avec un délai de {seuil_minutes} minutes.
""")
