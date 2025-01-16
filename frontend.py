import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.write('''
         # App pour le reporting des outputs des modeles data
         Cette application permet de faire des reportings graphiques
         ''')



req = requests.get("http://127.0.0.1:5000/index")

resultat = req.json()

data = pd.DataFrame(resultat, columns=["id"])

st.dataframe(data)

fig, ax = plt.subplots()
n_bins = st.number_input(
    label="Choisir un nombre de bins",
    min_value=10,
    value=20
)

ax.hist(data.id, bins=n_bins)

title=st.text_input(label="Saisir le titre du graphe")
st.title(title)
st.pyplot(fig)


st.sidebar.header("les parametres d'entrée")


# streamlit run frontend.py