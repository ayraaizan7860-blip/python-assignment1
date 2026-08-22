import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Home Credit | Executive Portfolio Overview",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 34px;
    font-weight: 750;
    margin-bottom: 2px;
}

.subtitle {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 12px;
}

.kpi-card {
    padding: 15px 16px;
    border-radius: 12px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    min-height: 105px;
}

.kpi-label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 650;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 23px;
    font-weight: 750;
    margin-top: 8px;
}

.insight-card {
    padding: 16px;
    border-radius: 12px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    base_dir = Path(__file__).resolve().parent

    data_path = (
        base_dir
        / "data"
        / "application_train.csv"
    )

    df = pd.read_csv(data_path)

    return df


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🏦 HOME CREDIT")

st.sidebar.caption(
    "Executive Portfolio Overview"
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Portfolio Filters")

# Contract type
contract_options = sorted(
    df["NAME_CONTRACT_TYPE"]
    .dropna()
    .unique()
)

selected_contract = st.sidebar.multiselect(
    "Contract Type",
    contract_options,
    default=contract_options
)

# Income type
income_options = sorted(
    df["NAME_INCOME_TYPE"]
    .dropna()
    .unique()
)

selected_income = st.sidebar.multiselect(
    "Income Type",
    income_options,
    default=income_options
)

# Gender
gender_options = sorted(
    df["CODE_GENDER"]
    .dropna()
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    default=gender_options
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    df["NAME_CONTRACT_TYPE"].isin(selected_contract)
    &
    df["NAME_INCOME_TYPE"].isin(selected_income)
    &
    df["CODE_GENDER"].isin(selected_gender)
].copy()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🏦 HOME CREDIT — EXECUTIVE PORTFOLIO OVERVIEW'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Management overview of customer volume, credit exposure and default risk'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_customers = (
    filtered_df["SK_ID_CURR"].nunique()
)

total_applications = len(filtered_df)

default_customers = int(
    filtered_df["TARGET"].sum()
)

non_default_customers = (
    total_applications -
    default_customers
)

default_rate = (
    filtered_df["TARGET"].mean() * 100
    if total_applications > 0
    else 0
)

total_credit = (
    filtered_df["AMT_CREDIT"].sum()
)

avg_credit = (
    filtered_df["AMT_CREDIT"].mean()
)

avg_income = (
    filtered_df["AMT_INCOME_TOTAL"].mean()
)

avg_annuity = (
    filtered_df["AMT_ANNUITY"].mean()
)

avg_goods_price = (
    filtered_df["AMT_GOODS_PRICE"].mean()
)

median_income = (
    filtered_df["AMT_INCOME_TOTAL"].median()
)

median_credit = (
    filtered_df["AMT_CREDIT"].median()
)


# =========================================================
# KPI ROW 1
# =========================================================

st.markdown(
    '<div class="section-title">📌 Portfolio KPIs</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Total Customers</div>
        <div class="kpi-value">{total_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Total Applications</div>
        <div class="kpi-value">{total_applications:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Default Customers</div>
        <div class="kpi-value">{default_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Non-Default Customers</div>
        <div class="kpi-value">{non_default_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KPI ROW 2
# =========================================================

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Default Rate</div>
        <div class="kpi-value">{default_rate:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c6:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Total Credit Amount</div>
        <div class="kpi-value">₹{total_credit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c7:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Average Credit Amount</div>
        <div class="kpi-value">₹{avg_credit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c8:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Average Customer Income</div>
        <div class="kpi-value">₹{avg_income:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KPI ROW 3
# =========================================================

c9, c10, c11, c12 = st.columns(4)

with c9:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Average Annuity</div>
        <div class="kpi-value">₹{avg_annuity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c10:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Average Goods Price</div>
        <div class="kpi-value">₹{avg_goods_price:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c11:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Median Income</div>
        <div class="kpi-value">₹{median_income:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c12:
    st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-label">Median Credit Amount</div>
        <div class="kpi-value">₹{median_credit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DEFAULT ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Default Portfolio Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# DEFAULT VS NON DEFAULT BAR
# ---------------------------------------------------------

with col1:

    default_bar = pd.DataFrame({
        "Status": [
            "Non-Default",
            "Default"
        ],
        "Customers": [
            non_default_customers,
            default_customers
        ]
    })

    fig = px.bar(
        default_bar,
        x="Status",
        y="Customers",
        text="Customers",
        title="Default vs Non-Default"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        yaxis_title="Customers",
        xaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# DEFAULT DONUT
# ---------------------------------------------------------

with col2:

    donut_data = pd.DataFrame({
        "Status": [
            "Non-Default",
            "Default"
        ],
        "Customers": [
            non_default_customers,
            default_customers
        ]
    })

    fig = px.pie(
        donut_data,
        names="Status",
        values="Customers",
        hole=0.60,
        title=f"Default Percentage — {default_rate:.2f}%"
    )

    fig.update_layout(
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CONTRACT TYPE + CREDIT DISTRIBUTION
# =========================================================

st.markdown(
    '<div class="section-title">💳 Credit Portfolio</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# APPLICATIONS BY CONTRACT TYPE
# ---------------------------------------------------------

with col1:

    contract_data = (
        filtered_df
        .groupby("NAME_CONTRACT_TYPE")
        .size()
        .reset_index(name="Applications")
    )

    fig = px.bar(
        contract_data,
        x="NAME_CONTRACT_TYPE",
        y="Applications",
        text="Applications",
        title="Applications by Contract Type"
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Contract Type",
        yaxis_title="Applications"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# CREDIT HISTOGRAM
# ---------------------------------------------------------

with col2:

    fig = px.histogram(
        filtered_df,
        x="AMT_CREDIT",
        nbins=50,
        title="Credit Amount Distribution",
        labels={
            "AMT_CREDIT": "Credit Amount"
        }
    )

    fig.update_layout(
        height=430,
        yaxis_title="Applications"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# INCOME ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">💰 Income & Exposure Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# INCOME HISTOGRAM
# ---------------------------------------------------------

with col1:

    income_plot = filtered_df[
        filtered_df["AMT_INCOME_TOTAL"] <
        filtered_df["AMT_INCOME_TOTAL"].quantile(0.99)
    ]

    fig = px.histogram(
        income_plot,
        x="AMT_INCOME_TOTAL",
        nbins=50,
        title="Income Distribution — 99th Percentile",
        labels={
            "AMT_INCOME_TOTAL": "Annual Income"
        }
    )

    fig.update_layout(
        height=430,
        yaxis_title="Applications"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# TREEMAP
# ---------------------------------------------------------

with col2:

    treemap_data = (
        filtered_df
        .groupby("NAME_INCOME_TYPE")
        .agg(
            Total_Credit=("AMT_CREDIT", "sum"),
            Default_Rate=("TARGET", "mean"),
            Applications=("TARGET", "count")
        )
        .reset_index()
    )

    treemap_data["Default_Rate"] *= 100

    fig = px.treemap(
        treemap_data,
        path=["NAME_INCOME_TYPE"],
        values="Total_Credit",
        color="Default_Rate",
        hover_data=[
            "Applications",
            "Default_Rate"
        ],
        title="Credit Exposure by Income Type"
    )

    fig.update_layout(
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DEFAULT RATE BY INCOME TYPE
# =========================================================

st.markdown(
    '<div class="section-title">⚠️ Income Segment Risk</div>',
    unsafe_allow_html=True
)

income_risk = (
    filtered_df
    .groupby("NAME_INCOME_TYPE")
    .agg(
        Applications=("TARGET", "count"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

income_risk["Default_Rate"] *= 100

income_risk = income_risk.sort_values(
    "Default_Rate",
    ascending=True
)

fig = px.bar(
    income_risk,
    x="Default_Rate",
    y="NAME_INCOME_TYPE",
    orientation="h",
    text="Default_Rate",
    hover_data=[
        "Applications",
        "Defaults"
    ],
    title="Default Rate by Income Type"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    height=500,
    xaxis_title="Default Rate (%)",
    yaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# INCOME VS CREDIT
# =========================================================

st.markdown(
    '<div class="section-title">📈 Income vs Credit</div>',
    unsafe_allow_html=True
)

sample_size = min(
    10000,
    len(filtered_df)
)

if sample_size > 0:

    scatter_data = filtered_df.sample(
        sample_size,
        random_state=42
    )

    fig = px.scatter(
        scatter_data,
        x="AMT_INCOME_TOTAL",
        y="AMT_CREDIT",
        color="TARGET",
        opacity=0.55,
        title="Customer Income vs Credit Amount",
        labels={
            "AMT_INCOME_TOTAL": "Customer Income",
            "AMT_CREDIT": "Credit Amount",
            "TARGET": "Default"
        },
        hover_data=[
            "SK_ID_CURR",
            "NAME_INCOME_TYPE",
            "NAME_EDUCATION_TYPE"
        ]
    )

    fig.update_layout(
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">📌 Portfolio Insights</div>',
    unsafe_allow_html=True
)

# Largest customer segment
largest_income_segment = (
    filtered_df["NAME_INCOME_TYPE"]
    .value_counts()
    .idxmax()
)

largest_income_count = (
    filtered_df["NAME_INCOME_TYPE"]
    .value_counts()
    .max()
)

# Highest risk income segment
# Require at least 100 applicants
reliable_risk = income_risk[
    income_risk["Applications"] >= 100
]

if len(reliable_risk) > 0:

    highest_risk_row = reliable_risk.loc[
        reliable_risk["Default_Rate"].idxmax()
    ]

    highest_risk_income = (
        highest_risk_row["NAME_INCOME_TYPE"]
    )

    highest_risk_rate = (
        highest_risk_row["Default_Rate"]
    )

else:

    highest_risk_income = "Not available"
    highest_risk_rate = 0


insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.markdown(
        f"""
        <div class="insight-card">

        <b>Overall Default Rate</b><br>

        The current portfolio default rate is
        <b>{default_rate:.2f}%</b>, with
        <b>{default_customers:,}</b> default customers.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-card">

        <b>Total Credit Exposure</b><br>

        The portfolio represents approximately
        <b>₹{total_credit:,.0f}</b> in total credit exposure.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-card">

        <b>Largest Customer Segment</b><br>

        <b>{largest_income_segment}</b> represents the
        largest income segment with
        <b>{largest_income_count:,}</b> applications.

        </div>
        """,
        unsafe_allow_html=True
    )


with insight_col2:

    st.markdown(
        f"""
        <div class="insight-card">

        <b>Highest-Risk Income Segment</b><br>

        Among segments with at least 100 applicants,
        <b>{highest_risk_income}</b> has the highest
        default rate at <b>{highest_risk_rate:.2f}%</b>.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-card">

        <b>Typical Credit Amount</b><br>

        The median credit amount is
        <b>₹{median_credit:,.0f}</b>.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-card">

        <b>Typical Customer Income</b><br>

        The median customer income is
        <b>₹{median_income:,.0f}</b>.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MANAGEMENT RECOMMENDATIONS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Management Recommendations</div>',
    unsafe_allow_html=True
)

recommendation_1 = (
    f"Prioritize enhanced risk assessment for "
    f"{highest_risk_income} applicants, where the "
    f"observed default rate is {highest_risk_rate:.2f}% "
    f"among segments with at least 100 applications."
)

recommendation_2 = (
    "Use income and credit amount together when "
    "assessing affordability. A customer's income "
    "alone does not fully describe their credit burden."
)

recommendation_3 = (
    "Monitor credit exposure by income segment. "
    "High exposure combined with elevated default "
    "rates can create concentration risk."
)

recommendation_4 = (
    "Use median income and median credit alongside "
    "average values because they provide a more "
    "representative view when the portfolio contains "
    "extreme values."
)

st.markdown(
    f"""
    <div class="insight-card">
    <b>1.</b> {recommendation_1}
    </div>

    <div class="insight-card">
    <b>2.</b> {recommendation_2}
    </div>

    <div class="insight-card">
    <b>3.</b> {recommendation_3}
    </div>

    <div class="insight-card">
    <b>4.</b> {recommendation_4}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Home Credit Default Risk Analytics | "
    "Executive Portfolio Overview | "
    "Python • Pandas • Plotly • Streamlit"
)