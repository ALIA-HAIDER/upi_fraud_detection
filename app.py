
import streamlit as st
import joblib
import numpy as np
from huggingface_hub import hf_hub_download

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="UPI Fraud Detection",
    page_icon="🔐",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL FROM HUGGING FACE
# --------------------------------------------------

@st.cache_resource
def load_model():
    model_path = hf_hub_download(
        repo_id="Madara786/upi-fraud-models",
        filename="final_model.pkl",
        repo_type="model"
    )
    return joblib.load(model_path)


try:
    with st.spinner("Loading AI Fraud Detection Model..."):
        model = load_model()

except Exception as e:
    st.error(f"Unable to load fraud detection model: {e}")
    st.stop()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

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


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    "<div class='header-title'>UPI FRAUD DETECTION</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='header-subtitle'>Advanced AI-Powered Transaction Security</div>",
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def yes_no_to_binary(choice):
    return 1 if choice == "Yes" else 0


def section_heading(title):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #bbdefb 0%, #e1f5fe 100%);
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #1e88e5;
            margin: 12px 0;
        ">
            <h3 style="color: #0d47a1; margin: 0;">
                {title}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# 1. TRANSACTION DETAILS
# --------------------------------------------------

section_heading("TRANSACTION DETAILS - Financial Information")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input(
        "Transaction Amount (Indian Rupees)",
        min_value=1,
        value=1000
    )

    hour = st.slider(
        "Transaction Hour (24-hour format)",
        0, 23,
        value=12
    )

    txn_last_10min = st.slider(
        "Transactions in Last 10 Minutes",
        1, 12,
        value=1
    )


with col2:

    merchant_payment = st.selectbox(
        "Merchant Category Payment?",
        ["No", "Yes"]
    )

    weekend = st.selectbox(
        "Weekend Transaction?",
        ["No", "Yes"]
    )


st.divider()


# --------------------------------------------------
# 2. DEVICE & SECURITY
# --------------------------------------------------

section_heading("SECURITY - Device and Authentication Status")

col3, col4 = st.columns(2)

with col3:

    new_device = st.selectbox(
        "New Device Registration?",
        ["No", "Yes"]
    )

    device_trusted = st.selectbox(
        "Device is Trusted/Registered?",
        ["No", "Yes"],
        index=1
    )

    kyc_verified = st.selectbox(
        "KYC Verification Status?",
        ["No", "Yes"],
        index=1
    )


with col4:

    sim_changed_recently = st.selectbox(
        "SIM Card Changed Recently?",
        ["No", "Yes"]
    )

    ip_risky_region = st.selectbox(
        "IP Address from High-Risk Region?",
        ["No", "Yes"]
    )


st.divider()


# --------------------------------------------------
# 3. ACCOUNT PROFILE
# --------------------------------------------------

section_heading("ACCOUNT PROFILE - Historical Data")

col5, col6 = st.columns(2)

with col5:

    account_age_days = st.number_input(
        "Account Age in Days",
        min_value=1,
        value=365
    )

    upi_app_age_days = st.number_input(
        "UPI Application Age in Days",
        min_value=1,
        value=200
    )


with col6:

    st.info("KYC and Device Trust status are collected in the Security section above.")


st.divider()


# --------------------------------------------------
# 4. RECEIVER & BEHAVIOR
# --------------------------------------------------

section_heading("RECEIVER & BEHAVIOR - Transaction Pattern Analysis")

col7, col8 = st.columns(2)

with col7:

    new_receiver = st.selectbox(
        "New Receiver/Beneficiary?",
        ["No", "Yes"]
    )

    beneficiary_added_24h = st.selectbox(
        "Beneficiary Added in Last 24 Hours?",
        ["No", "Yes"]
    )

    failed_attempts = st.slider(
        "Failed Authentication Attempts",
        0, 5,
        value=0
    )


with col8:

    city_changed = st.selectbox(
        "User Location Changed?",
        ["No", "Yes"]
    )

    multiple_small_txn = st.selectbox(
        "Multiple Small Transactions Pattern?",
        ["No", "Yes"]
    )


st.divider()


# --------------------------------------------------
# 5. PREDICTION
# --------------------------------------------------

col_btn = st.columns([1, 1, 1])

with col_btn[1]:

    predict_button = st.button(
        "🔍 VERIFY TRANSACTION SECURITY",
        use_container_width=True
    )


if predict_button:

    # IMPORTANT:
    # Keep this feature order identical to model training.

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

    try:

        with st.spinner("Analyzing transaction..."):

            pred = model.predict(arr)

        st.divider()

        # FRAUD DETECTED

        if pred[0] == 1:

            st.markdown(
                """
                <div style="
                    background-color: #ffebee;
                    padding: 16px;
                    border-radius: 8px;
                    border-left: 4px solid #c62828;
                    margin: 12px 0;
                ">
                    <h3 style="color: #c62828; margin: 0;">
                        ⚠️ ALERT: FRAUDULENT TRANSACTION DETECTED
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <p style="color: #d32f2f; font-size: 15px;">
                    <strong>AI FRAUD ALERT:</strong>
                    This transaction has been flagged as suspicious
                    by our machine learning model. Do not proceed
                    without independently verifying the transaction
                    with your bank through its official channels.
                </p>
                """,
                unsafe_allow_html=True
            )


        # GENUINE TRANSACTION

        else:

            st.markdown(
                """
                <div style="
                    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
                    padding: 16px;
                    border-radius: 8px;
                    border-left: 4px solid #2e7d32;
                    margin: 12px 0;
                ">
                    <h3 style="color: #1b5e20; margin: 0;">
                        ✅ VERIFIED: GENUINE TRANSACTION
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <p style="color: #2e7d32; font-size: 15px;">
                    <strong>AI ASSESSMENT:</strong>
                    The machine learning model has classified
                    this transaction as legitimate based on
                    the supplied information. This does not
                    guarantee that the transaction is safe.
                </p>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:

        st.error(f"Prediction failed: {e}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align: center; color: #607d8b; font-size: 13px;">
        UPI Fraud Detection | Machine Learning-Based Security Assessment
        <br>
        Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
