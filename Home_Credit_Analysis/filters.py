import streamlit as st


def application_filters(df):

    st.sidebar.header("Filters")

    # Gender
    if "CODE_GENDER" in df.columns:
        gender = st.sidebar.multiselect(
            "Gender",
            options=sorted(
                df["CODE_GENDER"]
                .dropna()
                .unique()
            )
        )

        if gender:
            df = df[
                df["CODE_GENDER"].isin(gender)
            ]

    # Income Type
    if "NAME_INCOME_TYPE" in df.columns:
        income_type = st.sidebar.multiselect(
            "Income Type",
            options=sorted(
                df["NAME_INCOME_TYPE"]
                .dropna()
                .unique()
            )
        )

        if income_type:
            df = df[
                df["NAME_INCOME_TYPE"]
                .isin(income_type)
            ]

    # Education
    if "NAME_EDUCATION_TYPE" in df.columns:
        education = st.sidebar.multiselect(
            "Education",
            options=sorted(
                df["NAME_EDUCATION_TYPE"]
                .dropna()
                .unique()
            )
        )

        if education:
            df = df[
                df["NAME_EDUCATION_TYPE"]
                .isin(education)
            ]

    # Contract Type
    if "NAME_CONTRACT_TYPE" in df.columns:
        contract = st.sidebar.multiselect(
            "Contract Type",
            options=sorted(
                df["NAME_CONTRACT_TYPE"]
                .dropna()
                .unique()
            )
        )

        if contract:
            df = df[
                df["NAME_CONTRACT_TYPE"]
                .isin(contract)
            ]

    # Target
    if "TARGET" in df.columns:

        target = st.sidebar.multiselect(
            "Default Status",
            options=[0, 1],
            format_func=lambda x:
                "Non-Default"
                if x == 0
                else "Default"
        )

        if target:
            df = df[
                df["TARGET"].isin(target)
            ]

    # Income range
    if "AMT_INCOME_TOTAL" in df.columns:

        min_income = float(
            df["AMT_INCOME_TOTAL"].min()
        )

        max_income = float(
            df["AMT_INCOME_TOTAL"].max()
        )

        income_range = st.sidebar.slider(
            "Income Range",
            min_value=min_income,
            max_value=max_income,
            value=(min_income, max_income)
        )

        df = df[
            df["AMT_INCOME_TOTAL"].between(
                income_range[0],
                income_range[1]
            )
        ]

    # Credit range
    if "AMT_CREDIT" in df.columns:

        min_credit = float(
            df["AMT_CREDIT"].min()
        )

        max_credit = float(
            df["AMT_CREDIT"].max()
        )

        credit_range = st.sidebar.slider(
            "Credit Range",
            min_value=min_credit,
            max_value=max_credit,
            value=(min_credit, max_credit)
        )

        df = df[
            df["AMT_CREDIT"].between(
                credit_range[0],
                credit_range[1]
            )
        ]

    return df