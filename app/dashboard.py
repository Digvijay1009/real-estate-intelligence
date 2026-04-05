import os

# Ensure DB exists (for deployment)
if not os.path.exists("db/database.db"):
    from pipeline.ingest_cre import load_cre_data
    from pipeline.ingest_news import fetch_rss_news
    from pipeline.llm_enrich import enrich_news_dataframe
    from pipeline.load_db import load_to_sqlite

    cre_df = load_cre_data("data/Real-Estate-Capital-Europe-Sample-CRE-Lending-Data.xlsx")
    news_df = fetch_rss_news()
    enriched_news = enrich_news_dataframe(news_df, limit=5)
    load_to_sqlite(cre_df, enriched_news)
    
    
import streamlit as st
import pandas as pd
import sqlite3

# Load data
conn = sqlite3.connect("db/database.db")
df = pd.read_sql("SELECT * FROM unified_data", conn)

st.title("📊 Real Estate Intelligence Dashboard")

# -----------------------------
# Filter CRE data
# -----------------------------
cre_df = df[df["source"] == "cre"]

# -----------------------------
# 1. Loan Volume by Company
# -----------------------------
st.subheader("🏦 Top Lenders by Loan Volume")

loan_data = (
    cre_df.groupby("company")["value"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(loan_data)

# -----------------------------
# 2. Deals Over Time
# -----------------------------
st.subheader("📈 Deals Over Time")

time_data = cre_df.groupby("date").size()

st.line_chart(time_data)

# -----------------------------
# 3. News Mentions
# -----------------------------
st.subheader("📰 News Mentions by Company")

news_df = df[(df["source"] == "news") & (df["company"].notna())]

news_data = (
    news_df.groupby("company")
    .size()
    .sort_values(ascending=False)
)

st.bar_chart(news_data)

# -----------------------------
# Insights
# -----------------------------
st.subheader("💡 Key Insights")

st.write("• Major lenders dominate deal volume in CRE dataset")
st.write("• News coverage is sparse and not always aligned with deal activity")
st.write("• Economic trends influence real estate indirectly")