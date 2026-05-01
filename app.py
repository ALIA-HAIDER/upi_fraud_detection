import streamlit as st
import joblib
import numpy as np


model = joblib.load("models/final_model.pkl")


st.set_page_config(page_title="UPI Fraud Detection", page_icon="🇮🇳", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton > button { 
        background-color: #1f77b4; 
        color: white; 
        font-size: 18px;
        border-radius: 8px;
        width: 100%;
        padding: 12px;
    }
    .stButton > button:hover { background-color: #155a9c; }
    </style>
""", unsafe_allow_html=True)

st.title("🇮🇳 UPI Fraud Detection AI")
st.write(" Detect suspicious UPI transactions using advanced Machine Learning algorithms.")
st.divider()


def yes_no_to_binary(choice):
    return 1 if choice == "Yes" else 0

# Transaction Details Section
st.subheader("💳 Transaction Details")
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("📊 Amount (₹)", min_value=1, value=1000)
    hour = st.slider("🕐 Transaction Hour", 0, 23, value=12)
    txn_last_10min = st.slider("⚡ Transactions in Last 10 Min", 1, 12, value=1)

with col2:
    merchant_payment = st.selectbox("🏪 Merchant Payment?", ["No", "Yes"])
    weekend = st.selectbox("📅 Weekend?", ["No", "Yes"])

st.divider()

# Device & Security Section
st.subheader("🔐 Device & Security")
col3, col4 = st.columns(2)

with col3:
    new_device = st.selectbox("📱 New Device?", ["No", "Yes"])
    device_trusted = st.selectbox("✅ Trusted Device?", ["No", "Yes"], index=1)
    kyc_verified = st.selectbox("📋 KYC Verified?", ["No", "Yes"], index=1)

with col4:
    sim_changed_recently = st.selectbox("🔄 SIM Changed Recently?", ["No", "Yes"])
    ip_risky_region = st.selectbox("⚠️ Risky IP Region?", ["No", "Yes"])

st.divider()

# Account History Section
st.subheader("📜 Account History")
col5, col6 = st.columns(2)

with col5:
    account_age_days = st.number_input("📅 Account Age (days)", min_value=1, value=365)
    upi_app_age_days = st.number_input("📱 UPI App Age (days)", min_value=1, value=200)

with col6:
    kyc_verified = st.selectbox("🆔 KYC Verified?", ["No", "Yes"], index=1, key="kyc_v2")
    device_trusted = st.selectbox("🛡️ Trusted Device?", ["No", "Yes"], index=1, key="device_t2")

st.divider()

# Receiver & Behavior Section
st.subheader("👥 Receiver & Behavior")
col7, col8 = st.columns(2)

with col7:
    new_receiver = st.selectbox("👤 New Receiver?", ["No", "Yes"])
    beneficiary_added_24h = st.selectbox("➕ Beneficiary Added in Last 24h?", ["No", "Yes"])
    failed_attempts = st.slider("❌ Failed Attempts", 0, 5, value=0)

with col8:
    city_changed = st.selectbox("🌍 City Changed?", ["No", "Yes"])
    multiple_small_txn = st.selectbox("💰 Multiple Small Transactions?", ["No", "Yes"])

st.divider()

# Prediction Section
col_btn = st.columns([1, 1, 1])
with col_btn[1]:
    predict_button = st.button("🔍 Check Fraud Status", use_container_width=True)

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
        st.error("🚨 ⚠️ FRAUDULENT TRANSACTION DETECTED ⚠️", icon="🔴")
        st.write("This transaction appears to be suspicious. Please verify with your bank immediately.")
    else:
        st.success("✅ GENUINE TRANSACTION ✅", icon="🟢")
        st.write("This transaction appears to be legitimate. Proceed safely.")