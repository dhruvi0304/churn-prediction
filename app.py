import streamlit as st
import pandas as pd
import joblib

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<styles>{f.read()}</styles>", unsafe_allow_html=True)

local_css("styles/styles.css")

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)

model = joblib.load("model.pkl")

st.title("Customer Churn Prediction")

st.write("Enter customer details")

tenure = st.number_input("Tenure (months)", min_value=0)
monthly_charges = st.number_input("Monthly Charges")
total_charges = st.number_input("Total Charges")

senior = st.selectbox("Senior Citizen", [0,1])

if st.button("Predict"):

    input_data = pd.DataFrame([{
        "gender":0,
        "SeniorCitizen":senior,
        "Partner":0,
        "Dependents":0,
        "tenure":tenure,
        "PhoneService":1,
        "MultipleLines":0,
        "InternetService":0,
        "OnlineSecurity":0,
        "OnlineBackup":0,
        "DeviceProtection":0,
        "TechSupport":0,
        "StreamingTV":0,
        "StreamingMovies":0,
        "Contract":0,
        "PaperlessBilling":1,
        "PaymentMethod":0,
        "MonthlyCharges":monthly_charges,
        "TotalCharges":total_charges
    }])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("Customer is likely to churn")
    else:
        st.success("Customer is likely to stay")