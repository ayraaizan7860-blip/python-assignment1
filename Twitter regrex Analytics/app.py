import sys
import pandas as pd
import streamlit as st

sys.path.append("src")

from metrics import calculate_metrics
from charts import (
    plot_top_hashtags,
    plot_top_mentions,
    plot_tweet_length_distribution,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Twitter RegEx Analytics",
    page_icon="🐦",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "output/processed_tweets.csv"
    )

    return df


df = load_data()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.title("🐦 Twitter RegEx Analytics")

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Dashboard title */
    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .dashboard-subtitle {
        font-size: 16px;
        opacity: 0.7;
        margin-bottom: 25px;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.15);
    }

    /* Section headings */
    h2, h3 {
        margin-top: 20px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.15);
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

min_length = st.sidebar.slider(
    "Minimum Tweet Length",
    min_value=0,
    max_value=int(df["tweet_length"].max()),
    value=0
)

max_length = st.sidebar.slider(
    "Maximum Tweet Length",
    min_value=1,
    max_value=int(df["tweet_length"].max()),
    value=int(df["tweet_length"].max())
)


filtered_df = df[
    (df["tweet_length"] >= min_length)
    &
    (df["tweet_length"] <= max_length)
]


# --------------------------------------------------
# METRICS
# --------------------------------------------------

metrics = calculate_metrics(filtered_df)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Tweets",
    f"{metrics['total_tweets']:,}"
)

col2.metric(
    "Unique Users",
    f"{metrics['unique_users']:,}"
)

col3.metric(
    "Mentions",
    f"{metrics['total_mentions']:,}"
)

col4.metric(
    "Hashtags",
    f"{metrics['total_hashtags']:,}"
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "URLs",
    f"{metrics['total_urls']:,}"
)

col6.metric(
    "Retweets",
    f"{metrics['total_retweets']:,}"
)

col7.metric(
    "Avg Tweet Length",
    f"{metrics['average_tweet_length']:.2f}"
)

col8.metric(
    "Avg Words",
    f"{metrics['average_word_count']:.2f}"
)


st.divider()

# --------------------------------------------------
# SENTIMENT ANALYTICS
# --------------------------------------------------

st.subheader("😊 Sentiment Analytics")

positive_count = (
    filtered_df["sentiment"] == "Positive"
).sum()

negative_count = (
    filtered_df["sentiment"] == "Negative"
).sum()

total_sentiment = positive_count + negative_count

positive_percentage = (
    positive_count / total_sentiment * 100
    if total_sentiment > 0
    else 0
)

negative_percentage = (
    negative_count / total_sentiment * 100
    if total_sentiment > 0
    else 0
)


sent_col1, sent_col2, sent_col3, sent_col4 = st.columns(4)

sent_col1.metric(
    "😊 Positive Tweets",
    f"{positive_count:,}"
)

sent_col2.metric(
    "😞 Negative Tweets",
    f"{negative_count:,}"
)

sent_col3.metric(
    "Positive %",
    f"{positive_percentage:.2f}%"
)

sent_col4.metric(
    "Negative %",
    f"{negative_percentage:.2f}%"
)


sentiment_counts = (
    filtered_df["sentiment"]
    .value_counts()
)

st.bar_chart(sentiment_counts)
# --------------------------------------------------
# CHARTS
# --------------------------------------------------
# --------------------------------------------------
# TOP HASHTAGS & MENTIONS
# --------------------------------------------------

st.divider()

st.subheader("🏆 Top Hashtags & Mentions")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### #️⃣ Top Hashtags")

    top_hashtags = (
        filtered_df["hashtags"]
        .explode()
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_hashtags.columns = [
        "Hashtag",
        "Count"
    ]

    st.dataframe(
        top_hashtags,
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.markdown("### 👤 Top Mentioned Users")

    top_mentions = (
        filtered_df["mentions"]
        .explode()
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_mentions.columns = [
        "Mention",
        "Count"
    ]

    st.dataframe(
        top_mentions,
        use_container_width=True,
        hide_index=True
    )

st.subheader("📊 Tweet Analytics")


col1, col2 = st.columns(2)


with col1:

    st.pyplot(
        plot_top_hashtags(filtered_df),
        use_container_width=True
    )


with col2:

    st.pyplot(
        plot_top_mentions(filtered_df),
        use_container_width=True
    )


st.subheader("📏 Tweet Length Distribution")

st.pyplot(
    plot_tweet_length_distribution(filtered_df),
    use_container_width=True
)


# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
# --------------------------------------------------
# TWEET EXPLORER
# --------------------------------------------------
# --------------------------------------------------


st.divider()

st.subheader("🔎 Tweet Explorer")

st.write(
    "Search and filter processed tweets using text, "
    "sentiment, hashtags, mentions, and retweet status."
)


# Search box
search_text = st.text_input(
    "Search tweet text",
    placeholder="Example: Python, AI, happy, project..."
)


# Filters
filter_col1, filter_col2, filter_col3 = st.columns(3)


with filter_col1:

    sentiment_filter = st.selectbox(
        "Sentiment",
        ["All", "Positive", "Negative"]
    )


with filter_col2:

    mention_filter = st.selectbox(
        "Mentions",
        ["All", "With Mentions", "Without Mentions"]
    )


with filter_col3:

    retweet_filter = st.selectbox(
        "Retweets",
        ["All", "Retweets Only", "Non-Retweets"]
    )


# Start with filtered dataset
explorer_df = filtered_df.copy()


# Text search
if search_text:

    explorer_df = explorer_df[
        explorer_df["Text"]
        .astype(str)
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]


# Sentiment filter
if sentiment_filter != "All":

    explorer_df = explorer_df[
        explorer_df["sentiment"] == sentiment_filter
    ]


# Mention filter
if mention_filter == "With Mentions":

    explorer_df = explorer_df[
        explorer_df["has_mention"] == True
    ]

elif mention_filter == "Without Mentions":

    explorer_df = explorer_df[
        explorer_df["has_mention"] == False
    ]


# Retweet filter
if retweet_filter == "Retweets Only":

    explorer_df = explorer_df[
        explorer_df["is_retweet"] == True
    ]

elif retweet_filter == "Non-Retweets":

    explorer_df = explorer_df[
        explorer_df["is_retweet"] == False
    ]


# Result count
st.info(
    f"Showing {len(explorer_df):,} matching tweets"
)


# Display columns
display_columns = [
    "Target",
    "sentiment",
    "User",
    "Text",
    "tweet_length",
    "word_count",
    "mention_count",
    "hashtag_count",
    "url_count",
    "is_retweet",
]


st.dataframe(
    explorer_df[display_columns].head(100),
    use_container_width=True
)
# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

st.divider()

st.subheader("⬇️ Download Data")

csv_data = explorer_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Tweets",
    data=csv_data,
    file_name="twitter_filtered_tweets.csv",
    mime="text/csv"
)
st.subheader("🔎 Processed Tweet Data")

display_columns = [
    "Target",
    "User",
    "Text",
    "tweet_length",
    "word_count",
    "mentions",
    "hashtags",
    "urls",
    "is_retweet",
]

st.dataframe(
    filtered_df[display_columns].head(100),
    use_container_width=True
)
# --------------------------------------------------
# REGEX PLAYGROUND
# --------------------------------------------------

st.divider()

st.subheader("🧪 RegEx Playground")

st.write(
    "Enter any tweet below and the RegEx engine will "
    "extract mentions, hashtags, URLs, and other patterns."
)

sample_tweet = st.text_area(
    "Enter Tweet",
    value=(
        "RT @OpenAI: New AI model released! "
        "#AI #MachineLearning https://openai.com"
    ),
    height=120
)

if sample_tweet:

    from tweet_parser import analyze_tweet

    result = analyze_tweet(sample_tweet)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 👤 Mentions")

        if result["mentions"]:
            for item in result["mentions"]:
                st.code(item)
        else:
            st.write("No mentions found.")

        st.markdown("### #️⃣ Hashtags")

        if result["hashtags"]:
            for item in result["hashtags"]:
                st.code(item)
        else:
            st.write("No hashtags found.")

        st.markdown("### 🔗 URLs")

        if result["urls"]:
            for item in result["urls"]:
                st.code(item)
        else:
            st.write("No URLs found.")

    with col2:

        st.markdown("### 🔄 Retweet")

        if result["is_retweet"]:
            st.success("Retweet detected")
        else:
            st.info("Not a retweet")

        st.markdown("### 📧 Emails")

        if result["emails"]:
            for item in result["emails"]:
                st.code(item)
        else:
            st.write("No emails found.")

        st.markdown("### 📞 Phone Numbers")

        if result["phone_numbers"]:
            for item in result["phone_numbers"]:
                st.code(item)
        else:
            st.write("No phone numbers found.")

        st.markdown("### 📅 Dates")

        if result["dates"]:
            for item in result["dates"]:
                st.code(item)
        else:
            st.write("No dates found.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Twitter RegEx Analytics | Python • Pandas • RegEx • Streamlit"
)