import sys
import os

# Ajoute le dossier racine au PYTHONPATH (finance-ai/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# app/streamlit_app.py
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from utils.mistral_api import call_mistral

#MODEL_PATH = Path("../model/finance_pipeline.pkl")
#META_PATH = Path("../model/meta.pkl")
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent  # finance-ai/
MODEL_PATH = BASE_DIR / "model" / "finance_pipeline.pkl"
META_PATH = BASE_DIR / "model" / "meta.pkl"


st.set_page_config(page_title="AI Finance Coach", layout="centered")

st.title("AI Finance Coach — Conseiller financier personnel (prototype)")

# Load
@st.cache_resource
def load_model():
    pipeline = joblib.load(MODEL_PATH)
    meta = joblib.load(META_PATH)
    return pipeline, meta

pipeline, meta = load_model()

st.sidebar.header("Informations utilisateur")
age = st.sidebar.number_input("Âge", 18, 80, 28)
profil = st.sidebar.selectbox("Statut / profil", ["etudiant", "jeune_salarie", "fonctionnaire", "independant", "cadre"])
ville = st.sidebar.selectbox("Ville", ["Paris", "Lyon", "Marseille", "Nantes", "Toulouse", "Bordeaux", "Rennes", "Lille", "Belfort"])
salaire = st.sidebar.number_input("Revenu mensuel (€)", 300, 20000, 2000)
loyer = st.sidebar.number_input("Charges fixes - loyer (€)", 0, 5000, 700)
objectif = st.sidebar.selectbox("Objectif financier", ["économiser", "stabiliser", "investir", "acheter_voiture", "acheter_appartement"])
comportement = st.sidebar.selectbox("Comportement financier", ["économe", "normal", "dépensier"])
hab_sorties = st.sidebar.number_input("Budget sorties moyen (€)", 0, 2000, 150)
hab_courses = st.sidebar.number_input("Dépenses courses mensuelles (€)", 0, 2000, 300)

if st.button("Analyser mon profil"):
    # Construire dataframe d'entrée en respectant meta['features']
    inp = {f: 0 for f in meta["features"]}
    # assign values present
    inp.update({
        "profil": profil,
        "salaire": salaire,
        "loyer": loyer,
        "ville": ville,
        "objectif_financier": objectif,
        "comportement": comportement,
        "habitudes_sorties": hab_sorties,
        "habitudes_courses": hab_courses
    })

    X = pd.DataFrame([inp])

    pred = pipeline.predict(X)[0]
    pred = float(pred)

    st.subheader(f"Dépenses mensuelles estimées : **{int(pred):,} €**".replace(",", " "))
    st.markdown(f"- Revenu mensuel : **{salaire} €**")
    st.markdown(f"- Loyer estimé : **{loyer} €**")

    # calcul simple d'un score de risque (exemple)
    ratio_dep_to_income = pred / max(1, salaire)
    if ratio_dep_to_income > 0.9:
        risk = "Très élevé"
    elif ratio_dep_to_income > 0.7:
        risk = "Élevé"
    elif ratio_dep_to_income > 0.5:
        risk = "Modéré"
    else:
        risk = "Sain"

    st.markdown(f"**Score de pression financière (approx.)** : {risk} (dépenses / revenus = {ratio_dep_to_income:.2f})")

    # Recommandation d'épargne simple (règle 50/30/20 suggestion)
    epargne_reco = round(max(0, salaire * 0.2), 0)
    st.info(f"Suggestion rapide : épargner environ **{int(epargne_reco)} € / mois** (≈ 20% du revenu) si possible.")

    # Préparer prompt pour LLM
    prompt = f"""
Tu es un conseiller financier professionnel, clair et pragmatique.
Voici le profil utilisateur :
- Âge : {age}
- Statut : {profil}
- Ville : {ville}
- Revenu mensuel : {salaire} €
- Loyer : {loyer} €
- Comportement : {comportement}
- Habitudes sorties : {hab_sorties} €
- Habitudes courses : {hab_courses} €
- Objectif financier : {objectif}

Prédiction (modèle ML) :
- Dépenses mensuelles estimées : {int(pred)} €

GÉNÈRE :
1) Un résumé très court (2 phrases).
2) 5 conseils concrets et priorisés pour réduire les dépenses ou atteindre l'objectif.
3) Un plan d'action en 4 étapes réalisable ce mois-ci.
4) Une estimation simple du montant à épargner chaque mois pour atteindre l'objectif en 12 mois (si applicable).

Présente la réponse en français, sans jargon excessif.
    """

    with st.spinner("Demande au modèle..."):
        try:
            llm_answer = call_mistral(prompt)
        except Exception as e:
            st.error(f"Erreur API LLM : {e}")
            llm_answer = "Impossible d'appeler l'API LLM — vérifie la clé / endpoint."

    st.markdown("### Analyse personnalisée (LLM)")
    st.write(llm_answer)

    # Option : afficher debug info
    if st.checkbox("Afficher l'entrée modèle (debug)"):
        st.json(X.to_dict(orient="records")[0])
