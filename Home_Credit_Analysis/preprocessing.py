import pandas as pd
import numpy as np


# =========================================================
# BASIC CLEANING
# =========================================================

def basic_cleaning(df):
    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Clean categorical columns
    categorical = df.select_dtypes(
        include="object"
    ).columns

    for col in categorical:
        df[col] = df[col].str.strip()

    return df


# =========================================================
# MISSING VALUE SUMMARY
# =========================================================

def missing_summary(df):

    result = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isna().sum().values,
        "Missing %": (
            df.isna().mean().values * 100
        ),
        "Unique Values": [
            df[col].nunique()
            for col in df.columns
        ]
    })

    return result.sort_values(
        "Missing %",
        ascending=False
    )


# =========================================================
# DATA TYPE SUMMARY
# =========================================================

def datatype_summary(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(dtype)
            for dtype in df.dtypes
        ],
        "Unique Values": [
            df[col].nunique()
            for col in df.columns
        ]
    })


# =========================================================
# NUMERICAL SUMMARY
# =========================================================

def numerical_summary(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    return numeric.describe().T


# =========================================================
# CATEGORICAL SUMMARY
# =========================================================

def categorical_summary(df):

    categorical = df.select_dtypes(
        include="object"
    )

    return categorical.describe().T


# =========================================================
# OUTLIER SUMMARY - IQR METHOD
# =========================================================

def outlier_summary(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    results = []

    for col in numeric.columns:

        q1 = numeric[col].quantile(0.25)
        q3 = numeric[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = (
            (numeric[col] < lower) |
            (numeric[col] > upper)
        ).sum()

        results.append({
            "Column": col,
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "Lower Bound": lower,
            "Upper Bound": upper,
            "Outlier Count": outliers
        })

    return pd.DataFrame(results)


# =========================================================
# HOME CREDIT SPECIAL VALUE
# =========================================================

def fix_days_employed(df):

    df = df.copy()

    if "DAYS_EMPLOYED" in df.columns:

        # Home Credit uses 365243 as a special value
        df["DAYS_EMPLOYED"] = df[
            "DAYS_EMPLOYED"
        ].replace(
            365243,
            np.nan
        )

    return df


# =========================================================
# CATEGORY CONSISTENCY
# =========================================================

def category_summary(df):

    categorical = df.select_dtypes(
        include="object"
    ).columns

    results = []

    for col in categorical:

        results.append({
            "Column": col,
            "Unique Categories": df[col].nunique(),
            "Missing": df[col].isna().sum(),
            "Most Common": (
                df[col].mode().iloc[0]
                if not df[col].mode().empty
                else None
            )
        })

    return pd.DataFrame(results)


# =========================================================
# FULL PREPROCESSING
# =========================================================

def preprocess_application(df):

    df = basic_cleaning(df)

    df = fix_days_employed(df)

    return df