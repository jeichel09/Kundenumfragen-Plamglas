import pandas as pd

def load_csv(file_path, drop_na_column=None):
    """Lädt CSV-Daten und bereinigt leere Einträge."""
    df = pd.read_csv(file_path)
    if drop_na_column:
        df.dropna(subset=[drop_na_column], inplace=True)
    return df
