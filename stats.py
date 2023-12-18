import os
import json
from collections import Counter
import csv

# Definisci le variabili per i dati da raccogliere
num_files = 0
num_tables = 0
num_cells = 0
num_figures=0
num_articles_without_title = 0
num_articles_without_abstract = 0
num_articles_without_id = 0
all_keywords = []
keyword_counter = Counter()

json_folder = "/Users/fspezzano/miniconda3/envs/desiree/json"

# Percorri tutti i file nella cartella
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        with open(os.path.join(json_folder, filename)) as f:
            data = json.load(f)

            # Conta il numero di tabelle e celle
            num_tables += len(data['content']['tables'])
            for table in data['content']['tables']:
                num_cells += len(table['cells'])
                
            # Conta il numero di immagini
            num_figures += len(data['content']['figures'])
            
            # Verifica la presenza di titolo, abstract e id
            if not data['content']['title']:
                num_articles_without_title += 1
            if not data['content']['abstract']:
                num_articles_without_abstract += 1
            if not data.get('pmcid'):
                num_articles_without_id += 1

            # Aggiungi le keywords alla lista globale e al counter
            all_keywords.extend(data['content']['keywords'])
            keyword_counter.update(data['content']['keywords'])

            num_files += 1

# Calcola le medie
avg_tables_per_document = num_tables / num_files if num_files > 0 else 0
avg_cells_per_table = num_cells / num_tables if num_tables > 0 else 0
avg_keywords_per_article = len(all_keywords) / num_files if num_files > 0 else 0
avg_figures_per_article = num_figures / num_files if num_files > 0 else 0

# Stampa i risultati
print(f"Numero di file: {num_files}")
print(f"Numero di tabelle: {num_tables}")
print(f"Numero di immagini: {num_figures}")
print(f"Numero di celle: {num_cells}")
print(f"Media di tabelle per documento: {avg_tables_per_document:.2f}")
print(f"Media di immagini per documento: {avg_figures_per_article:.2f}")
print(f"Media di celle per tabella: {avg_cells_per_table:.2f}")
print(f"Numero di articoli senza titolo: {num_articles_without_title}")
print(f"Numero di articoli senza abstract: {num_articles_without_abstract}")
print(f"Numero di articoli senza id: {num_articles_without_id}")

# Keyword più ricorrenti
most_common_keywords = keyword_counter.most_common(10)
print(f"\nKeyword più ricorrenti:")
for keyword, count in most_common_keywords:
    print(f"{keyword}: {count}")

print(f"\nMedia di keyword per articolo: {avg_keywords_per_article:.2f}")


# Definisci il percorso del file CSV di output
csv_file_path = "/Users/fspezzano/miniconda3/envs/desiree/dati_statistici.csv"

# Scrivi i dati nel file CSV
with open(csv_file_path, 'w', newline='') as csvfile:
    # Definisci le colonne del CSV
    fieldnames = ['Numero di file', 'Numero di tabelle', 'Numero di immagini', 
                  'Numero di celle', 'Media di tabelle per documento',
                  'Media di immagini per documento', 'Media di celle per tabella',
                  'Numero di articoli senza titolo', 'Numero di articoli senza abstract',
                  'Numero di articoli senza id', 'Media di keyword per articolo']

    # Crea un writer CSV
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Scrivi l'intestazione
    csv_writer.writeheader()

    # Scrivi i dati
    csv_writer.writerow({
        'Numero di file': num_files,
        'Numero di tabelle': num_tables,
        'Numero di immagini': num_figures,
        'Numero di celle': num_cells,
        'Media di tabelle per documento': avg_tables_per_document,
        'Media di immagini per documento': avg_figures_per_article,
        'Media di celle per tabella': avg_cells_per_table,
        'Numero di articoli senza titolo': num_articles_without_title,
        'Numero di articoli senza abstract': num_articles_without_abstract,
        'Numero di articoli senza id': num_articles_without_id,
        'Media di keyword per articolo': avg_keywords_per_article
    })

# Aggiungi anche le keyword più ricorrenti al CSV
with open(csv_file_path, 'a', newline='') as csvfile:
    # Crea un writer CSV
    csv_writer = csv.writer(csvfile)

    # Scrivi l'intestazione per le keyword
    csv_writer.writerow(['Keyword', 'Frequenza'])

    # Scrivi i dati delle keyword
    for keyword, count in most_common_keywords:
        csv_writer.writerow([keyword, count])

print(f"I dati sono stati esportati correttamente nel file CSV: {csv_file_path}")
