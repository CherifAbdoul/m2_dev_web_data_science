import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.write('''
         # App pour le reporting des outputs des modeles data
         Cette application permet de faire des reportings graphiques
         ''')



req = requests.get("http://127.0.0.1:5000/index")

resultat = req.json()

data = pd.DataFrame(resultat, columns=["id", "type_bien", "pieces", "region", "nb_vente", "ca_vente", "semaine", "mois"])

# Configuration de la page Streamlit
st.title("Reporting des Ventes Immobilières")

# Option pour sélectionner le type de visualisation
visualization_type = st.sidebar.selectbox("Choisissez le type de visualisation", ("Histogramme", "Courbe", "Camembert"))

# Sélection du filtre : Semaine ou Mois
filter_by = st.sidebar.radio("Filtrer par", ("Semaine", "Mois", "Type_bien"))

# Groupement des données
if filter_by == "Semaine":
    group_data = data.groupby("semaine").sum().reset_index()
elif filter_by == "Mois":
    group_data = data.groupby("mois").sum().reset_index()
else:
    group_data = data.groupby("type_bien").sum().reset_index()

# Visualisation des données
if visualization_type == "Histogramme":
    st.header(f"Histogramme des ventes par {filter_by.lower()}")
    fig, ax = plt.subplots()
    sns.barplot(x=filter_by.lower(), y='nb_vente', data=group_data, ax=ax)
    st.pyplot(fig)

elif visualization_type == "Courbe":
    st.header(f"Courbe des ventes par {filter_by.lower()}")
    fig, ax = plt.subplots()
    sns.lineplot(x=filter_by.lower(), y='nb_vente', data=group_data, ax=ax)
    st.pyplot(fig)

elif visualization_type == "Camembert":
    st.header("Répartition des ventes par type de bien")
    fig, ax = plt.subplots()
    data.groupby('type_bien').sum()['nb_vente'].plot.pie(autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

# Afficher le tableau de données
st.header("Tableau des données")
st.dataframe(data)

# Autres options de reporting
st.header("Autres Analyses")
st.write("Sélectionnez différentes options dans la barre latérale pour explorer les données sous divers angles.")

# Filtres supplémentaires
st.sidebar.header("Filtres supplémentaires")
selected_region = st.sidebar.multiselect("Sélectionnez la région", options=data["region"].unique(), default=data["region"].unique())
filtered_df = data[data["region"].isin(selected_region)]
st.dataframe(filtered_df)







# streamlit run frontend.py