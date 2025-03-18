import argparse
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from modules.data_loader import load_csv
from modules.sentiment import analyze_sentiment

def generate_umfrage_report(input_file, output_dir):
    df = load_csv(input_file)
    
    # 1. Numerische Bewertungen analysieren
    numeric_data = df[df['kategorie'] != 'feedback']
    report = numeric_data.groupby('kategorie').agg(
        durchschnitt=('bewertung', 'mean'),
        teilnehmer=('bewertung', 'count')
    ).round(2)
    
    # 2. Freitext-Kommentare analysieren
    feedbacks = df[df['kategorie'] == 'feedback']
    if not feedbacks.empty:
        feedbacks['sentiment'] = feedbacks['kommentar'].apply(analyze_sentiment)
        feedbacks.to_csv(f"{output_dir}/feedback_details.csv", index=False)
        
        # Wordcloud generieren
        text = " ".join(feedbacks['kommentar'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        wordcloud.to_file(f"{output_dir}/wordcloud.png")
    
    # 3. Visualisierung der Bewertungen
    plt.figure(figsize=(10, 5))
    report['durchschnitt'].plot(kind='bar', color='skyblue')
    plt.title('Durchschnittliche Bewertungen pro Kategorie')
    plt.ylabel('Bewertung (1-5)')
    plt.ylim(0, 5)
    plt.savefig(f"{output_dir}/bewertungen.png")
    plt.close()
    
    # Bericht speichern
    report.to_csv(f"{output_dir}/umfrage_analyse.csv")
    print(f"Berichte und Grafiken gespeichert in: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analysiert Umfragedaten der Plamglas GmbH.')
    parser.add_argument('--input', type=str, required=True, help='Pfad zur CSV-Datei')
    parser.add_argument('--output_dir', type=str, default='umfrage_results', help='Ausgabeordner')
    args = parser.parse_args()
    
    generate_umfrage_report(args.input, args.output_dir)
