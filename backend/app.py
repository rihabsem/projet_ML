from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

svr_pipeline = joblib.load("models/gradient_boosting_burnout.pkl")

MODEL_FEATURES = [
'tenure_months',
 'salary',
 'performance_score',
 'satisfaction_score',
 'workload_score',
 'team_sentiment',
 'project_completion_rate',
 'overtime_hours',
 'training_participation',
 'collaboration_score',
 'email_sentiment',
 'slack_activity',
 'meeting_participation',
 'goal_achievement_rate',
 'stress_level',
 'role_complexity_score',
 'career_progression_score',
 'job_level_Entry',
 'job_level_Lead',
 'job_level_Manager',
 'job_level_Mid',
 'job_level_Senior']
JOB_LEVEL_CATEGORIES = ["Entry", "Lead", "Manager", "Mid", "Senior"]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received data:", data)
        joblevel = data.get("joblevel")

        row = {
            "tenure_months":             data.get("tenure_months"),
            "salary":                   data.get("salary"),
            "performance_score":        data.get("performance_score"),
            "satisfaction_score":       data.get("satisfaction_score"),
            "workload_score":           data.get("workload_score"),
            "team_sentiment":           data.get("team_sentiment"),
            "project_completion_rate":  data.get("project_completion_rate"),
            "overtime_hours":           data.get("overtime_hours"),
            "training_participation":   data.get("training_participation"),
            "collaboration_score":      data.get("collaboration_score"),
            "email_sentiment":          data.get("email_sentiment"),
            "slack_activity":           data.get("slack_activity"),
            "meeting_participation":    data.get("meeting_participation"),
            "goal_achievement_rate":    data.get("goal_achievement_rate"),
            "stress_level":             data.get("stress_level"),
            "role_complexity_score":    data.get("role_complexity_score"),
            "career_progression_score": data.get("career_progression_score"),
        }
        for category in JOB_LEVEL_CATEGORIES:
            col_name = f"job_level_{category}"
            row[col_name] = 1 if joblevel == category else 0
        input_df = pd.DataFrame([row])[MODEL_FEATURES]
        print(input_df)
        print("Input shape:", input_df.shape)
        print("Input columns:", list(input_df.columns))

        # Prédiction
        prediction = svr_pipeline.predict(input_df)[0]

        return jsonify({
            "prediction": float(prediction)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()  # prints full error in terminal
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)