from searchobject import SearchObject
import os

if __name__ == '__main__':

    current_working_directory = os.getcwd()

    if os.path.isfile(f'{current_working_directory}/datasets/statements.csv'):
        os.system('rm ' + f'{current_working_directory}/datasets/statements.csv')

    searches = [
        SearchObject('body_parts_subparts',
                     ['hand', 'foot', 'arm', 'head', 'abdomen', 'chest', 'mouth', 'finger', 'skin', 'ear'],
                     'part of',
                     ('{} is {} {}.', ['value', 'property', 'item']),
                     'statements.csv'),
        SearchObject('illnesses_causes',
                     ['influenza', 'cancer', 'asthma'],
                     'has effect',
                     ('{} {} of {}.', ['value', 'property', 'item']),
                     'statements.csv'),
        SearchObject('molecules_parts',
                     ['RNA', 'DNA'],
                     'part of',
                     ('{} involves {}.', ['value', 'item']),
                     'statements.csv'),
    ]

    for search in searches:
        search.search_values_for_items()
        search.build_statements(verbose=True)
        # search.build_counterfactuals(verbose=True)