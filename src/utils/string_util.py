

def convert_array_to_string(array, connecting_char='\n', char_to_strip=''):
        """
        Given the input array, converts it to a single string 
        in one line. Note that if the element in the array
        ends with '\n', it will be removed.
        """
        assert isinstance(array, list), "Input must be a list."
        assert all(isinstance(item, str) for item in array), "All items in the list must be strings."
        return connecting_char.join(item.strip(char_to_strip) for item in array)