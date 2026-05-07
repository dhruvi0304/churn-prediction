import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.hero {
    background: linear-gradient(135deg, #1f4e79, #2e86c1);
    padding: 35px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.hero h1 {
    font-size: 46px;
    margin-bottom: 10px;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.metric-card {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}
.risk-high {
    background-color: #ffe6e6;
    color: #b00020;
    padding: 22px;
    border-radius: 16px;
    font-size: 22px;
    font-weight: bold;
}
.risk-low {
    background-color: #e6f7ec;
    color: #137333;
    padding: 22px;
    border-radius: 16px;
    font-size: 22px;
    font-weight: bold;
}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

model = joblib.load("model.pkl")

st.markdown("""
<div class="hero">
    <h1>📊 Customer Churn Prediction</h1>
    <p>Predict customer churn risk using a machine learning model.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Enter Customer Details")

    col1, col2 = st.columns(2)

    with col1:
        tenure = st.number_input("Tenure (months)", min_value=0, value=12)
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=70.0)
        total_charges = st.number_input("Total Charges", min_value=0.0, value=850.0)

    with col2:
        senior = st.selectbox("Senior Citizen", [0, 1])
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    predict_button = st.button("Predict Churn Risk")
    st.markdown('</div>', unsafe_allow_html=True)

contract_map = {
    "Month-to-month": 0,
    "One year": 1,
    "Two year": 2
}

internet_map = {
    "DSL": 0,
    "Fiber optic": 1,
    "No": 2
}

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Project Summary")
    st.write("This app uses a Random Forest model trained on telecom customer data.")
    st.write("It predicts whether a customer is likely to churn based on customer account information.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Model Accuracy", "79.84%")
    st.markdown("</div>", unsafe_allow_html=True)

if predict_button:

    input_data = pd.DataFrame([{
        "gender": 0,
        "SeniorCitizen": senior,
        "Partner": 0,
        "Dependents": 0,
        "tenure": tenure,
        "PhoneService": 1,
        "MultipleLines": 0,
        "InternetService": internet_map[internet],
        "OnlineSecurity": 0,
        "OnlineBackup": 0,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "Contract": contract_map[contract],
        "PaperlessBilling": 1,
        "PaymentMethod": 0,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100

    st.markdown("---")
    st.subheader("Prediction Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric("Churn Probability", f"{probability:.2f}%")

    with result_col2:
        if prediction == 1:
            st.metric("Prediction", "Likely to Churn")
        else:
            st.metric("Prediction", "Likely to Stay")

    with result_col3:
        if probability >= 70:
            st.metric("Risk Level", "High")
        elif probability >= 40:
            st.metric("Risk Level", "Medium")
        else:
            st.metric("Risk Level", "Low")

    if prediction == 1:
        st.markdown(
            '<div class="risk-high">⚠️ High churn risk detected. Recommended action: offer retention discount or improved support.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="risk-low">✅ Low churn risk. Customer is likely to stay.</div>',
            unsafe_allow_html=True
        )