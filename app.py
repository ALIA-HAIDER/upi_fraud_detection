import streamlit as st
import joblib
import numpy as np


model = joblib.load("models/final_model.pkl")


st.set_page_config(page_title="UPI Fraud Detection", page_icon=None, layout="wide")

# Custom CSS - Light Blue and White Theme
st.markdown("""
    <style>
    .main { 
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
    }
    .stButton > button { 
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        color: white; 
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px;
        width: 100%;
        padding: 12px;
        border: none;
        box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
    }
    .stButton > button:hover { 
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.4);
    }
    .header-title {
        color: #0d47a1;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }
    .header-subtitle {
        color: #1565c0;
        text-align: center;
        font-size: 14px;
        margin-bottom: 16px;
    }
    .section-card {
        background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%);
        padding: 16px;
        border-radius: 8px;
        border-left: 4px solid #1e88e5;
        margin: 12px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-title'>NPCI UPI FRAUD DETECTION</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'> Advanced AI-Powered Transaction Security</div>", unsafe_allow_html=True)
st.divider()

def yes_no_to_binary(choice):
    return 1 if choice == "Yes" else 0

# Transaction Details Section
st.markdown("<div style='background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%); padding: 12px; border-radius: 8px; border-left: 4px solid #1e88e5; margin: 12px 0;'><h3 style='color: #0d47a1; margin: 0;'>TRANSACTION DETAILS - Financial Information</h3></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount (Indian Rupees)", min_value=1, value=1000)
    hour = st.slider("Transaction Hour (24-hour format)", 0, 23, value=12)
    txn_last_10min = st.slider("Transactions in Last 10 Minutes", 1, 12, value=1)

with col2:
    merchant_payment = st.selectbox("Merchant Category Payment?", ["No", "Yes"])
    weekend = st.selectbox("Weekend Transaction?", ["No", "Yes"])

st.divider()

# Device & Security Section
st.markdown("<div style='background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%); padding: 12px; border-radius: 8px; border-left: 4px solid #1e88e5; margin: 12px 0;'><h3 style='color: #0d47a1; margin: 0;'>SECURITY - Device and Authentication Status</h3></div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    new_device = st.selectbox("New Device Registration?", ["No", "Yes"])
    device_trusted = st.selectbox("Device is Trusted/Registered?", ["No", "Yes"], index=1)
    kyc_verified = st.selectbox("KYC Verification Status?", ["No", "Yes"], index=1)

with col4:
    sim_changed_recently = st.selectbox("SIM Card Changed Recently?", ["No", "Yes"])
    ip_risky_region = st.selectbox("IP Address from High-Risk Region?", ["No", "Yes"])

st.divider()

# Account History Section
st.markdown("<div style='background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%); padding: 12px; border-radius: 8px; border-left: 4px solid #1e88e5; margin: 12px 0;'><h3 style='color: #0d47a1; margin: 0;'>ACCOUNT PROFILE - Historical Data</h3></div>", unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    account_age_days = st.number_input("Account Age in Days", min_value=1, value=365)
    upi_app_age_days = st.number_input("UPI Application Age in Days", min_value=1, value=200)

with col6:
    kyc_verified = st.selectbox("Complete KYC Verification?", ["No", "Yes"], index=1, key="kyc_v2")
    device_trusted = st.selectbox("Device Trust Status?", ["No", "Yes"], index=1, key="device_t2")

st.divider()

# Receiver & Behavior Section
st.markdown("<div style='background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%); padding: 12px; border-radius: 8px; border-left: 4px solid #1e88e5; margin: 12px 0;'><h3 style='color: #0d47a1; margin: 0;'>RECEIVER & BEHAVIOR - Transaction Pattern Analysis</h3></div>", unsafe_allow_html=True)
col7, col8 = st.columns(2)

with col7:
    new_receiver = st.selectbox("New Receiver/Beneficiary?", ["No", "Yes"])
    beneficiary_added_24h = st.selectbox("Beneficiary Added in Last 24 Hours?", ["No", "Yes"])
    failed_attempts = st.slider("Failed Authentication Attempts", 0, 5, value=0)

with col8:
    city_changed = st.selectbox("User Location Changed?", ["No", "Yes"])
    multiple_small_txn = st.selectbox("Multiple Small Transactions Pattern?", ["No", "Yes"])

st.divider()

# Prediction Section
col_btn = st.columns([1, 1, 1])
with col_btn[1]:
    predict_button = st.button("VERIFY TRANSACTION SECURITY", use_container_width=True)

if predict_button:
    # Convert Yes/No to binary
    arr = np.array([[
        amount,
        hour,
        yes_no_to_binary(city_changed),
        yes_no_to_binary(new_device),
        failed_attempts,
        yes_no_to_binary(new_receiver),
        txn_last_10min,
        yes_no_to_binary(merchant_payment),
        yes_no_to_binary(weekend),
        account_age_days,
        yes_no_to_binary(kyc_verified),
        upi_app_age_days,
        yes_no_to_binary(device_trusted),
        yes_no_to_binary(beneficiary_added_24h),
        yes_no_to_binary(multiple_small_txn),
        yes_no_to_binary(ip_risky_region),
        yes_no_to_binary(sim_changed_recently)
    ]])

    pred = model.predict(arr)

    st.divider()
    if pred[0] == 1:
        st.markdown("<div style='background-color: #ffebee; padding: 16px; border-radius: 8px; border-left: 4px solid #c62828; margin: 12px 0;'><h3 style='color: #c62828; margin: 0;'>ALERT: FRAUDULENT TRANSACTION DETECTED</h3></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #d32f2f; font-size: 15px;'><strong>NPCI FRAUD ALERT:</strong> This transaction has been flagged as suspicious by our AI system. Please verify with your bank immediately or call the UPI helpline before proceeding.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%); padding: 16px; border-radius: 8px; border-left: 4px solid #2e7d32; margin: 12px 0;'><h3 style='color: #1b5e20; margin: 0;'>VERIFIED: GENUINE TRANSACTION</h3></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #2e7d32; font-size: 15px;'><strong>NPCI VERIFICATION:</strong> This transaction has passed all security checks. The transaction appears to be legitimate. You may proceed safely.</p>", unsafe_allow_html=True)