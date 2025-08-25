"""
this class is a container for the system controls in a gaussian input file
"""

from input_parameters import system_control
import os
import json

class SystemControl():

    required_system_control = [ ### the required system controls
        'chk'
    ]

    def __init__(self):
        self.system_control = {}
        for key in system_control:
            self.system_control[key] = None

    # setter
    def set_system_control(self, key, value):
        assert isinstance(key, str), "Key must be a string."
        key = key.lower()
        assert key in self.system_control, f"Invalid system control key: {key}"
        self.system_control[key] = value

    # getter
    def get_system_control(self, key):
        assert isinstance(key, str), "Key must be a string."
        key = key.lower()
        assert key in self.system_control, f"Invalid system control key: {key}"
        return self.system_control[key]
    
    # reader
    def read_system_control_from_string(self, string):
        assert isinstance(string, str), "Input must be a string."
        assert string.startswith("%"), "Input line must start with '%'."
        inputs = string[1:].strip().split('=')
        assert len(inputs) > 1, f"Failed to obtain any information from {string}"
        key = inputs[0][1:].lower()
        value = inputs[1]
        self.set_system_control(key, value)
    
    def read_system_control_from_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        for item in array:
            self.read_system_control_from_string(item.strip())
    
    def read_system_control_from_file(self, filename):
        assert os.path.isfile(filename), f"File {filename} does not exist."
        with open(filename, 'r') as file:
            lines = file.readlines()
        self.read_system_control_from_array(lines)
    
    # data structure printers
    def show_current_settings(self):
        print("Current settings for system control:")
        for key in self.system_control:
            print(f"{key}: {self.system_control[key]}")

    def sanity_check(self):
        for key in self.required_system_control:
            assert key in self.system_control, f"Missing required system control: {key}"
            assert self.system_control[key] is not None, f"System control {key} is not set."

    def pack_current_settings_to_dict(self):
        return self.system_control

    def save_current_settings_to_json(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        assert filename.endswith('.json'), "Filename must end with .json"
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data_in_file = json.load(f)
        else:
            data_in_file = {}
        data_in_file['system_control'] = self.pack_current_settings_to_dict()
        with open(filename, 'w') as file:
            json.dump(data_in_file, file, indent=4)

    # data structure getter
    def get_current_settings_from_json(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        assert filename.endswith('.json'), "Filename must end with .json"
        assert os.path.isfile(filename), f"File {filename} does not exist."

        with open(filename, 'r') as file:
            data = json.load(file).get('system_control', None)
        if data is None:
            print(f"No system-control information found in {filename}.")
        else:
            for key in system_control:
                self.system_control[key] = data.get(key, None)

    # input line generators
    def generate_system_control_string(self):
        self.sanity_check()
        display_in_file = ""
        for key in system_control:
            if key in self.system_control and self.system_control[key] is not None:
                display_in_file += f"%{key}={self.system_control[key]}\n"
        return display_in_file