from SPARQLWrapper import SPARQLWrapper, JSON
import re


def get_item_id(item, search):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.addCustomHttpHeader("User-Agent", "MyApp/1.0 (MyContactInfo@example.com)")

    query = f"""
        SELECT ?item WHERE {{
          ?item rdfs:label "{item}"@en.
        }}
        LIMIT 1
        """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        item_url = results["results"]["bindings"][0]["item"]["value"]
        item_id = item_url.split('/')[-1]
        search.add_items_id_map(item, item_id)
        search.add_id_items_map(item_id, item)
        return item_id
    else:
        return None


def get_property_id(search):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.addCustomHttpHeader("User-Agent", "MyApp/1.0 (MyContactInfo@example.com)")

    query = f"""
        SELECT ?item WHERE {{
          ?item rdfs:label "{search.property_label}"@en.
        }}
        LIMIT 1
        """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        item_url = results["results"]["bindings"][0]["item"]["value"]
        item_id = item_url.split('/')[-1]
        search.set_property_id(item_id)
        return item_id
    else:
        return None


def get_values_for_item(item, property, search):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.addCustomHttpHeader("User-Agent", "MyApp/1.0 (MyContactInfo@example.com)")

    pattern = r"^Q\d+$"

    item_id = search.get_id_from_item(item)
    query = f"""
    SELECT ?subPart ?subPartLabel WHERE {{
      ?subPart wdt:{property} wd:{item_id}; 
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 10
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    values_pairs = [(result["subPartLabel"]["value"], result["subPart"]["value"].split('/')[-1]) for result in
                    results["results"]["bindings"] if not re.match(pattern, result["subPartLabel"]["value"])]

    for value, value_id in values_pairs:
        search.add_values_id_map(value, value_id)
        search.add_id_values_map(value_id, value)

    values = [values_pair[0] for values_pair in values_pairs]

    search.add_items_values_map(item, values)


def check_false_relationship(item_id, property, value_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.addCustomHttpHeader("User-Agent", "ExampleApp/1.0 (example@example.com)")
    query = f"""
    ASK WHERE {{
      wd:{value_id} wdt:{property}* wd:{item_id}.
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()

    return not result['boolean']