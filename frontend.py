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
st.title("Reporting des Ventes Immobilières en Volume")

# Option pour sélectionner le type de visualisation
visualization_type = st.sidebar.selectbox("Choisissez le type de visualisation", ("Histogramme", "Courbe", "Camembert"))

# Sélection du filtre : Semaine ou Mois
filter_by = st.sidebar.radio("Filtrer par", ("Semaine", "Mois", "Type_bien"))

# Sous-filtres pour la sélection de plages de semaines ou de mois
if filter_by == "Semaine":
    min_week, max_week = st.sidebar.select_slider("Sélectionnez la plage de semaines", options=sorted(data["semaine"].unique()), value=(min(data["semaine"]), max(data["semaine"])))
    filtered_df = data[(data["semaine"] >= min_week) & (data["semaine"] <= max_week)]
    group_data = filtered_df.groupby("semaine").sum().reset_index()
    #group_data = data.groupby("semaine").sum().reset_index()
elif filter_by == "Mois":
    #min_month, max_month = st.sidebar.slider("Sélectionnez la plage de mois", min_value=min(data["mois"]), max_value=max(data["mois"]), value=(min(data["mois"]), max(data["mois"])))
    min_month, max_month = st.sidebar.select_slider("Sélectionnez la plage de mois", options=sorted(data["mois"].unique()), value=(min(data["mois"]), max(data["mois"])))
    filtered_df = data[(data["mois"] >= min_month) & (data["mois"] <= max_month)]
    group_data = filtered_df.groupby("mois").sum().reset_index()
    #group_data = data.groupby("mois").sum().reset_index()
else:
    group_data = data.groupby("type_bien").sum().reset_index()


# Visualisation des données
if visualization_type == "Histogramme":
    st.header(f"Histogramme des ventes par {filter_by.lower()}")
    fig, ax = plt.subplots()
    sns.barplot(x=filter_by.lower(), y='nb_vente', data=group_data, ax=ax, label='Volume des ventes')
    st.pyplot(fig)

elif visualization_type == "Courbe":
    st.header(f"Courbe des ventes par {filter_by.lower()}")
    fig, ax = plt.subplots()
    sns.lineplot(x=filter_by.lower(), y='nb_vente', data=group_data, ax=ax, label='Volume des ventes')
    st.pyplot(fig)

elif visualization_type == "Camembert":
    st.header("Répartition des ventes par type de bien")
    fig, ax = plt.subplots()
    data.groupby('type_bien').sum()['nb_vente'].plot.pie(autopct='%1.1f%%', ax=ax, label='Volume des ventes')
    st.pyplot(fig)


# Visualisation supplémentaire : Courbe sur le CA
st.header(f"Courbe du chiffre d'affaires par {filter_by.lower()}")
fig, ax = plt.subplots()
sns.lineplot(x=filter_by.lower(), y='ca_vente', data=group_data, ax=ax, label='Chiffre d\'Affaires')
ax.set_ylabel('CA Vente')
st.pyplot(fig)


st.header(f"Histogramme du chiffre d'affaires par {filter_by.lower()}")
fig, ax = plt.subplots()
sns.barplot(x=filter_by.lower(), y='ca_vente', data=group_data, ax=ax, label='Chiffre d\'Affaires')
ax.set_ylabel('CA Vente')
st.pyplot(fig)


# Afficher le tableau de données
st.header("Tableau des données")
st.dataframe(data)

# Autres options de reporting
st.header("Autres Analyses")
st.write("Sélectionnez différentes options dans la barre latérale pour explorer les données sous divers angles.")

# Filtres supplémentaires
st.sidebar.header("Filtres supplémentaires")
selected_region = st.sidebar.multiselect("Sélectionnez la region", options=data["region"].unique(), default=data["region"].unique())
filtered_df = data[data["region"].isin(selected_region)]
st.dataframe(filtered_df)







# streamlit run frontend.py