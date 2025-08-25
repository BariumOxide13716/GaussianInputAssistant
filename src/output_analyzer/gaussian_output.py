'''
This file is a class for holding the output data, and it inherits from
the class GaussianInput gaussian_input.
'''

from input_modifier.gaussian_input import GaussianInput as gi
from utils.pygrep import py_grep
from utils.logger import IOUtil as ioutil

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

        self._logger = ioutil("gaussian_output_log.txt")

        self._gaussian_normal_termination_string = "Normal termination of Gaussian"

    def set_output_file(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        self._output_file = filename
        self._file_name, self._extension = self.get_file_name_and_extension(filename)

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
    
    def get_input_from_output(self):
        """
        This part retrieves the input section from the output file.
        It identifies the first line with multiple backward slashes using py_grep,
        and get the information starting from this line till the first blank line.
        
        It removes the "new line" signs in this information, split it by the 
        backward slashes. 
        """
        assert self._output_file is not None, "Output file must be set before getting input."
        assert self._termination_status is True, "Calculation must be successfully terminated before getting input."

        results, return_code = py_grep(r"\\", self._output_file)
        if return_code == -1 or len(results) == 0:
            self._logger.log_warning(f"No input section found in output: {self._output_file}")
            return None

        start_line = min(results.keys())
        end_line = start_line
        for line_number in range(start_line + 1, len(results) + 1):
            if line_number not in results:
                end_line = line_number - 1
                break

        input_section = []
        for line_number in range(start_line, end_line + 1):
            input_section.append(results[line_number].strip())

        return input_section
