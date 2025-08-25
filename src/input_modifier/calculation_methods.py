"""
This class is the container of the calculation methods in gaussian.
"""
import json
import os
from input_parameters import print_level, \
                             electronic_structure_method, \
                             optional_standalone, \
                             optional_withvalue
class CalculationMethods():

    def __init__(self):
        self.print_level = None
        self.method_electronic_structure = {}
        self.method_optional_standalone = {}
        self.method_optional_withvalue = {}
        self.other_options = []
        self.method_electronic_structure['theory'] = None
        self.method_electronic_structure['basis'] = None
        self.method_electronic_structure['df_basis'] = None

# setters
    def set_print_level(self, level):
        assert isinstance(level, str), "Print level must be a string."
        assert level.lower() in print_level, f"Print level must be one of {print_level}."
        self.print_level = level

    def turn_on_switch(self, method):
        assert isinstance(method, str), "Method must be a string."
        method = method.lower()
        assert method in optional_standalone, f"Method must be one of {optional_standalone}."
        self.method_optional_standalone[method] = True

    def turn_off_switch(self, method):
        assert isinstance(method, str), "Method must be a string."
        method = method.lower()
        assert method in optional_standalone, f"Method must be one of {optional_standalone}."
        self.method_optional_standalone[method] = False

    def set_electronic_structure_method(self, method, value):
        """setting method value for keys in electronic_structure_method"""
        assert isinstance(value, str), "Value must be a string."
        assert isinstance(method, str), "Method must be a string."
        method = method.lower()
        assert method in electronic_structure_method, f"Method must be one of {electronic_structure_method}."
        assert value.lower() in electronic_structure_method[method], f"Value must be one of {electronic_structure_method[method]}."
        self.method_electronic_structure[method] = value
    
    def unset_electronic_structure_method(self, method):
        assert isinstance(method, str), "Method must be a string."
        method = method.lower()
        assert method in electronic_structure_method, f"Method must be one of {electronic_structure_method}."
        self.method_electronic_structure[method] = None

    def set_optional_withvalue(self, method, value):
        """setting method value for keys in optional_withvalue"""
        assert isinstance(value, str), "Value must be a string."
        assert isinstance(method, str), "Method must be a string."
        method = method.lower()
        assert method in optional_withvalue, f"Method must be one of {optional_withvalue}."
        assert value in optional_withvalue[method], f"Value must be one of {optional_withvalue[method]}."
        self.method_optional_withvalue[method] = value
    
    def unset_optional_withvalue(self, method):
        assert isinstance(method, str), "Method must be a string."
        method = method.lower()
        assert method in optional_withvalue, f"Method must be one of {optional_withvalue}."
        self.method_optional_withvalue[method] = None

    def add_other_option(self, option):
        if not isinstance(option, str):
            option = str(option)
        option = option.lower()
        assert option not in self.other_options, f"Option '{option}' is already in the list."
        self.other_options.append(option)

    def remove_other_option(self, option):
        if not isinstance(option, str):
            option = str(option)
        option = option.lower()
        assert option in self.other_options, f"Option '{option}' is not in the list."
        self.other_options.remove(option)

    def clear_other_options(self):
        self.other_options = []
    
    def sanity_check(self):
        assert self.method_electronic_structure['theory'] is not None, "Electronic structure theory method must be set."
        assert self.method_electronic_structure['basis'] is not None, "Electronic structure basis set must be set."


# input line generators
    def generate_print_level_string(self):
        if self.print_level is None:
            return ""
        else:
            return self.print_level

    def generate_electronic_structure_method_string(self):
        self.sanity_check()
        if self.method_electronic_structure['df_basis'] is not None:
            return f"{self.method_electronic_structure['theory']}/{self.method_electronic_structure['basis']}/{self.method_electronic_structure['df_basis']}"
        return f"{self.method_electronic_structure['theory']}/{self.method_electronic_structure['basis']}"

    def generate_switch_string(self):
        if len(self.method_optional_standalone) == 0:
            return ""
        else:
            """
            if the value of the key is True, add the key to the string to return
            """
            return " ".join(key for key, value in self.method_optional_standalone.items() if value)
    
    def generate_optional_withvalue_string(self):
        if len(self.method_optional_withvalue) == 0:
            return ""
        else:
            """
            add key=value for optional methods
            """
            return " ".join(f"{key}={value}" for key, value in self.method_optional_withvalue.items())
        
    def generate_other_options_string(self):
        if len(self.other_options) == 0:
            return ""
        else:
            return " ".join(self.other_options)
    
    def generate_full_method_string(self):
        self.sanity_check()
        method_parts = [
            f"#{self.generate_print_level_string()}",
            self.generate_electronic_structure_method_string(),
            self.generate_switch_string(),
            self.generate_optional_withvalue_string(),
            self.generate_other_options_string()
        ]
        # Filter out empty strings and join with spaces
        full_method_string = " ".join(part for part in method_parts if part)
        return full_method_string.strip()
    
    @staticmethod
    def convert_gaussian_input_line_to_array(string):
        assert isinstance(string, str), "Input must be a string."
        assert string.startswith("#"), "Input line must start with '#'."
        inputs = string.strip().split()
        assert len(inputs) > 1, f"Failed to obtain any information from {string}"
        return inputs

# input line processors
    def get_print_level_from_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert len(array) > 1, "Input list must contain at least 2 elements."
        if array[0][1:].lower() in print_level:
            self.set_print_level(array[0])

    def get_electronic_structure_method_from_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert len(array) > 1, "Input list must contain at least 2 elements."
        assert '/' in array[1], f"Electronic structure method must contain '/'."
        theory, basis, *df_basis = array[1].split('/')
        self.set_electronic_structure_method('theory', theory)
        self.set_electronic_structure_method('basis', basis)
        if df_basis:
            self.set_electronic_structure_method('df_basis', df_basis)

    def is_string_the_start(self, string):
        assert isinstance(string, str), "Input must be a string."
        return string.startswith('#')
    
    def is_string_the_method_part(self, string):
        assert isinstance(string, str), "Input must be a string."
        return '/' in string and string.strip().split('/')[0].lower() in electronic_structure_method['theory']

    def is_string_a_switch(self, string):
        assert isinstance(string, str), "Input must be a string."
        return string.lower() in optional_standalone
    
    def is_string_an_optional_withvalue(self, string):
        assert isinstance(string, str), "Input must be a string."
        return string.split('=')[0] in optional_withvalue
    
    def is_string_an_other_option(self, string):
        assert isinstance(string, str), "Input must be a string."
        if string.lower() in optional_standalone:
            return False
        if string.split('=')[0] in optional_withvalue:
            return False
        if '/' in string:
            return False
        if string.startswith('#'):
            return False
        return True

    def get_non_es_options_in_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        for item in array:
            if self.is_string_an_other_option(item):
                continue
            elif self.is_string_the_method_part(item):
                continue
            elif self.is_string_a_switch(item):
                self.turn_on_switch(item)
            elif self.is_string_an_optional_withvalue(item):
                key, value = item.split('=')
                self.set_optional_withvalue(key, value)
            else:
                self.add_other_option(item)
    
    def process_gaussian_input_line(self, string):
        assert isinstance(string, str), "Input must be a string."
        assert string.startswith("#"), "Input line must start with '#'."
        # add a safe to remove the trailing \n or space in the string, in
        # case it is obtained from a file.
        string = string.strip()
        input_array = self.convert_gaussian_input_line_to_array(string)
        self.get_print_level_from_array(input_array)
        self.get_electronic_structure_method_from_array(input_array)
        self.get_non_es_options_in_array(input_array)

    def process_gaussian_input_file(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        assert os.path.isfile(filename), f"File {filename} does not exist."
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("#"):
                    # Process Gaussian input line
                    # Note that the string line may end with '\n', so we need to
                    # remove it
                    self.process_gaussian_input_line(line.strip())

    # data structure printers
    def show_current_settings(self):
        print("Current settings:")
        print(f"Print level: {self.print_level}")
        print(f"Electronic structure method: {self.method_electronic_structure}")
        print(f"Switches: {self.method_optional_standalone}")
        print(f"Optional methods: {self.method_optional_withvalue}")
        print(f"Other options: {self.other_options}")
        print(f"Full method string: {self.generate_full_method_string()}")
    
    def save_current_settings_to_json(self, filename):
        """this function dumps the current settings to a json file"""
        assert isinstance(filename, str), "Filename must be a string."
        assert filename.endswith('.json'), "Filename must end with .json"
        with open(filename, 'w') as f:
            json.dump({
                "print_level": self.print_level,
                "method_electronic_structure": self.method_electronic_structure,
                "method_optional_standalone": self.method_optional_standalone,
                "method_optional_withvalue": self.method_optional_withvalue,
                "other_options": self.other_options
            }, f, indent=4)

    # data structure reader (from a json file)
    def get_current_settings_from_json(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        assert filename.endswith('.json'), "Filename must end with .json"
        assert os.path.isfile(filename), f"File {filename} does not exist."
        with open(filename, 'r') as f:
            data = json.load(f)
            self.print_level = data['print_level']
            self.method_electronic_structure = data['method_electronic_structure']
            self.method_optional_standalone = data['method_optional_standalone']
            self.method_optional_withvalue = data['method_optional_withvalue']
            self.other_options = data['other_options']
