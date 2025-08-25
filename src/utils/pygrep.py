def py_grep(pattern, filename, if_ignore_case = False):
    """
        This is a function that does similar things to grep in bash shell.
        It returns a dictionary, with the line index (1-based) as keys and the matching lines as values.
    """
    assert isinstance(pattern, str), "Pattern must be a string."
    assert isinstance(filename, str), "Filename must be a string."
    results = {}
    normal_return = 0
    file_not_found_error = -1
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        return results, file_not_found_error

    if if_ignore_case:
        pattern = pattern.lower()
        for line_number, line in enumerate(f):
            if pattern in line.lower():
                results[line_number+1] = line
        f.close()
        return results, normal_return
    
    for line_number, line in enumerate(f):
        if pattern in line:
            results[line_number+1] = line
    f.close()
    return results, normal_return