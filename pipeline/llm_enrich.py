from openai import OpenAI
import os
import json
import pandas as pd

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# -----------------------------
# LLM: Single article
# -----------------------------
def enrich_article(text):
    prompt = f"""
    Extract the following from the text:
    1. Short summary (2 lines)
    2. Company names (if any)
    3. Location (city/country)

    Return ONLY valid JSON (no explanation, no markdown):

    {{
        "summary": "...",
        "company": "...",
        "location": "..."
    }}

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# Batch enrichment
# -----------------------------
def enrich_news_dataframe(df, limit=5):
    enriched_rows = []

    for i, row in df.head(limit).iterrows():
        row_copy = row.copy()  # ✅ avoid modifying original

        try:
            response = enrich_article(row["text"])

            # 🔧 Clean response (remove markdown if present)
            cleaned = response.strip().replace("```json", "").replace("```", "")

            parsed = json.loads(cleaned)

            row_copy["summary"] = parsed.get("summary")
            row_copy["company"] = parsed.get("company")
            row_copy["location"] = parsed.get("location")

        except Exception as e:
            print(f"Error processing row {i}: {e}")
            row_copy["summary"] = None
            row_copy["company"] = None
            row_copy["location"] = None

        enriched_rows.append(row_copy)

    return pd.DataFrame(enriched_rows)