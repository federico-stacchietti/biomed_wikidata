from dataclasses import dataclass
from typing import List, Dict, Tuple

import pandas as pd

import os.path
from utils import *


@dataclass
class SearchObject:
    name: str
    items: List[str]
    property_label: str
    template: Tuple[str, List[str]]
    items_id_maps: Dict[str, str]
    id_items_map: Dict[str, str]
    values_id_maps: Dict[str, str]
    id_values_map: Dict[str, str]
    items_values_maps: Dict[str, str]
    statements = List[str]
    file_path = str

    def __init__(self, name, items, property_label, template, file_path):
        self.name = name
        self.items = items
        self.property_label = property_label
        self.property_id = None
        self.template = template
        self.items_id_maps = {}
        self.id_items_map = {}
        self.values_id_maps = {}
        self.id_values_map = {}
        self.items_values_maps = {item: [] for item in items}
        self.file_path = f'datasets/{file_path}'

    def search_property_id(self):
        result = get_property_id(self)
        if result is not None:
            self.property_id = result
            return True
        else:
            print(f'No Wikidata ID for property {self.property_label}')
            return False

    def search_values_for_items(self):
        result = self.search_property_id()
        if result:
            for item in self.items:
                item_id = get_item_id(item, self)
                if item_id:
                    get_values_for_item(item, self.property_id, self)
                else:
                    print(f"No Wikidata ID found for {item}\n")

    def set_property_id(self, property_id):
        self.property_id = property_id

    def add_items_id_map(self, item, id):
        self.items_id_maps[item] = id

    def add_id_items_map(self, item, id):
        self.id_items_map[item] = id

    def add_values_id_map(self, value, id):
        self.values_id_maps[value] = id

    def add_id_values_map(self, id, value):
        self.id_values_map[id] = value

    def add_items_values_map(self, item, value):
        self.items_values_maps[item] = value

    def get_id_from_item(self, item):
        return self.items_id_maps.get(item)

    def get_item_from_id(self, id):
        return self.id_items_map.get(id)

    def get_value_from_id(self, id):
        return self.id_values_map.get(id)

    def build_statements(self, verbose=False):
        template_text = self.template[0]
        template_order = self.template[1]

        statements = []

        columns = ['statement', 'item', 'property', 'value', 'type']

        if os.path.isfile(self.file_path):
            df = pd.read_csv(self.file_path, index_col=False)
        else:
            df = pd.DataFrame(columns=columns)

        for item in self.items_values_maps.keys():
            for value in self.items_values_maps[item]:
                if template_order == ['value', 'property', 'item']:
                    statement = template_text.format(value.capitalize(), self.property_label, item)
                if template_order == ['item', 'property', 'value']:
                    statement = template_text.format(item.capitalize(), self.property_label, value)
                if template_order == ['item', 'value']:
                    statement = template_text.format(item.capitalize(), value)
                if template_order == ['value', 'item']:
                    statement = template_text.format(value.capitalize(), item)

                statements.append(statement)
                temp_df = pd.DataFrame([(statement, item, self.property_label, value, 0)],
                                       columns=['statement', 'item', 'property', 'value', 'type'])
                df = pd.concat([df, temp_df], ignore_index=True)

        if verbose:
            print('######### Statements #########\n')
            for statement in statements:
                print(statement)
        df.to_csv(self.file_path, index=False)

    def build_counterfactuals(self, n=2, verbose=False):
        values_ids = list(self.id_values_map.keys())

        counterfactuals = []

        if os.path.isfile(self.file_path):
            df = pd.read_csv(self.file_path, index_col=False)
        else:
            df = pd.DataFrame(columns=['statement', 'item', 'property', 'value', 'type'])

        for value_id in values_ids:
            template_text = self.template[0]
            template_order = self.template[1]

            pairs = []

            columns = ['statement', 'item', 'property', 'value', 'type']

            for item_id in self.id_items_map.keys():
                if check_false_relationship(item_id, self.property_id, value_id):
                    pairs.append((self.get_item_from_id(item_id), self.get_value_from_id(value_id)))
                else:
                    print(f"Counterfactual not valid: {self.get_value_from_id(value_id)} "
                          f"is part of {self.get_item_from_id(item_id)}")

            for pair in pairs:
                item = pair[0]
                value = pair[1]
                if template_order == ['value', 'property', 'item']:
                    counterfactual = template_text.format(value.capitalize(), self.property_label, item)
                if template_order == ['item', 'property', 'value']:
                    counterfactual = template_text.format(item.capitalize(), self.property_label, value)

                counterfactuals.append(counterfactual)
                temp_df = pd.DataFrame([(counterfactual, item, self.property_label, value, 1)],
                                       columns=columns)
                df = pd.concat([df, temp_df], ignore_index=True)
            if verbose:
                print('\n######### Counterfactuals #########\n')
                for counterfactual in counterfactuals:
                    print(counterfactual)
            df.to_csv(self.file_path, index=False)


    # def build_counterfactuals(self, value_id, n=2):
    #     template_text = self.template[0]
    #     template_order = self.template[1]
    #
    #     counterfactuals = []
    #
    #     pairs = []
    #
    #     for item_id in self.id_items_map.keys():
    #         if check_false_relationship(item_id, self.property_id, value_id):
    #             pairs.append((self.get_item_from_id(item_id), self.get_value_from_id(value_id)))
    #         else:
    #             print(f"Counterfactual not valid: {self.get_value_from_id(value_id)} "
    #                   f"is part of {self.get_item_from_id(item_id)}")
    #
    #     for pair in pairs:
    #         item = pair[0]
    #         value = pair[1]
    #         if template_order == ['value', 'property', 'item']:
    #             counterfactuals.append(template_text.format(value.capitalize(), self.property_label, item))
    #         else:
    #             counterfactuals.append(template_text.format(item.capitalize(), self.property_label, value))
    #
    #     return counterfactuals
