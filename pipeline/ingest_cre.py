import pandas as pd
import re
from datetime import datetime

# -----------------------------
# Helper: Clean loan size
# -----------------------------
def clean_loan_size(value):
    if pd.isna(value):
        return None

    value = str(value)

    # Remove unwanted characters like 'c.', '>', etc.
    value = re.sub(r"[^\d.]", "", value)

    try:
        return float(value)
    except:
        return None


# -----------------------------
# Helper: Parse month row
# -----------------------------
def parse_date(value):
    # Case 1: Already datetime
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.strftime("%Y-%m")

    # Case 2: String like Mar-18
    try:
        return datetime.strptime(str(value).strip(), "%b-%y").strftime("%Y-%m")
    except:
        return None


# -----------------------------
# Core: Process a single sheet
# -----------------------------
def process_sheet(df, region):
    records = []
    current_date = None
    header_found = False

    for _, row in df.iterrows():
        # first_cell = str(row.iloc[0]).strip()

        # Step 1: Detect header row
        if not header_found:
            if any("Lender" in str(cell) for cell in row):
                header_found = True
            continue

        # Step 2: Detect date row (e.g., Mar-18)
        parsed_date = None
        for cell in row:
            parsed_date = parse_date(cell)
            if parsed_date:
                break
        
        if parsed_date:
            current_date = parsed_date
            continue
        
        if all(pd.isna(cell) for cell in row):
            continue

        # Skip rows until date is found
        if current_date is None:
            continue
        
        if len(row) < 4:
            continue

        lender = row.iloc[0]
        borrower = row.iloc[1]
        loan_size = clean_loan_size(row.iloc[2])
        asset = row.iloc[3]

        # Skip empty rows
        if pd.isna(lender) and pd.isna(borrower):
            continue

        records.append({
            "date": current_date,
            "lender": str(lender).strip() if pd.notna(lender) else None,
            "borrower": str(borrower).strip() if pd.notna(borrower) else None,
            "loan_size": loan_size,
            "asset": str(asset).strip() if pd.notna(asset) else None,
            "source": "cre",
            "entity_type": "deal",
            "region": region
        })

    return pd.DataFrame(records)


# -----------------------------
# Main: Load both sheets
# -----------------------------
def load_cre_data(file_path):
    xls = pd.ExcelFile(file_path)

    all_data = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        
        print(f"\n==== SHEET: {sheet} ====")
        print(df.head(30))
        
        df = df.dropna(how="all").reset_index(drop=True)

        # Normalize columns (take only first 4 relevant ones)
        # df = df.iloc[:, :4]

        # Assign region
        region = "uk" if "UK" in sheet else "eu"

        processed = process_sheet(df, region)
        all_data.append(processed)

    final_df = pd.concat(all_data, ignore_index=True)

    return final_df