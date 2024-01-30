import os
import json
from collections import Counter
import numpy as np
import time

# Definisci le variabili per i dati da raccogliere
num_files = 0
num_tables = 0
num_cells = 0
num_figures=0
num_articles_without_title = 0
num_articles_without_abstract = 0
num_articles_without_id = 0
all_keywords = []
no_abstract=[]
no_id=[]
num_tables_list=[]
num_figures_list=[]
keyword_counter = Counter()
articles_per_table = Counter()
articles_per_figure = Counter()
tables_to_id={}



# Inizializza il timer
start_time = time.time()

json_folder = "/Users/fspezzano/miniconda3/envs/desiree/json"

# Percorri tutti i file nella cartella
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        with open(os.path.join(json_folder, filename)) as f:
            data = json.load(f)

            # Conta il numero di tabelle e celle
            num_tables += len(data['content']['tables'])
            #for table in data['content']['tables']:
                #num_cells += len(table['cells'])
            articles_per_table[len(data['content']['tables'])] += 1
             
            # Conta il numero di immagini
            num_figures += len(data['content']['figures'])
            articles_per_figure[len(data['content']['figures'])] += 1
            
            num_tables_list.append(len(data['content']['tables']))
            num_figures_list.append(len(data['content']['figures']))
            
            # Verifica la presenza di titolo, abstract e id
            if not data['content']['title']:
                num_articles_without_title += 1
            if not data['content']['abstract']:
                num_articles_without_abstract += 1
                no_abstract.append(filename)
            if not data.get('pmcid'):
                num_articles_without_id += 1
                no_id.append(filename)

            # Aggiungi le keywords alla lista globale e al counter
            all_keywords.extend(data['content']['keywords'])
            keyword_counter.update(data['content']['keywords'])

            num_files += 1
            
            if num_files % 500 == 0:
                elapsed_time = time.time() - start_time
                if elapsed_time > 60:
                    # Stampa il tempo trascorso in minuti
                    elapsed_time_minutes = elapsed_time / 60
                    print(f"{num_files} file processati. Tempo trascorso: {elapsed_time_minutes:.2f} minuti.")
                else:
                    print(f"{num_files} file processati. Tempo trascorso: {elapsed_time:.2f} secondi.")

# Calcola le medie
avg_tables_per_document = num_tables / num_files if num_files > 0 else 0
avg_cells_per_table = num_cells / num_tables if num_tables > 0 else 0
avg_keywords_per_article = len(all_keywords) / num_files if num_files > 0 else 0
avg_figures_per_article = num_figures / num_files if num_files > 0 else 0

median_tables = np.median(num_tables_list)
median_figures = np.median(num_figures_list)

print(f"Mediana delle tabelle: {median_tables}")
print(f"Mediana delle figure: {median_figures}")

#print("No abstract: ",no_abstract)
#print("No id",no_id)    

""" # Stampa i risultati
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
most_common_keywords = keyword_counter.most_common(20)
print(f"\nKeyword più ricorrenti:")
for keyword, count in most_common_keywords:
    print(f"{keyword}: {count}")

print(f"\nMedia di keyword per articolo: {avg_keywords_per_article:.2f}")

# Stampa il numero di articoli per numero di tabelle (ordinato)
print("\nNumero di articoli per numero di tabelle (ordinato per numero di articoli):")
sorted_articles_per_table = sorted(articles_per_table.items(), key=lambda x: x[1], reverse=True)
for num_tables, count in sorted_articles_per_table:
    print(f"{num_tables} tabelle: {count} articoli")

# Stampa il numero di articoli per numero di figure (ordinato)
print("\nNumero di articoli per numero di figure (ordinato per numero di articoli):")
sorted_articles_per_figure = sorted(articles_per_figure.items(), key=lambda x: x[1], reverse=True)
for num_figures, count in sorted_articles_per_figure:
    print(f"{num_figures} figure: {count} articoli") """
    
    
