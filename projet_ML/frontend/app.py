import streamlit as st
import requests

st.set_page_config(page_title="Burnout Predictor", layout="centered")
st.title("Prédiction du Risque de Burnout")

st.info(
    "Veuillez remplir les informations ci-dessous. Les scores de 1 à 10 seront automatiquement normalisés pour le modèle.")

# --- SECTION 1 : INFOS GÉNÉRALES ---
st.subheader("Profil Employé")
job_level = st.selectbox("Niveau de poste", ["Entry", "Lead", "Manager", "Mid", "Senior"])
tenure = st.number_input("Ancienneté (mois)", min_value=0, max_value=600, value=12)
salary = st.number_input("Salaire Mensuel (€)", min_value=0, max_value=20000, value=3000)

# --- SECTION 2 : ÉVALUATIONS ---
st.subheader("Indicateurs (Échelle 1-10)")

# On définit les variables et leurs labels
variables = {
    "performance_score": "Performance globale",
    "satisfaction_score": "Satisfaction au travail",
    "workload_score": "Charge de travail perçue",
    "team_sentiment": "Sentiment envers l'équipe",
    "project_completion_rate": "Taux de complétion des projets",
    "overtime_hours": "Intensité des heures supplémentaires",
    "training_participation": "Participation aux formations",
    "collaboration_score": "Niveau de collaboration",
    "email_sentiment": "Ton des échanges emails",
    "slack_activity": "Niveau d'activité Slack/Teams",
    "meeting_participation": "Engagement en réunion",
    "goal_achievement_rate": "Atteinte des objectifs",
    "stress_level": "Niveau de stress ressenti",
    "role_complexity_score": "Complexité des missions",
    "career_progression_score": "Perspectives de carrière"
}

# Création dynamique des sliders
scores_input = {}
for key, label in variables.items():
    scores_input[key] = st.slider(label, 1, 10, 5)

# --- BOUTON DE PRÉDICTION ---
if st.button("Calculer le risque maintenant", use_container_width=True):
    # Préparation du dictionnaire de données
    payload = {
        "joblevel": job_level,
        "tenure_months": float(tenure),
        "salary": float(salary)
    }

    # Division par 10 de tous les scores avant l'envoi
    for key, value in scores_input.items():
        payload[key] = value / 10.0

    try:
        response = requests.post("http://localhost:5000/predict", json=payload)
        if response.status_code == 200:
            prediction = response.json()['prediction']
            score = prediction * 100

            # Affichage du résultat avec une couleur selon le risque
            st.divider()
            if prediction > 0.7:
                st.error(f"⚠Risque Élevé : {score:.2f}%")
            elif prediction > 0.4:
                st.warning(f"Risque Modéré : {score:.2f}%")
            else:
                st.success(f" Risque Faible : {score:.2f}%")
        else:
            st.error(f"Erreur serveur : {response.json().get('error')}")
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")