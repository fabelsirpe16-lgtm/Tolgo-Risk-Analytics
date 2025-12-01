# generate_dataset.py
# -------------------------------------------------------------
# Generate a realistic fintech transaction dataset
# with real anomalies (amount spikes, rapid transactions,
# repeated top-ups, abnormal behaviours).
#
# Output saved into ../Data/transactions.csv
# -------------------------------------------------------------

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# ----------------------------
# 1. PARAMETERS
# ----------------------------

N_USERS = 40
N_TRANSACTIONS = 1000

payment_methods = ["card", "mobile_money", "bank_transfer"]

# ----------------------------
# 2. CREATE USERS
# ----------------------------

users = [f"user_{i}" for i in range(1, N_USERS + 1)]

# ----------------------------
# 3. GENERATE BASE TRANSACTIONS
# ----------------------------

rows = []
start_time = datetime(2024, 1, 1, 12, 0, 0)

for i in range(N_TRANSACTIONS):

    user = random.choice(users)

    # Random time offset
    time = start_time + timedelta(
        minutes=np.random.randint(0, 3000),
        seconds=np.random.randint(0, 59)
    )

    # Most transactions are normal
    amount = np.random.normal(loc=5000, scale=2000)
    amount = max(200, amount)   # minimum amount threshold

    # Random top-up flag
    topup_flag = 1 if random.random() < 0.25 else 0

    # Payment method
    method = random.choice(payment_methods)

    rows.append({
        "transaction_id": i + 1,
        "user_id": user,
        "amount": round(amount, 2),
        "time": time,
        "method": method,
        "topup_flag": topup_flag
    })

df = pd.DataFrame(rows)

# ----------------------------
# 4. INSERT REAL ANOMALIES
# ----------------------------

# 4.1 Very large payments (amount anomaly)
for idx in df.sample(5).index:
    df.loc[idx, "amount"] = np.random.randint(15000, 30000)

# 4.2 Rapid consecutive transactions (< 1 minute)
anomaly_users = df["user_id"].sample(3)

for user in anomaly_users:
    subset = df[df["user_id"] == user].sample(3).sort_values("time")
    t0 = subset.iloc[0]["time"]
    df.loc[subset.index, "time"] = [
        t0,
        t0 + timedelta(seconds=20),
        t0 + timedelta(seconds=40)
    ]

# 4.3 Repeated top-ups (3+ in short window)
for idx in df.sample(10).index:
    df.loc[idx, "topup_flag"] = 1


# ----------------------------
# 5. SORT AND SAVE
# ----------------------------

df = df.sort_values("time")

output_path = "../Data/transactions.csv"

os.makedirs("../Data", exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully → {output_path}")
print(df.head())
