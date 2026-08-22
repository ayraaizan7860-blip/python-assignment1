import pandas as pd
import streamlit as st

DATA_PATH = "data/"


@st.cache_data
def load_application():
    return pd.read_csv(
        DATA_PATH + "application_train.csv"
    )


@st.cache_data
def load_bureau():
    return pd.read_csv(
        DATA_PATH + "bureau.csv"
    )


@st.cache_data
def load_bureau_balance():
    return pd.read_csv(
        DATA_PATH + "bureau_balance.csv"
    )


@st.cache_data
def load_previous_application():
    return pd.read_csv(
        DATA_PATH + "previous_application.csv"
    )


@st.cache_data
def load_pos_cash():
    return pd.read_csv(
        DATA_PATH + "POS_CASH_balance.csv"
    )


@st.cache_data
def load_installments():
    return pd.read_csv(
        DATA_PATH + "installments_payments.csv"
    )


@st.cache_data
def load_credit_card():
    return pd.read_csv(
        DATA_PATH + "credit_card_balance.csv"
    )