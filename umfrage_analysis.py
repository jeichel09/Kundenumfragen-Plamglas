import argparse
import pandas as pd
from modules.data_loader import load_csv
from modules.sentiment import analyze_sentiment
import matplotlib.pyplot as plt

def generate_umfrage_report(input_file, output_file):
    """Analysiert Umfragedaten und generiert einen CSV-Bericht."""
    df = load_csv(input_file)
    
    # 1. Numerische Bewertungen (ohne Freitext)
    numeric_data = df[df['kategorie'] != 'feedback']
    report = numeric_data.groupby('kategorie')['bewertung'].agg(['mean', 'count']).round(2)
    
    # 2. Freitext-Sentiment
    feedbacks = df[df['kategorie'] == 'feedback']
    if not feedbacks.empty:
        feedbacks['sentiment'] = feedbacks['kommentar'].apply(analyze_sentiment)
        feedbacks[['umfrage_id', 'sentiment', 'kommentar']].to_csv('feedback_details.csv', index=False)
    
    # Bericht speichern
    report.to_csv(output_file)
    
    # Optional: Histogramm
    if not feedbacks.empty:
        feedbacks['sentiment'].plot(kind='hist', bins=5, title='Sentiment der Freitext-Kommentare')
        plt.savefig('umfrage_sentiment.png')
        plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analysiert Umfrage-CSV-Dateien.')
    parser.add_argument('--input', type=str, required=True, help='Pfad zur CSV-Datei')
    parser.add_argument('--output', type=str, default='umfrage_analyse.csv', help='Ausgabedatei')
    args = parser.parse_args()
    
    generate_umfrage_report(args.input, args.output)
    print(f"Umfrageanalyse gespeichert: {args.output}")
