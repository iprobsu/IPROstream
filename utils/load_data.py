import pandas as pd
import os

def load_ip_data():
    files = [f for f in os.listdir("data") if f.endswith(".xlsx")]
    records = []

    for f in files:
        year = f[:4]
        xls = pd.read_excel(os.path.join("data", f), sheet_name=None, engine="openpyxl")
        for sheet, df in xls.items():
            df['Year'] = year
            df['IP Type'] = sheet
            records.append(df)

    df = pd.concat(records, ignore_index=True)
    df['Date Applied'] = pd.to_datetime(df.get('Date Applied', pd.NaT), errors='coerce')
    df.fillna('', inplace=True)

    if 'Author' in df:
        df['Author'] = df['Author'].astype(str).str.replace(';', ',').str.split(',')
        df['Author'] = df['Author'].apply(lambda x: [a.strip() for a in x])
        df = df.explode('Author').reset_index(drop=True)

    return df
