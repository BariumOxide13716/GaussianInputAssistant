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
            parts = item.split()
            assert len(parts) == 4, "Each line must contain an atom and three coordinates."
            atom = parts[0].capitalize()
            assert atom in periodic_table, f"Atom {atom} is not recognized."
            try:
                coord = [float(x) for x in parts[1:4]]
            except ValueError:
                raise ValueError("Coordinates must be numeric values.")
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