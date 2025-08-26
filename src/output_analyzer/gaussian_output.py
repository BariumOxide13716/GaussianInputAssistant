'''
This file is a class for holding the output data, and it inherits from
the class GaussianInput gaussian_input.
'''
import os
from input_modifier.gaussian_input import GaussianInput as gi
from utils.string_util import convert_array_to_string
from utils.list_util import search_array_string_elements
from utils.pygrep import py_grep
from utils.logger import Logger
from .output_parameters import output_parameters

class GaussianOutput(gi):
    """
    Class for holding the output data from a Gaussian calculation.
    """
    def __init__(self):
        super().__init__()
        self._output_file = None
        self._file_name = None
        self._extension = None
        self._termination_status = None
        self.results = {}
        for key in output_parameters:
            self.results[key] = None

        self._logger = Logger("gaussian_output_log.txt")

        self._gaussian_normal_termination_string = "Normal termination of Gaussian"

    def set_output_file(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        self._output_file = filename
        self._file_name, self._extension = os.path.splitext(filename)

    def check_calculation_termination_status(self):
        assert self._output_file is not None, "Output file must be set before checking termination."
        results, return_code = py_grep(self._gaussian_normal_termination_string, self._output_file)
        if return_code == -1 or len(results) == 0:
            self._termination_status = False
            return False
        else:
            self._termination_status = True
            return True
        
    def get_termination_status(self):
        return self._termination_status
    
    def get_output_results(self):
        assert self._output_file is not None, "Output file must be set before getting input."
        assert self._termination_status is True, "Calculation must be successfully terminated before getting input."
        results, return_code = py_grep("\\", self._output_file)
        if return_code == -1 or len(results) == 0:
            self._logger.log_highlight(f"No input section found in output: {self._output_file}")
            return None
        
        # get the items in the dictionary results
        results_array = list(results.values())

        results_string = convert_array_to_string(results_array, connecting_char='', char_to_strip=' \n')
        results_array = results_string.split('\\')

        input_array = self.get_input_array_from_output_array(results_array)
        self.read_gaussian_input_from_string(input_array[0])
        self.read_geometry_from_geometry_array(input_array[2:])
        self.read_gaussian_output_from_array(self.get_output_array_from_output_array(results_array))

    
    def get_input_array_from_output_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert all(isinstance(item, str) for item in array), "All items in the list must be strings."

        # Search for '#' in the array to mark the starting index for the input in the array
        indices_list = search_array_string_elements(array, starting_string='#')
        assert indices_list['starting'], "No starting indices found."
        input_start_index = indices_list['starting'][0]

        # Search for 'Version=' in the array to mark the ending index for the input in the array and the results
        indices_list = search_array_string_elements(array, starting_string='Version=')
        assert indices_list['starting'], "No ending indices found."
        input_end_index = indices_list['starting'][0]

        # Extract the input section from the array
        input_section = array[input_start_index:input_end_index]
        return input_section
    
    def get_output_array_from_output_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert all(isinstance(item, str) for item in array), "All items in the list must be strings."

        # Search for 'Version=' in the array to mark the starting index for the output in the array
        indices_list = search_array_string_elements(array, starting_string='Version=')
        assert indices_list['starting'], "No starting indices found."
        output_start_index = indices_list['starting'][0]
        return array[output_start_index:]
    
    def read_gaussian_output_from_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert all(isinstance(item, str) for item in array), "All items in the list must be strings."
        assert array[0].startswith('Version='), "Array must start with 'Version='."

        # Read the output parameters from the array
        for item in array[1:]:
            if '=' not in item:
                continue
            key, value = item.split('=')
            key = key.strip()
            value = value.strip()
            if key in output_parameters:
                if ',' in value:
                    self.results[key] = value.split(',')
                else:
                    self.results[key] = value

