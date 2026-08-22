import pandas as pd
import numpy as np


# =========================================================
# APPLICATION FEATURES
# =========================================================

def application_features(df):

    df = df.copy()

    # Age
    df["AGE"] = -df["DAYS_BIRTH"] / 365.25

    # Employment years
    days = df["DAYS_EMPLOYED"].copy()
    days[days > 100000] = np.nan

    df["EMPLOYMENT_YEARS"] = -days / 365.25

    # Income per family member
    df["INCOME_PER_FAMILY"] = (
        df["AMT_INCOME_TOTAL"] /
        df["CNT_FAM_MEMBERS"].replace(0, np.nan)
    )

    # Credit-to-income
    income = df["AMT_INCOME_TOTAL"].replace(0, np.nan)

    df["CREDIT_TO_INCOME"] = (
        df["AMT_CREDIT"] / income
    )

    # Annuity-to-income
    df["ANNUITY_TO_INCOME"] = (
        df["AMT_ANNUITY"] / income
    )

    # Goods-to-income
    df["GOODS_TO_INCOME"] = (
        df["AMT_GOODS_PRICE"] / income
    )

    # Credit-to-goods
    goods = df["AMT_GOODS_PRICE"].replace(0, np.nan)

    df["CREDIT_TO_GOODS"] = (
        df["AMT_CREDIT"] / goods
    )

    # Age groups
    df["AGE_GROUP"] = pd.cut(
        df["AGE"],
        bins=[0, 30, 40, 50, 60, 100],
        labels=[
            "20–30",
            "31–40",
            "41–50",
            "51–60",
            "60+"
        ]
    )

    # Income groups
    df["INCOME_GROUP"] = pd.qcut(
        df["AMT_INCOME_TOTAL"],
        5,
        labels=[
            "Very Low",
            "Low",
            "Middle",
            "High",
            "Very High"
        ],
        duplicates="drop"
    )

    # Employment groups
    df["EMPLOYMENT_GROUP"] = pd.cut(
        df["EMPLOYMENT_YEARS"],
        bins=[
            -1, 1, 3, 5, 10, 20,
            float("inf")
        ],
        labels=[
            "<1 Year",
            "1–3 Years",
            "3–5 Years",
            "5–10 Years",
            "10–20 Years",
            "20+ Years"
        ]
    )

    return df


# =========================================================
# INSTALLMENT FEATURES
# =========================================================

def installment_features(df):

    df = df.copy()

    # Payment delay
    df["PAYMENT_DELAY"] = (
        df["DAYS_ENTRY_PAYMENT"]
        - df["DAYS_INSTALMENT"]
    )

    # Payment difference
    df["PAYMENT_DIFFERENCE"] = (
        df["AMT_PAYMENT"]
        - df["AMT_INSTALMENT"]
    )

    # Payment ratio
    df["PAYMENT_RATIO"] = (
        df["AMT_PAYMENT"] /
        df["AMT_INSTALMENT"].replace(0, np.nan)
    )

    # Payment timing
    df["PAYMENT_TIMING"] = np.select(
        [
            df["PAYMENT_DELAY"] < 0,
            df["PAYMENT_DELAY"] == 0,
            df["PAYMENT_DELAY"] > 0
        ],
        [
            "Early Payment",
            "On-Time Payment",
            "Late Payment"
        ],
        default="Unknown"
    )

    # Payment type
    df["PAYMENT_TYPE"] = np.select(
        [
            df["PAYMENT_RATIO"] < 0.99,
            df["PAYMENT_RATIO"].between(
                0.99, 1.01
            ),
            df["PAYMENT_RATIO"] > 1.01
        ],
        [
            "Underpayment",
            "Full Payment",
            "Overpayment"
        ],
        default="Unknown"
    )

    return df


# =========================================================
# CREDIT CARD FEATURES
# =========================================================

def credit_card_features(df):

    df = df.copy()

    df["CREDIT_UTILIZATION"] = (
        df["AMT_BALANCE"] /
        df["AMT_CREDIT_LIMIT_ACTUAL"]
        .replace(0, np.nan)
    )

    return df


# =========================================================
# BUREAU BALANCE FEATURES
# =========================================================

def bureau_balance_features(df):

    df = df.copy()

    # Delinquency flag
    df["DELINQUENCY"] = df[
        "STATUS"
    ].isin(
        ["1", "2", "3", "4", "5"]
    )

    # Numeric delinquency level
    df["DELINQUENCY_LEVEL"] = pd.to_numeric(
        df["STATUS"],
        errors="coerce"
    )

    return df


# =========================================================
# POS / CASH FEATURES
# =========================================================

def pos_cash_features(df):

    df = df.copy()

    df["DPD_EVENT"] = (
        df["SK_DPD"] > 0
    )

    return df


# =========================================================
# PREVIOUS APPLICATION FEATURES
# =========================================================

def previous_application_features(df):

    df = df.copy()

    df["APPROVED"] = (
        df["NAME_CONTRACT_STATUS"]
        == "Approved"
    )

    df["REFUSED"] = (
        df["NAME_CONTRACT_STATUS"]
        == "Refused"
    )

    return df