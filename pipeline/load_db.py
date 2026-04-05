import sqlite3
import pandas as pd

# -----------------------------
# Create DB connection
# -----------------------------
def create_connection(db_path="db/database.db"):
    return sqlite3.connect(db_path)


# -----------------------------
# Prepare CRE data
# -----------------------------
def prepare_cre(cre_df):
    return pd.DataFrame({
        "date": cre_df["date"],
        "source": "cre",
        "entity_type": "deal",
        "company": cre_df["lender"],
        "location": None,
        "value": cre_df["loan_size"],
        "text": cre_df["asset"],
        "summary": None
    })


# -----------------------------
# Prepare News data
# -----------------------------
def prepare_news(news_df):
    return pd.DataFrame({
        "date": news_df["date"],
        "source": "news",
        "entity_type": "article",
        "company": news_df["company"],
        "location": news_df["location"],
        "value": None,
        "text": news_df["title"],
        "summary": news_df.get("summary")
    })


# -----------------------------
# Load into SQLite
# -----------------------------
def load_to_sqlite(cre_df, news_df):
    conn = create_connection()

    cre_clean = prepare_cre(cre_df)
    news_clean = prepare_news(news_df)
    
    news_clean = news_clean.dropna(axis=1, how="all")

    unified = pd.concat([cre_clean, news_clean], ignore_index=True)

    # Save to DB
    unified.to_sql("unified_data", conn, if_exists="replace", index=False)

    conn.close()

    return unified