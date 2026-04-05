# from pipeline.ingest_cre import load_cre_data

# df = load_cre_data("data/Real-Estate-Capital-Europe-Sample-CRE-Lending-Data.xlsx")

# print(df.head())
# print(df.shape)



# from pipeline.ingest_news import fetch_rss_news

# news_df = fetch_rss_news()

# print("NEWS DATA:")
# print(news_df.head())
# print(news_df.shape)


# from pipeline.ingest_cre import load_cre_data
# from pipeline.ingest_news import fetch_rss_news
# from pipeline.llm_enrich import enrich_article

# # Step 1: CRE data
# cre_df = load_cre_data("data/Real-Estate-Capital-Europe-Sample-CRE-Lending-Data.xlsx")

# print("CRE DATA:")
# print(cre_df.head())
# print(cre_df.shape)

# # Step 2: News data
# news_df = fetch_rss_news()

# print("\nNEWS DATA:")
# print(news_df.head())
# print(news_df.shape)

# # Step 3: LLM test
# sample_text = news_df.iloc[0]["text"]

# result = enrich_article(sample_text)

# print("\nLLM OUTPUT:")
# print(result)

# from pipeline.ingest_cre import load_cre_data
# from pipeline.ingest_news import fetch_rss_news
# from pipeline.llm_enrich import enrich_article, enrich_news_dataframe

# # Step 1: CRE data
# cre_df = load_cre_data("data/Real-Estate-Capital-Europe-Sample-CRE-Lending-Data.xlsx")

# print("CRE DATA:")
# print(cre_df.head())
# print(cre_df.shape)

# # Step 2: News data
# news_df = fetch_rss_news()

# print("\nNEWS DATA:")
# print(news_df.head())
# print(news_df.shape)

# # Step 3: LLM test (optional but keep for debugging)
# if not news_df.empty:
#     sample_text = news_df.iloc[0]["text"]
#     result = enrich_article(sample_text)

#     print("\nLLM OUTPUT (Single):")
#     print(result)

# # ✅ Step 4: Batch enrichment (THIS IS IMPORTANT)
# enriched_news = enrich_news_dataframe(news_df, limit=5)

# print("\nENRICHED NEWS:")
# print(enriched_news[["title", "company", "location"]])

# from pipeline.load_db import load_to_sqlite

# # Step 5: Load into SQLite
# unified_df = load_to_sqlite(cre_df, enriched_news)

# print("\nUNIFIED DATA:")
# print(unified_df.head())
# print(unified_df.shape)

# from pipeline.ingest_cre import load_cre_data
# from pipeline.ingest_news import fetch_rss_news
# from pipeline.llm_enrich import enrich_article, enrich_news_dataframe
# from pipeline.load_db import load_to_sqlite

# # Step 1: CRE data
# cre_df = load_cre_data("data/Real-Estate-Capital-Europe-Sample-CRE-Lending-Data.xlsx")

# print("CRE DATA:")
# print(cre_df.head())
# print(cre_df.shape)

# # Step 2: News data
# news_df = fetch_rss_news()

# print("\nNEWS DATA:")
# print(news_df.head())
# print(news_df.shape)

# # Step 3: LLM test (optional)
# if not news_df.empty:
#     sample_text = news_df.iloc[0]["text"]
#     result = enrich_article(sample_text)

#     print("\nLLM OUTPUT (Single):")
#     print(result)

# # Step 4: Batch enrichment
# if not news_df.empty:
#     enriched_news = enrich_news_dataframe(news_df, limit=5)

#     print("\nENRICHED NEWS:")
#     print(enriched_news[["title", "company", "location"]])
# else:
#     print("No news data available")
#     enriched_news = news_df

# # Step 5: Load into SQLite
# unified_df = load_to_sqlite(cre_df, enriched_news)

# print("\nUNIFIED DATA:")
# print(unified_df.head())
# print(unified_df.shape)

from pipeline.query import run_query

# Query 1: Top companies by loan volume
query1 = """
SELECT company, SUM(value) as total_loan
FROM unified_data
WHERE source = 'cre'
GROUP BY company
ORDER BY total_loan DESC
LIMIT 5;
"""

print("\nTOP COMPANIES BY LOAN:")
print(run_query(query1))


# Query 2: Companies appearing in news
query2 = """
SELECT company, COUNT(*) as mentions
FROM unified_data
WHERE source = 'news'
GROUP BY company
ORDER BY mentions DESC;
"""

print("\nNEWS MENTIONS:")
print(run_query(query2))