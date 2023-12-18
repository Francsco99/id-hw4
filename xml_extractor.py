from lxml import etree
class XmlElement:
    def __init__(self, xml_file_path):
        # Apri il file XML in lettura e carica la radice
        with open(xml_file_path, "r", encoding="utf-8") as file:
            xml_content = file.read()
        self.root = etree.fromstring(xml_content)

###################
#--ESTRAZIONE ID--#
###################
    def get_article_id(self):
        # Trova l'elemento article-id con l'attributo pub-id-type='pmc' e restituisce il suo testo.
        article_id_element = self.root.xpath("//article-id[@pub-id-type='pmc']/text()")
        return article_id_element if article_id_element is not None else None

#######################
#--ESTRAZIONE TITOLO--#
#######################
    def get_article_title(self):
        # Trova l'elemento article-title all'interno di title-group e restituisce il suo testo.
        title_element = self.root.xpath("//title-group/article-title/text()")
        return title_element if title_element is not None else None

#########################
#--ESTRAZIONE ABSTRACT--#
#########################
    def get_abstract_text(self):
        # Trova tutti gli elementi che seguono il tag abstract.
        abstract_elements = self.root.xpath("//abstract/*")
        abstract_text = ""
        # Prendi ciascun elemento trovato e costruisci una stringa con il contenuto di tutti gli elementi
        for element in abstract_elements:
            abstract_text= abstract_text + (etree.tostring(element, encoding = 'unicode'))
        return abstract_text if abstract_text is not None else None

#########################
#--ESTRAZIONE KEYWORDS--#
#########################
    def get_keywords(self):
        # Cerca tutti gli elementi con il tag kwd
        keyword_elements = self.root.xpath("//kwd-group/kwd/text()")
        return keyword_elements if keyword_elements is not None else None

#######################
#--ESTRAZIONE TABLES--#
#######################
    def get_tables(self):
        # Funzione per estrarre tutte le tabelle con i relativi dati
        tables_list = []
        tables = self.root.xpath("//table-wrap")
        # Per ogni tabella trovata estrai i dati e mettila nella lista di output
        for t in tables:
            output = self.extract_table_data(t)
            tables_list.append(output)
        return tables_list if tables_list is not None else None

    def extract_table_data(self, table_element):
        # Funzione per estrarre i dati da un elemento di tabella XML
        temp_table = {
            "table_id": table_element.xpath("@id")[0] if table_element.xpath("@id") else "",
            "body": "",
            "caption": "",
            "caption_citations": [],
            "foots": table_element.xpath("table-wrap-foot/*/text()") if table_element.xpath("table-wrap-foot/*/text()") else [],
            "paragraphs": [
                {
                    "text": [], 
                    "citations": []
                    }
                ],
            "cells": [
                {
                    "cell_content": "", 
                    "cited_in": []
                    }
                ],
        }
        
        # Estrazione della caption e delle relative citazioni
        captions_map = self.extract_captions(table_element)
        temp_table["caption"], temp_table["caption_citations"] = list(captions_map.keys())[0], list(captions_map.values())[0]
        
        
        # Estrazione table head ---> table body
        value_thead = table_element.xpath(".//thead")
        value_tbody = table_element.xpath(".//tbody")
        head_string = (etree.tostring(value_thead[0], encoding="unicode") if value_thead else "")
        body_string = (etree.tostring(value_tbody[0], encoding="unicode") if value_tbody else "")
        temp_table["body"] = head_string + body_string

        # Estrai il contenuto del paragrafo <p> che precede il nodo <xref>
        id = temp_table["table_id"]
        paragraphs_with_xref = table_element.xpath(f'//p[xref[@ref-type="table" and @rid="{id}"]]')
        # Costruisce la lista di paragrafi estratti
        text_list = []
        citations_list = []
        for par in paragraphs_with_xref:
            par_text_string = (etree.tostring(par, encoding="unicode") if par is not None else "")
            text_list.append(par_text_string)
            citations_list.append(self.extract_citations(par))
        
        citations_list_single = [elemento for sottolista in citations_list for elemento in sottolista]
        temp_table["paragraphs"][0]["citations"] = citations_list_single

        # Mette i paragrafi estratti dentro il campo text
        temp_table["paragraphs"][0]["text"] = text_list

        # Estrai le celle di una tabella
        extracted_cells = table_element.xpath(".//td")
        # Per ogni valore in extracted_cells, crea un nuovo elemento cell_content
        for cella in extracted_cells:
            cell_content_element = {
                "cell_content": etree.tostring(cella, encoding="unicode")
                if cella is not None
                else "",
                "cited_in": self.extract_cell_citations(cella),
            }
            temp_table["cells"].append(cell_content_element)

        return temp_table
    
###############################
#--ESTRAZIONE CITAZIONI CELLS-#
###############################
    def extract_cell_citations(self, cell_content):
        if cell_content is None or cell_content.text is None:
            #print("Il contenuto della cella è vuoto.")
            return []

        cell_citations = self.root.xpath(f'//p[contains(text(), "{cell_content.text}")]')
        citazioni_cella = [ct.text for ct in cell_citations]
    
        #print(citazioni_cella)
        return citazioni_cella


########################
#--ESTRAZIONE FIGURES--#
########################
    def get_figures(self):
        figures_list = []
        figures = self.root.xpath("//fig")
        for f in figures:
            output = self.extract_figure_data(f)
            figures_list.append(output)
        return figures_list if figures_list is not None else None

    def extract_figure_data(self, figure_element):
        temp_figure = {
            "fig_id": figure_element.xpath("@id")[0] if figure_element.xpath("@id") is not None else "",
            "caption": "",
            "source": "",
            "caption_citations" : "",
            "paragraphs": 
                [
                {
                    "text": [],
                    "citations": []
                    }
                ],
        }

        # Estrazione della caption e delle relative citazioni
        captions_map = self.extract_captions(figure_element)
        temp_figure["caption"], temp_figure["caption_citations"] = list(captions_map.keys())[0], list(captions_map.values())[0]
        
        # Estrazione source
        xlink_href = figure_element.xpath(".//graphic/@xlink:href",namespaces={"xlink": "http://www.w3.org/1999/xlink"},)
        href_string = xlink_href[0] if xlink_href else ""
        pmc_id = self.root.xpath("//article-id[@pub-id-type='pmc']/text()")
        temp_figure["source"] = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id[0]}/bin/{href_string}.jpg"

        # Estrai il contenuto del paragrafo <p> che precede il nodo <xref>
        id = temp_figure["fig_id"]
        paragraphs_with_xref = figure_element.xpath(f'//p[xref[@ref-type="fig" and @rid="{id}"]]')
        # Costruisce la lista di paragrafi estratti
        text_list = []
        citations_list =[]
        for par in paragraphs_with_xref:
            text = etree.tostring(par, encoding="unicode")
            text_list.append(text)
            citations_list.append(self.extract_citations(par))
        # Mette i paragrafi estratti dentro il campo text
        
        citations_list_single = [elemento for sottolista in citations_list for elemento in sottolista]
        temp_figure["paragraphs"][0]["text"] = text_list
        temp_figure["paragraphs"][0]["citations"] = citations_list_single


        return temp_figure

##########################
#--ESTRAZIONE CITAZIONI--#
##########################
    def extract_citations(self, element):
        rif = set(element.xpath('.//xref[@ref-type="bibr"]/@rid'))
        citations_string = []
        for r in rif:
            elemento_bibliografico = self.root.xpath(f'//ref[@id="{r}"]')
            for eb in elemento_bibliografico:
                # temp_table["paragraphs"][0]["citations"].append(eb)
                citations_string.append(etree.tostring(eb, encoding="unicode"))
                # print (etree.tostring(eb, encoding='unicode'))
                # print('\n')
                #temp_table["paragraphs"][0]["citations"] = citations_string
        return citations_string
    
#########################
#--ESTRAZIONE CAPTIONS--#
#########################
    def extract_captions(self,element):
        captions_string = ""
        captions = element.xpath(".//caption/*")
        caption_citations=[]
        for caption in captions:
            captions_string = captions_string + etree.tostring(caption, encoding = 'unicode')
            caption_citations.append(self.extract_citations(caption))
        captions_map = {captions_string:caption_citations}
        return captions_map