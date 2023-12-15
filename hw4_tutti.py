import os
import time
from xml_extractor import XmlElement
from json_parser import JsonParser

# Percorsi delle cartelle di input e output
input_folder = "/Users/fspezzano/miniconda3/envs/desiree/download"
output_folder = "/Users/fspezzano/vscode/hw4/json"

# Assicurati che la cartella di output esista
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Elenco dei file XML nella cartella di input
xml_files = [f for f in os.listdir(input_folder) if f.endswith(".xml")]

# Inizializza il contatore
file_counter = 0

# Inizializza il timer
start_time = time.time()

# Per ogni file XML, esegui le istruzioni
for xml_file in xml_files:
    file_counter += 1

    xml_path = os.path.join(input_folder, xml_file)
    json_file = os.path.splitext(xml_file)[0] + ".json"
    json_path = os.path.join(output_folder, json_file)

    xmlObject = XmlElement(xml_path)
    jsonObject = JsonParser(json_path)

    jsonObject.add_pmcid(XmlElement.get_article_id(xmlObject))
    jsonObject.add_article_title(XmlElement.get_article_title(xmlObject))
    jsonObject.add_abstract_text(XmlElement.get_abstract_text(xmlObject))
    jsonObject.add_keywords(XmlElement.get_keywords(xmlObject))
    jsonObject.add_tables(XmlElement.get_tables(xmlObject))
    jsonObject.add_figures(XmlElement.get_figures(xmlObject))

    jsonObject.write_json()

    if file_counter % 500 == 0:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:
            # Stampa il tempo trascorso in minuti
            elapsed_time_minutes = elapsed_time / 60
            print(
                f"{file_counter} file processati. Tempo trascorso: {elapsed_time_minutes:.2f} minuti."
            )
        else:
            print(
                f"{file_counter} file processati. Tempo trascorso: {elapsed_time:.2f} secondi."
            )
# Calcola la media del tempo di elaborazione per ogni file
average_time_per_file = (
    (time.time() - start_time) / file_counter if file_counter > 0 else 0
)

print(
    f"\nProcessamento completato. File totali: {file_counter}. Tempo totale: {elapsed_time:.2f} secondi."
)
print(f"Tempo medio di processamento per file: {average_time_per_file:.4f} secondi.")