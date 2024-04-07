# Biomed kwnoledge extraction through Wikidata

This project is designed to run SPARQL queries to build statements from Wikidata kwnoledge. Given a list of items and a property common to these items, it retrieves values linked to said items through the speficied property. Templates can be specified to build custom statements.

## Requirements

The project depends on the following Python packages:
- SPARQLWrapper
- pandas

These dependencies are listed in the `requirements.txt` file.

## Installation

Follow these steps to set up the project environment:

1. **Clone the Project and install the requirements**  
```bash
git clone https://github.com/federico-stacchietti/biomed_wikidata.git
cd biomed_wikidata
pip install -r requirements.txt
```

2. Run some sample searches and save the statements in a .csv
```bash
python3 sparql_search.py
```


