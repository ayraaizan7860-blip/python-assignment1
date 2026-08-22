import pandas as pd
import numpy as np


# =========================================================
# PORTFOLIO METRICS
# =========================================================

def total_customers(df):
    return df["SK_ID_CURR"].nunique()


def total_applications(df):
    return len(df)


def default_customers(df):
    return (df["TARGET"] == 1).sum()


def non_default_customers(df):
    return (df["TARGET"] == 0).sum()


def default_rate(df):
    return df["TARGET"].mean() * 100


# =========================================================
# CREDIT METRICS
# =========================================================

def total_credit(df):
    return df["AMT_CREDIT"].sum()


def average_credit(df):
    return df["AMT_CREDIT"].mean()


def median_credit(df):
    return df["AMT_CREDIT"].median()


def average_annuity(df):
    return df["AMT_ANNUITY"].mean()


def average_goods_price(df):
    return df["AMT_GOODS_PRICE"].mean()


# =========================================================
# INCOME METRICS
# =========================================================

def average_income(df):
    return df["AMT_INCOME_TOTAL"].mean()


def median_income(df):
    return df["AMT_INCOME_TOTAL"].median()


# =========================================================
# AFFORDABILITY METRICS
# =========================================================

def average_credit_to_income(df):
    ratio = (
        df["AMT_CREDIT"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

    return ratio.mean()


def median_credit_to_income(df):
    ratio = (
        df["AMT_CREDIT"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

    return ratio.median()


def average_annuity_to_income(df):
    ratio = (
        df["AMT_ANNUITY"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

    return ratio.mean()


# =========================================================
# BURDEN METRICS
# =========================================================

def high_credit_burden(df):
    ratio = (
        df["AMT_CREDIT"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

    threshold = ratio.quantile(0.90)

    return (ratio >= threshold).sum()


def high_annuity_burden(df):
    ratio = (
        df["AMT_ANNUITY"] /
        df["AMT_INCOME_TOTAL"].replace(0, np.nan)
    )

    threshold = ratio.quantile(0.90)

    return (ratio >= threshold).sum()


# =========================================================
# BUREAU METRICS
# =========================================================

def bureau_customers(bureau):
    return bureau["SK_ID_CURR"].nunique()


def active_bureau_accounts(bureau):
    return (
        bureau["CREDIT_ACTIVE"] == "Active"
    ).sum()


def closed_bureau_accounts(bureau):
    return (
        bureau["CREDIT_ACTIVE"] == "Closed"
    ).sum()


def total_bureau_debt(bureau):
    return bureau[
        "AMT_CREDIT_SUM_DEBT"
    ].sum()


def total_bureau_overdue(bureau):
    return bureau[
        "AMT_CREDIT_SUM_OVERDUE"
    ].sum()


# =========================================================
# INSTALLMENT METRICS
# =========================================================

def total_installments(installments):
    return len(installments)


def average_installment(installments):
    return installments[
        "AMT_INSTALMENT"
    ].mean()


def average_payment(installments):
    return installments[
        "AMT_PAYMENT"
    ].mean()


def late_payment_percentage(installments):

    delay = (
        installments["DAYS_ENTRY_PAYMENT"]
        -
        installments["DAYS_INSTALMENT"]
    )

    return (delay > 0).mean() * 100


def average_payment_delay(installments):

    delay = (
        installments["DAYS_ENTRY_PAYMENT"]
        -
        installments["DAYS_INSTALMENT"]
    )

    return delay.mean()


# =========================================================
# CREDIT CARD METRICS
# =========================================================

def credit_card_customers(card):
    return card["SK_ID_CURR"].nunique()


def average_balance(card):
    return card["AMT_BALANCE"].mean()


def average_credit_limit(card):
    return card[
        "AMT_CREDIT_LIMIT_ACTUAL"
    ].mean()


def average_utilization(card):

    utilization = (
        card["AMT_BALANCE"] /
        card[
            "AMT_CREDIT_LIMIT_ACTUAL"
        ].replace(0, np.nan)
    )

    return utilization.mean() * 100


def customers_with_dpd(card):

    return card.loc[
        card["SK_DPD"] > 0,
        "SK_ID_CURR"
    ].nunique()