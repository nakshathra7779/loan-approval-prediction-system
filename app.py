import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Smart Loan Advisor",
    page_icon="🏦",
    layout="centered"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    border: none;
    background: #2563EB;
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #1D4ED8;
}

div[data-testid="stMetric"] {
    background-color: #111827;
    padding: 10px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================

model = joblib.load("loan_model.pkl")
scaler = joblib.load("scaler.pkl")

# =========================
# HEADER
# =========================

st.markdown("""
<div style="
background: linear-gradient(135deg,#0F172A,#2563EB);
padding:35px;
border-radius:20px;
text-align:center;
margin-bottom:20px;
">

<h1 style="color:white;">
🏦 Smart Loan Advisor
</h1>

<p style="color:#dbeafe;font-size:18px;">
Check your loan eligibility instantly
</p>

</div>
""", unsafe_allow_html=True)

# =========================
# PERSONAL DETAILS
# =========================

st.subheader("👤 Personal Information")

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=25
)

income = st.number_input(
    "Annual Income (₹)",
    min_value=1.0,
    value=500000.0
)

emp_length = st.number_input(
    "Employment Length (Years)",
    min_value=0.0,
    value=2.0
)

credit_history = st.number_input(
    "Credit History Length",
    min_value=0,
    value=3
)

home = st.selectbox(
    "Home Ownership",
    ["OTHER", "OWN", "RENT"]
)

default = st.selectbox(
    "Previous Default",
    ["N", "Y"]
)

st.markdown("---")

# =========================
# LOAN DETAILS
# =========================

st.subheader("💰 Loan Information")

loan_amount = st.number_input(
    "Loan Amount (₹)",
    min_value=0.0,
    value=100000.0
)

interest_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    value=8.5
)

grade = st.selectbox(
    "Loan Grade",
    ["A","B","C","D","E","F","G"]
)

intent = st.selectbox(
    "Loan Purpose",
    [
        "EDUCATION",
        "HOMEIMPROVEMENT",
        "MEDICAL",
        "PERSONAL",
        "VENTURE"
    ]
)

st.markdown("---")

# =========================
# SUMMARY
# =========================

st.subheader("📊 Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Income", f"₹{income:,.0f}")
c2.metric("Loan", f"₹{loan_amount:,.0f}")
c3.metric("Interest", f"{interest_rate}%")
c4.metric("Grade", grade)

# =========================
# GRADE MAP
# =========================

grade_map = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7
}

# =========================
# PREDICT
# =========================

if st.button("🚀 Check Eligibility"):

    # Derived Features
    loan_percent_income = loan_amount / income if income > 0 else 0
    income_to_loan_ratio = income / loan_amount if loan_amount > 0 else 0

    # Input Data
    sample = pd.DataFrame({

        'person_age':[age],
        'person_income':[income],
        'person_emp_length':[emp_length],
        'loan_grade':[grade_map[grade]],
        'loan_amnt':[loan_amount],
        'loan_int_rate':[interest_rate],
        'loan_percent_income':[loan_percent_income],
        'cb_person_default_on_file':[1 if default == "Y" else 0],
        'cb_person_cred_hist_length':[credit_history],
        'income_to_loan_ratio':[income_to_loan_ratio],

        'person_home_ownership_OTHER':[1 if home == "OTHER" else 0],
        'person_home_ownership_OWN':[1 if home == "OWN" else 0],
        'person_home_ownership_RENT':[1 if home == "RENT" else 0],

        'loan_intent_EDUCATION':[1 if intent == "EDUCATION" else 0],
        'loan_intent_HOMEIMPROVEMENT':[1 if intent == "HOMEIMPROVEMENT" else 0],
        'loan_intent_MEDICAL':[1 if intent == "MEDICAL" else 0],
        'loan_intent_PERSONAL':[1 if intent == "PERSONAL" else 0],
        'loan_intent_VENTURE':[1 if intent == "VENTURE" else 0]
    })
    
    sample = sample[scaler.feature_names_in_]

    sample_scaled = scaler.transform(sample)


    prediction = model.predict(sample_scaled)

    # Risk Score
    probability = model.predict_proba(sample_scaled)[0]
    risk_score = probability[1] * 100

    st.markdown("### 📈 Risk Assessment")

    st.progress(int(risk_score))

    if risk_score < 30:
        st.success(f"🟢 Low Risk • {risk_score:.1f}%")

    elif risk_score < 70:
        st.warning(f"🟡 Medium Risk • {risk_score:.1f}%")

    else:
        st.error(f"🔴 High Risk • {risk_score:.1f}%")

    # Final Result
    if prediction[0] == 0:

        st.markdown("""
        <div style="
        background: linear-gradient(135deg,#16A34A,#22C55E);
        padding:30px;
        border-radius:20px;
        text-align:center;
        margin-top:20px;
        ">

        <h1 style="color:white;">
        ✅ Loan Approved
        </h1>

        <p style="color:white;font-size:18px;">
        Congratulations! Your application meets the eligibility criteria.
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div style="
        background: linear-gradient(135deg,#DC2626,#EF4444);
        padding:30px;
        border-radius:20px;
        text-align:center;
        margin-top:20px;
        ">

        <h1 style="color:white;">
        ❌ Loan Rejected
        </h1>

        <p style="color:white;font-size:18px;">
        Your application does not meet the eligibility criteria.
        </p>

        </div>
        """, unsafe_allow_html=True)