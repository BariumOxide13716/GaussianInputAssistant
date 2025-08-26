

def search_array_string_elements(array, starting_string=None, ending_string=None, containing_string=None, match_case=True):
    """
    Searches for elements in the array that match the specified criteria.
    At least one of starting_string, ending_string, or containing_string must be provided.
    Returns a list of matching elements.
    """
    assert isinstance(array, list), "Input must be a list."
    assert all(isinstance(item, str) for item in array), "All items in the list must be strings."
    assert any([starting_string, ending_string, containing_string]), "At least one of starting_string, ending_string, or containing_string must be provided."

    index_dict = {}
    index_dict['starting'] = []
    index_dict['ending'] = []
    index_dict['containing'] = []


    if starting_string is not None:
        assert isinstance(starting_string, str), "starting_string must be a string."
        if not match_case:
            starting_string = starting_string.lower()
            for i, item in enumerate(array):
                if item.lower().startswith(starting_string):
                    index_dict['starting'].append(i)
        else:
            for i, item in enumerate(array):
                if item.startswith(starting_string):
                    index_dict['starting'].append(i)

    if ending_string is not None:
        assert isinstance(ending_string, str), "ending_string must be a string."
        if not match_case:
            ending_string = ending_string.lower()
            for i, item in enumerate(array):
                if item.lower().endswith(ending_string):
                    index_dict['ending'].append(i)
        else:
            for i, item in enumerate(array):
                if item.endswith(ending_string):
                    index_dict['ending'].append(i)

    if containing_string is not None:
        assert isinstance(containing_string, str), "containing_string must be a string."
        if not match_case:
            containing_string = containing_string.lower()
            for i, item in enumerate(array):
                if containing_string in item.lower():
                    index_dict['containing'].append(i)
        else:
            for i, item in enumerate(array):
                if containing_string in item:
                    index_dict['containing'].append(i)

    return index_dict
