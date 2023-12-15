import json

class JsonParser:
    def __init__(self, json_file_path):
        # Inizializza l'oggetto JsonParser con il percorso del file JSON e una struttura dati iniziale.
        self.json_file_path = json_file_path
        self.json_structure = {
            "pmcid": "",  # Identificatore unico dell'articolo
            "content": {
                "title": "",  # Titolo dell'articolo
                "abstract": "",  # Testo dell'abstract
                "keywords": [],  # Elenco delle parole chiave
                "tables": [],
                "figures": []
            }
        }

    def write_json(self):
        # Scrive la struttura JSON nel file specificato.
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.json_structure, json_file, indent=2)

    def add_pmcid(self, value):
        # Aggiunge l'ID PMC all'interno della struttura JSON se il valore è presente.
        if value:
            self.json_structure["pmcid"] = value[0]

    def add_article_title(self, value):
        # Aggiunge il titolo dell'articolo all'interno della struttura JSON se il valore è presente.
        if value:
            self.json_structure["content"]["title"] = value[0]

    def add_abstract_text(self, value):
        # Aggiunge il testo dell'abstract all'interno della struttura JSON se il valore è presente.
        if value:
            self.json_structure["content"]["abstract"] = value

    def add_keywords(self, value):
        # Aggiunge le parole chiave all'interno della struttura JSON se il valore è presente.
        if value:
            self.json_structure["content"]["keywords"] = value

    def add_tables(self,value):
        if value:
            self.json_structure["content"]["tables"] = value
            
    def add_figures(self,value):
        if value:
            self.json_structure["content"]["figures"] = value