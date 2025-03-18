import pandas as pd
from textblob import TextBlob  # Für Sentiment-Analyse
import matplotlib.pyplot as plt
import argparse

def load_data(file_path):
    """Lädt CSV-Daten und bereinigt leere Einträge."""
    df = pd.read_csv(file_path)
    df.dropna(subset=['feedback'], inplace=True)
    return df

def analyze_sentiment(text):
    """Berechnet Sentiment-Polarität (-1 bis +1)."""
    return TextBlob(text).sentiment.polarity

def analyze_umfrage(input_csv, output_csv):
    # Daten laden
    df = pd.read_csv(input_csv)
    
    # 1. Numerische Bewertungen aggregieren (ohne Freitext)
    numeric_data = df[df['kategorie'] != 'feedback']
    report = numeric_data.groupby('kategorie')['bewertung'].mean().round(2)
    
    # 2. Freitext-Kommentare analysieren
    feedbacks = df[df['kategorie'] == 'feedback']
    feedbacks['sentiment'] = feedbacks['kommentar'].apply(lambda x: TextBlob(x).sentiment.polarity)
    
    # Bericht speichern
    report.to_csv(output_csv)
    print(f"Analysebericht gespeichert unter: {output_csv}")

    # Optional: Sentiment-Plot
    feedbacks['sentiment'].plot(kind='hist', title='Sentiment der Freitext-Kommentare')
    plt.savefig('sentiment_histogram.png')

# Beispielaufruf
analyze_umfrage('umfrage_daten.csv', 'umfrage_analyse.csv')

def generate_report(df, output_file):
    """Erstellt einen Analysebericht mit Visualisierungen."""
    # Sentiment-Kategorien
    df['sentiment'] = df['feedback'].apply(analyze_sentiment)
    df['category'] = pd.cut(df['sentiment'], 
                            bins=[-1, -0.5, 0.5, 1],
                            labels=['Negativ', 'Neutral', 'Positiv'])
    
    # Häufigste Keywords extrahieren (Beispiel)
    keywords = {
        'Positiv': ['gut', 'schnell', 'empfehlen'],
        'Negativ': ['langsam', 'Problem', 'enttäuscht']
    }
    
    # Bericht generieren
    report = f"""
    **Kundenfeedback-Analysebericht**
    ----------------------------------
    Gesamtbewertungen: {len(df)}
    Durchschnittliches Sentiment: {df['sentiment'].mean():.2f}
    
    Verteilung:
    - Positiv: {len(df[df['category'] == 'Positiv'])} Bewertungen
    - Neutral: {len(df[df['category'] == 'Neutral'])} Bewertungen
    - Negativ: {len(df[df['category'] == 'Negativ'])} Bewertungen
    
    Häufige Themen:
    - Positive Bewertungen: {', '.join(keywords['Positiv'])}
    - Negative Bewertungen: {', '.join(keywords['Negativ'])}
    """
    
    # Speichern des Berichts
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Visualisierung (optional)
    df['category'].value_counts().plot(kind='bar', color=['green', 'gray', 'red'])
    plt.title('Sentiment-Verteilung')
    plt.savefig('sentiment_distribution.png')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analysiert Kundenfeedback-Daten.')
    parser.add_argument('--input', type=str, required=True, help='Pfad zur CSV-Datei')
    parser.add_argument('--output', type=str, default='feedback_report.txt', help='Ausgabedatei')
    args = parser.parse_args()
    
    df = load_data(args.input)
    generate_report(df, args.output)
    print(f"Bericht erfolgreich generiert: {args.output}")
