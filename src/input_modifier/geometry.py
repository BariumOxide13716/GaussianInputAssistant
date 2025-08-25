"""
This class stores the geometry part in a gaussian input file,
starting from the title section.

For current purpose, it works with Cartisian coordinates
"""

import os
import json
import numpy as np
from ..constants.periodic_table import periodic_table
from input_parameters import input_geometry

class Geometry:

    required_keys = {
        'charge',
        'multiplicity',
        'atoms',
        'coordinates'
    }

    def __init__(self):
        self.geometry = {}
        for key in input_geometry:
            self.geometry[key] = None
    
    # setters
    def set_title(self, title):
        assert isinstance(title, str), "Title must be a string."
        self.geometry['title'] = title

    def set_charge(self, charge):
        assert isinstance(charge, int), "Charge must be an integer."
        self.geometry['charge'] = charge

    def set_multiplicity(self, multiplicity):
        assert isinstance(multiplicity, int), "Multiplicity must be an integer."
        self.geometry['multiplicity'] = multiplicity

    def set_coordinates(self, coordinates):
        assert isinstance(coordinates, (np.ndarray, list)), "Coordinates must be a numpy array."
        if self.geometry['atoms'] is not None:
            assert len(coordinates) == len(self.geometry['atoms']), "Coordinates must match the number of atoms."
        self.geometry['coordinates'] = np.array(coordinates) if not isinstance(coordinates, np.ndarray) else coordinates
    
    def set_atoms(self, atoms):
        assert isinstance(atoms, list), "Atoms must be a list."
        for atom in atoms:
            assert isinstance(atom, str), "Each atom must be a string."
            assert atom.capitalize() in periodic_table, f"Atom {atom} is not recognized."
        self.geometry['atoms'] = atoms

    def add_atom(self, atom):
        assert isinstance(atom, str), "Atom must be a string."
        assert atom.capitalize() in periodic_table, f"Atom {atom} is not recognized."
        if self.geometry['atoms'] is None:
            self.geometry['atoms'] = []
        self.geometry['atoms'].append(atom.capitalize())
    
    def add_coordinate(self, coordinate):
        assert isinstance(coordinate, (list, np.ndarray)), "Coordinate must be a list or numpy array."
        assert len(coordinate) == 3, "Coordinate must have three elements."
        if self.geometry['coordinates'] is None:
            self.geometry['coordinates'] = np.array([coordinate]) if not isinstance(coordinate, np.ndarray) else coordinate.reshape(1, 3)
        else:
            self.geometry['coordinates'] = np.vstack([self.geometry['coordinates'], np.array(coordinate) if not isinstance(coordinate, np.ndarray) else coordinate.reshape(1, 3)])

    def clear_atoms(self):
        self.geometry['atoms'] = None
    
    def clear_coordinates(self):
        self.geometry['coordinates'] = None

    # getters
    def get_title(self):
        return self.geometry['title']

    def get_charge(self):
        return self.geometry['charge']

    def get_multiplicity(self):
        return self.geometry['multiplicity']

    def get_coordinates(self):
        return self.geometry['coordinates']

    def get_atoms(self):
        return self.geometry['atoms']

    # readers
    def read_atoms_and_coordinates_from_string(self, string):
        assert isinstance(string, str), "Input must be a string."
        lines = string.strip().split("\n")
        for line in lines:
            parts = line.split()
            assert len(parts) == 4, "Each line must contain an atom and three coordinates."
            atom = parts[0].capitalize()
            assert atom in periodic_table, f"Atom {atom} is not recognized."
            try:
                coord = [float(x) for x in parts[1:4]]
            except ValueError:
                raise ValueError("Coordinates must be numeric values.")
            return atom, coord

    def read_atoms_and_coordinates_from_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert len(array) > 0, "Input list must contain at least 1 element"
        for i in range(len(array)):
            assert isinstance(array[i], str), "Each item in the list must be a string."
        for i in range(len(array)):    
            array[i] = array[i].strip()
        self.clear_atoms()
        self.clear_coordinates()
        for item in array:
            if item == "":
                continue
            assert isinstance(item, str), "Each item in the list must be a string."
            atom, coord = self.read_atoms_and_coordinates_from_string(item)
            self.add_atom(atom)
            self.add_coordinate(coord)

    def read_geometry_from_geometry_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert len(array) > 3, "Input list must contain at least 4 elements."

        for i in range(len(array)):
            assert isinstance(array[i], str), "Each item in the list must be a string."
        for i in range(len(array)):
            array[i] = array[i].strip()

        self.set_title(array[0])
        multiplicity, charge = array[2].split()
        self.set_multiplicity(int(multiplicity))
        self.set_charge(int(charge))
        self.read_atoms_and_coordinates_from_array(array[3:])

    def read_geometry_from_input_array(self, array):
        assert isinstance(array, list), "Input must be a list."
        assert len(array) > 3, "Input list must contain at least 4 elements."

        for i in range(len(array)):
            assert isinstance(array[i], str), "Each item in the list must be a string."
        for i in range(len(array)):
            array[i] = array[i].strip()

        for i, item in enumerate(array):
            if item.startswith('#'):
                iline = i
                break
        
        self.read_geometry_from_geometry_array(array[iline+1:])

    def read_geometry_from_file(self, filename):
        assert os.path.isfile(filename), f"File {filename} does not exist."
        with open(filename, 'r') as file:
            lines = file.readlines()
        self.read_geometry_from_input_array(lines)

    # geometry part generator
    def sanity_check(self):
        for key in self.required_keys:
            assert self.geometry[key] is not None, f"{key} is not set."
        assert len(self.geometry['atoms']) == len(self.geometry['coordinates']), "Number of atoms and coordinates must match."

    def generate_geometry_string(self):
        self.sanity_check()

        if self.geometry['title'] is None:
            self.geometry['title'] = " "
        
        display_in_file = ""
        display_in_file += f"{self.geometry['title']}\n"
        display_in_file += "\n"
        display_in_file += f"{self.geometry['multiplicity']} {self.geometry['charge']}\n"
        for atom, coord in zip(self.geometry['atoms'], self.geometry['coordinates']):
            display_in_file += f"{atom} {coord[0]:.6f} {coord[1]:.6f} {coord[2]:.6f}\n"
        display_in_file += "\n"
        return display_in_file

    # data structure printers
    def show_current_settings(self):
        print("Current settings for geometry:")
        print(f"Title: {self.geometry['title']}")
        print()
        print(f"Multiplicity: {self.geometry['multiplicity']}")
        print(f"Charge: {self.geometry['charge']}")
        print("Atoms and Coordinates:")
        for atom, coord in zip(self.geometry['atoms'], self.geometry['coordinates']):
            print(f"  {atom}: {coord[0]:.6f}, {coord[1]:.6f}, {coord[2]:.6f}")

    def pack_current_settings_to_dict(self):
        current_settings = {
            "title": self.geometry['title'],
            "multiplicity": self.geometry['multiplicity'],
            "charge": self.geometry['charge'],
            "atoms": self.geometry['atoms'],
            "coordinates": self.geometry['coordinates']
        }
        return current_settings

    def save_current_settings_to_json(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        assert filename.endswith('.json'), "Filename must end with .json"
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data_in_file = json.load(f)
        else:
            data_in_file = {}
        data_in_file['geometry'] = self.pack_current_settings_to_dict()
        with open(filename, 'w') as f:
            json.dump(data_in_file, f, indent=4)

    # data structure reader (from a json file)
    def get_current_settings_from_json(self, filename):
        assert isinstance(filename, str), "Filename must be a string."
        assert filename.endswith('.json'), "Filename must end with .json"
        assert os.path.isfile(filename), f"File {filename} does not exist."
        with open(filename, 'r') as f:
            data = json.load(f).get('geometry', None)
        if data is None:
            print(f"No geometry information found in {filename}.")
        else:
            for key in input_geometry:
                self.geometry[key] = data.get(key, None)
