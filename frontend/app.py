import streamlit as st
import requests

st.title("Burnout Risk Prediction")
with st.form("form_id"):
    joblevel = st.selectbox(
        "Job Level",
        ['Choose a value',"Mid","Manager","Entry","Senior","Lead"]
    )
    tenure_months = st.number_input("Tenure month")
    salary = st.number_input("Salary")
    performance_score = st.number_input("Performance Score")
    satisfaction_score = st.number_input("Satisfaction Score")  
    workload_score = st.number_input("Workload Score")
    team_sentiment = st.number_input("Team Sentiment")
    project_completion_rate = st.number_input("Project Completion Rate")
    overtime_hours = st.number_input("Overtime Hours")
    training_participation = st.number_input("Traning Participation")
    collaboration_score = st.number_input("Collaboration Score")
    email_sentiment = st.number_input("Email Sentiment")
    slack_activity = st.number_input("Slack Activity")
    meeting_participation = st.number_input("Meeting Participation")
    goal_achievement_rate = st.number_input("Goal Achievement Rate")
    stress_level = st.number_input("Stress Level")
    role_complexity_score = st.number_input("Role Complexity Score")
    career_progression_score = st.number_input("Career Progression Score")
    submit = st.form_submit_button("Submit")
if submit:
    if any(v == 0 for v in [
        tenure_months, salary, performance_score,satisfaction_score,workload_score,
        team_sentiment,project_completion_rate,training_participation,
        collaboration_score, email_sentiment, slack_activity, meeting_participation,
        goal_achievement_rate, stress_level, role_complexity_score, career_progression_score
    ] or (u == "Choose a value" for u in ["jobelevel", "departement"])):
        st.error("Veuillez remplir tous les champs")


    else:
        payload = {
            "joblevel": joblevel,
            "tenure_months": tenure_months,
            "salary": salary,
            "performance_score": performance_score,
            "satisfaction_score": satisfaction_score,
            "workload_score": workload_score,
            "team_sentiment": team_sentiment,
            "project_completion_rate": project_completion_rate,
            "overtime_hours": overtime_hours,
            "training_participation": training_participation,
            "collaboration_score": collaboration_score,
            "email_sentiment": email_sentiment,
            "slack_activity": slack_activity,
            "meeting_participation": meeting_participation,
            "goal_achievement_rate": goal_achievement_rate,
            "stress_level": stress_level,
            "role_complexity_score": role_complexity_score,
            "career_progression_score": career_progression_score
        }

        try:
            response = requests.post("http://localhost:5000/predict", json=payload)

            if response.status_code == 200:
                result = response.json()
                st.success(f"Prediction: {result['prediction']}")
            else:
                st.error("Backend error")

        except Exception as e:
            st.error(f"Connection error: {e}")


