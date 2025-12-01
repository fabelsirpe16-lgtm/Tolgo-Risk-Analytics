# utils.py
# -------------------------------------------------------------
# Tolgo – Risk Analytics Utility Functions
# By Fabel Sirpe
#
# This module provides commonly used analytical and business KPIs
# for fintech-style transaction datasets.
#
# Functions include:
# - revenue calculations
# - user metrics
# - top performers
# - daily & hourly KPIs
# - simple cohort analysis
# -------------------------------------------------------------

import pandas as pd
import numpy as np


# -------------------------------------------------------------
# BASIC AGGREGATIONS
# -------------------------------------------------------------

def total_revenue(df):
    """Sum of all amounts."""
    return df["amount"].sum()


def average_transaction_value(df):
    """Mean basket size."""
    return df["amount"].mean()


def daily_revenue(df):
    """Revenue grouped by date."""
    df["date"] = df["time"].dt.date
    return df.groupby("date")["amount"].sum().reset_index()


def hourly_volume(df):
    """Transaction volume per hour of day."""
    df["hour"] = df["time"].dt.hour
    return df.groupby("hour")["transaction_id"].count().reset_index(name="volume")


# -------------------------------------------------------------
# USER METRICS
# -------------------------------------------------------------

def unique_users(df):
    """Total number of unique users."""
    return df["user_id"].nunique()


def user_total_amount(df):
    """Total spending per user."""
    return df.groupby("user_id")["amount"].sum().reset_index()


def user_transaction_count(df):
    """Transaction frequency per user."""
    return df.groupby("user_id")["transaction_id"].count().reset_index(name="tx_count")


def top_users_by_spending(df, n=5):
    """Top N users by amount spent."""
    users = user_total_amount(df)
    return users.sort_values("amount", ascending=False).head(n)


def top_users_by_volume(df, n=5):
    """Top N users by transaction count."""
    users = user_transaction_count(df)
    return users.sort_values("tx_count", ascending=False).head(n)


# -------------------------------------------------------------
# RECHARGE / TOP-UP ANALYSIS
# -------------------------------------------------------------

def topup_rate(df):
    """Percentage of transactions that are top-ups."""
    return df["topup_flag"].mean()


def topup_volume(df):
    """Total number of top-ups."""
    return df["topup_flag"].sum()


def user_topup_count(df):
    """How many top-ups per user."""
    return df.groupby("user_id")["topup_flag"].sum().reset_index()


# -------------------------------------------------------------
# COHORT ANALYSIS (simple)
# -------------------------------------------------------------

def first_transaction_date(df):
    """Returns first transaction per user."""
    return df.groupby("user_id")["time"].min().reset_index(name="first_seen")


def cohort_size(df):
    """Number of new users per day."""
    first = first_transaction_date(df)
    first["date"] = first["first_seen"].dt.date
    return first.groupby("date")["user_id"].count().reset_index(name="new_users")


# -------------------------------------------------------------
# RISK METRICS (simple)
# -------------------------------------------------------------

def anomaly_rate(df):
    """Percentage of transactions flagged as anomalies."""
    return df["is_anomaly"].mean()


def anomalies_by_type(df):
    """Breakdown of flag types to understand risk drivers."""
    return df[["amount_flag", "rapid_flag", "freq_flag"]].sum()


def high_risk_users(df):
    """Users with multiple anomalies."""
    risky = df[df["is_anomaly"] == 1]
    return risky.groupby("user_id")["is_anomaly"].count().sort_values(ascending=False)


# -------------------------------------------------------------
# EXPORT UTILITIES
# -------------------------------------------------------------

def export_summary(df, path="summary_metrics.csv"):
    """Exports key summary metrics."""
    summary = {
        "total_revenue": total_revenue(df),
        "avg_transaction_value": average_transaction_value(df),
        "unique_users": unique_users(df),
        "topup_rate": topup_rate(df),
        "anomaly_rate": anomaly_rate(df),
    }

    pd.DataFrame([summary]).to_csv(path, index=False)
    return summary


# -------------------------------------------------------------
# END OF FILE
# -------------------------------------------------------------
