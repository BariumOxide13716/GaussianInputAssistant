"""
This class integrates system_control, calculation methods, and geometry
"""

import os
from .system_control import SystemControl as SysCon
from .calculation_methods import CalculationMethods as CalMeth
from .gaussian_geometry import Geometry as Geom

class GaussianInput(SysCon, CalMeth, Geom):
    def __init__(self):
        SysCon.__init__(self)
        CalMeth.__init__(self)
        Geom.__init__(self)
    
    
    # setters
    # some of them should have been defined in the base classes

    # readers
    def read_input_from_file(self, filename):
        assert os.path.isfile(filename), f"File {filename} does not exist."

        self.read_system_control_from_file(filename) # defined in SystemControl
        self.read_gaussian_input_from_file(filename) # defined in CalculationMethods
        self.read_geometry_from_file(filename) # defined in Geometry

    # input file generator
    def generate_gaussian_input_string(self):
        input_string = ""
        input_string += self.generate_system_control_string()
        input_string += self.generate_calculation_methods_string()
        input_string += '\n'
        input_string += self.generate_geometry_string()
        return input_string

    def generate_gaussian_input_file(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        with open(filename, 'w') as f:
            f.write(self.generate_gaussian_input_string())

    # data structure printers
    def show_current_settings(self):
        SysCon.show_current_settings(self)
        CalMeth.show_current_settings(self)
        Geom.show_current_settings(self)
    
    # data structure saver
    def save_current_settings_to_json(self, filename):
        assert os.path.exists(filename), f"File {filename} does not exist."
        assert filename.endswith(".json"), "Filename must end with .json"
        SysCon.save_current_settings_to_json(self, filename)
        CalMeth.save_current_settings_to_json(self, filename)
        Geom.save_current_settings_to_json(self, filename)
    
    # data structure getter
    def get_current_settings_from_json(self, filename):
        assert os.path.exists(filename), f"File {filename} does not exist."
        assert filename.endswith(".json"), "Filename must end with .json"
        SysCon.get_current_settings_from_json(self, filename)
        CalMeth.get_current_settings_from_json(self, filename)
        Geom.get_current_settings_from_json(self, filename)