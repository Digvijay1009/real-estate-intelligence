# 🏢 Real Estate Intelligence Pipeline

## 📌 Overview

This project builds an end-to-end **data pipeline** that ingests messy real estate data, enriches it with AI, and produces a **unified dataset with insights and a dashboard**.

The goal is to transform **raw, unstructured, multi-source data** into **structured intelligence and actionable insights**.

---

## 🚀 Architecture

```
Ingestion → Cleaning → LLM Enrichment → Unified Schema → SQLite → Dashboard
```

### Components:

1. **CRE Dataset (Excel)**

   * Parsed messy spreadsheet with multiple sections and formats
   * Extracted structured deal-level data

2. **News Data (RSS Feed)**

   * Fetched latest business/news articles
   * Limited to 10–15 articles as per constraints

3. **LLM Enrichment (OpenRouter / GPT)**

   * Extracted:

     * Summary
     * Company
     * Location
   * Applied selectively (5 articles) to avoid overuse

4. **Data Unification**

   * Combined CRE + News into a **common schema**

5. **Storage**

   * Stored in **SQLite database**
   * Table: `unified_data`

6. **Dashboard (Streamlit)**

   * Interactive visualisations
   * Displays insights

---

## 📊 Data Sources

* CRE Lending Dataset (Excel)
* RSS Feed (BBC Business News)

---

## 🧠 AI Usage

Used LLM to:

* Extract entities (company, location)
* Generate summaries

### Example Output:

```json
{
  "summary": "Pepsi withdrew sponsorship...",
  "company": "Pepsi",
  "location": "UK"
}
```

---

## 📁 Unified Schema

| Column      | Description                |
| ----------- | -------------------------- |
| date        | Deal/article date          |
| source      | `cre` or `news`            |
| entity_type | `deal` / `article`         |
| company     | Lender or extracted entity |
| location    | Extracted location         |
| value       | Loan size (CRE only)       |
| text        | Asset / title              |
| summary     | LLM-generated summary      |

---

## 🗄️ Example Query

```sql
SELECT company, SUM(value) AS total_loan
FROM unified_data
WHERE source = 'cre'
GROUP BY company
ORDER BY total_loan DESC;
```

---

## 📈 Dashboard Features

* 🏦 Top Lenders by Loan Volume
* 📈 Deals Over Time
* 📰 News Mentions by Company

---

## 💡 Key Insights

* Major lenders dominate CRE deal volume, indicating concentration in financing activity
* News coverage shows weak alignment with lending activity
* Macroeconomic trends indirectly influence real estate markets

---

## ⚖️ Trade-offs & Decisions

### 1. Limited LLM Usage

* Applied only to 5 articles
* Reason: cost, latency, and constraint compliance

### 2. RSS over Web Scraping

* More stable and faster
* Avoids HTML parsing complexity

### 3. Imperfect Entity Extraction

* LLM may return generic entities (e.g., "major European firm")
* Accepted as realistic limitation

### 4. Partial Data Usage

* Full CRE dataset used
* News limited intentionally (sampling strategy)

---

## 🛠️ Tech Stack

* Python
* Pandas
* SQLite
* Streamlit
* OpenRouter (LLM API)

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run pipeline

```bash
python main.py
```

### 3. Launch dashboard

```bash
streamlit run app/dashboard.py
```

---

## 📦 Output

* SQLite DB → `db/database.db`
* Unified dataset → `unified_data` table
* Dashboard → http://localhost:8501

---

## ✅ Deliverables

* ✔ Unified structured dataset
* ✔ Dashboard with 3 visualisations
* ✔ AI-powered enrichment
* ✔ Queryable SQLite system
* ✔ Code + explanation

---

## 🧠 Summary

This project demonstrates:

* Handling messy real-world data
* Multi-source data integration
* Controlled use of LLMs
* Building an end-to-end data pipeline
* Delivering insights through a dashboard

---
