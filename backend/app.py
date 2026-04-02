from flask import Flask, request, jsonify
import pandas as pd
import joblib
import traceback

app = Flask(__name__)

# Chargement du modèle
svr_pipeline = joblib.load("../models/linear_regression_burnout.pkl")

MODEL_FEATURES = [
    'tenure_months', 'salary', 'performance_score', 'satisfaction_score',
    'workload_score', 'team_sentiment', 'project_completion_rate',
    'overtime_hours', 'training_participation', 'collaboration_score',
    'email_sentiment', 'slack_activity', 'meeting_participation',
    'goal_achievement_rate', 'stress_level', 'role_complexity_score',
    'career_progression_score', 'job_level_encoded'
]

JOB_MAPPING = {"Entry": 0, "Lead": 1, "Manager": 2, "Mid": 3, "Senior": 4}


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Encodage du Job Level
        job_encoded = JOB_MAPPING.get(data.get("joblevel"), 0)

        # On construit le dictionnaire. Les scores arrivent déjà divisés par 10.
        row = {feat: data.get(feat, 0) for feat in MODEL_FEATURES if feat != "job_level_encoded"}
        row["job_level_encoded"] = job_encoded

        # Création du DataFrame
        input_df = pd.DataFrame([row])[MODEL_FEATURES]

        # Prédiction
        prediction = svr_pipeline.predict(input_df)[0]

        return jsonify({"prediction": float(prediction)})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)