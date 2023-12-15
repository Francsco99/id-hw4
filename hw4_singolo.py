from xml_extractor import XmlElement
from json_parser import JsonParser

file_path = "/Users/fspezzano/vscode/hw4/TEST.xml"
json_path = "/Users/fspezzano/vscode/hw4/TEST.json"

xmlObject = XmlElement(file_path)
jsonObject = JsonParser(json_path)

#foot
jsonObject.add_pmcid(XmlElement.get_article_id(xmlObject))
jsonObject.add_article_title(XmlElement.get_article_title(xmlObject))
jsonObject.add_abstract_text(XmlElement.get_abstract_text(xmlObject))
jsonObject.add_keywords(XmlElement.get_keywords(xmlObject))
jsonObject.add_tables(XmlElement.get_tables(xmlObject))
jsonObject.add_figures(XmlElement.get_figures(xmlObject))


jsonObject.write_json()