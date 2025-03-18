import argparse
import pandas as pd
from modules.data_loader import load_csv
from modules.sentiment import analyze_sentiment
import matplotlib.pyplot as plt

def generate_feedback_report(input_file, output_file):
    """Analysiert Kundenfeedback und generiert einen Bericht."""
    # Daten laden und bereinigen
    df = load_csv(input_file, drop_na_column="feedback")
    
    # Sentiment-Analyse
    df['sentiment'] = df['feedback'].apply(analyze_sentiment)
    df['category'] = pd.cut(
        df['sentiment'], 
        bins=[-1, -0.5, 0.5, 1],
        labels=['Negativ', 'Neutral', 'Positiv']
    )
    
    # Bericht erstellen
    report = f"""
    **Kundenfeedback-Analysebericht**
    ----------------------------------
    Gesamtbewertungen: {len(df)}
    Durchschnittliches Sentiment: {df['sentiment'].mean():.2f}
    Verteilung:
    - Positiv: {len(df[df['category'] == 'Positiv'])} 
    - Neutral: {len(df[df['category'] == 'Neutral'])}
    - Negativ: {len(df[df['category'] == 'Negativ'])}
    """
    
    # Bericht speichern
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Visualisierung
    df['category'].value_counts().plot(kind='bar', color=['green', 'gray', 'red'])
    plt.title('Sentiment-Verteilung')
    plt.savefig('sentiment_distribution.png')
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analysiert Kundenfeedback-CSV-Dateien.')
    parser.add_argument('--input', type=str, required=True, help='Pfad zur CSV-Datei')
    parser.add_argument('--output', type=str, default='feedback_report.txt', help='Ausgabedatei')
    args = parser.parse_args()
    
    generate_feedback_report(args.input, args.output)
    print(f"Bericht generiert: {args.output}")
