# detect_anomalies.py
# -------------------------------------------------------------
# Tolgo – Risk Analytics (Anomaly Detection)
# By Fabel Sirpe
#
# Simple risk rules for fintech transactions:
# - Atypical amounts (Z-score)
# - Rapid consecutive payments (< 60 sec)
# - Frequent top-ups (rolling window)
# - Combined anomaly score
# -------------------------------------------------------------

import pandas as pd
import numpy as np


def load_data(path):
    """Load and sort transaction dataset."""
    df = pd.read_csv(path, parse_dates=["time"])
    df = df.sort_values("time")
    df["topup_flag"] = df["topup_flag"].astype(int)
    return df


def flag_amount_outliers(df, threshold=2.5):
    """Z-score anomaly detection on transaction amounts."""
    df["zscore_amount"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()
    df["amount_flag"] = (abs(df["zscore_amount"]) > threshold).astype(int)
    return df


def flag_rapid_transactions(df, seconds=60):
    """Detect consecutive transactions occurring within short intervals."""
    df["prev_time"] = df.groupby("user_id")["time"].shift(1)
    df["time_diff_sec"] = (df["time"] - df["prev_time"]).dt.total_seconds()
    df["rapid_flag"] = (df["time_diff_sec"] <= seconds).astype(int)
    return df


def flag_frequent_topups(df, window=3, min_count=3):
    """Detect repeated top-ups in rolling windows."""
    df["rolling_topups"] = (
        df.groupby("user_id")["topup_flag"]
        .rolling(window=window, min_periods=1)
        .sum()
        .reset_index(0, drop=True)
    )
    df["freq_flag"] = (df["rolling_topups"] >= min_count).astype(int)
    return df


def compute_anomaly_score(df):
    """Combine flags into a risk/anomaly score."""
    df["anomaly_score"] = df["amount_flag"] + df["rapid_flag"] + df["freq_flag"]
    df["is_anomaly"] = (df["anomaly_score"] >= 2).astype(int)
    return df


def run_detection(input_path, output_path=None):
    """Full pipeline."""
    df = load_data(input_path)
    df = flag_amount_outliers(df)
    df = flag_rapid_transactions(df)
    df = flag_frequent_topups(df)
    df = compute_anomaly_score(df)

    if output_path:
        df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    df_out = run_detection(
        input_path="../Data/transactions.csv",
        output_path="anomalies_output.csv"
    )
    print("Detection finished. Output saved as anomalies_output.csv.")
