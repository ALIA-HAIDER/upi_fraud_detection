import pandas as pd
import numpy as np



np.random.seed(42)
n = 50000


data = pd.DataFrame({
    "amount": np.random.randint(10, 100000, n),                 # ₹10 to ₹1 lakh
    "hour": np.random.randint(0, 24, n),
    "city_changed": np.random.binomial(1, 0.15, n),            # 15%
    "new_device": np.random.binomial(1, 0.18, n),              # 18%
    "failed_attempts": np.random.randint(0, 6, n),
    "new_receiver": np.random.binomial(1, 0.22, n),
    "txn_last_10min": np.random.randint(1, 12, n),
    "merchant_payment": np.random.binomial(1, 0.45, n),
    "weekend": np.random.binomial(1, 0.28, n),
    "account_age_days": np.random.randint(1, 2500, n),
    "kyc_verified": np.random.binomial(1, 0.82, n),
    "upi_app_age_days": np.random.randint(1, 1500, n),
    "device_trusted": np.random.binomial(1, 0.75, n),
    "beneficiary_added_24h": np.random.binomial(1, 0.12, n),
    "multiple_small_txn": np.random.binomial(1, 0.18, n),
    "ip_risky_region": np.random.binomial(1, 0.08, n),
    "sim_changed_recently": np.random.binomial(1, 0.07, n)
})


risk = np.zeros(n)

risk += (data["amount"] > 30000) * 2
risk += (data["amount"] > 70000) * 2

risk += ((data["hour"] >= 0) & (data["hour"] <= 4)) * 2

# Behavioral anomalies
risk += data["city_changed"] * 2
risk += data["new_device"] * 2
risk += (data["failed_attempts"] >= 3) * 3
risk += data["new_receiver"] * 2
risk += (data["txn_last_10min"] >= 6) * 2


risk += data["multiple_small_txn"] * 2
risk += data["beneficiary_added_24h"] * 2


risk += data["ip_risky_region"] * 3
risk += data["sim_changed_recently"] * 3

risk += (data["account_age_days"] < 30) * 2
risk += (data["upi_app_age_days"] < 15) * 2
risk += (data["kyc_verified"] == 0) * 2
risk += (data["device_trusted"] == 0) * 2

risk -= data["merchant_payment"] * 3


risk += data["weekend"] * 1


noise = np.random.normal(0, 1.5, n)
final_score = risk + noise


data["fraud"] = (final_score >= 8).astype(int)


data.to_csv("data/upi_bank_grade_data.csv", index=False)

print("✅ Bank-grade UPI fraud dataset created!")
print("Saved as: data/upi_bank_grade_data.csv")
print(data["fraud"].value_counts())