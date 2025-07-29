# This file is a class that stores input parameters for Gaussian calculations.
# It uses a dictionary to hold the parameters and provides methods to set and get them.

'''
As it is in a premature stage, the input file is assumed to be as follows:
%chk = path/to/checkfile.chk
%nprocshared = 1
%mem = 1GB
# method/basis

title

charge multiplicity
atom_xyz

'''
import numpy as np
import os
from input_keys import required_input, optional_input, system_control

class GaussianInput:
    def __init__(self):
        self._input_parameters = {}
        self._system_controls = {}
        # set default value for chkpath to the chkpoint file
        # where the script is running
        self._system_controls['chk'] = 'my_calculation.chk'
        self._input_parameters['method'] = 'hf'
        self._input_parameters['basis'] = 'sto-3g'
        self._input_parameters['charge'] = 0
        self._input_parameters['multiplicity'] = 1
        self._input_parameters['title'] = 'Gaussian Calculation'
        self._input_parameters['atoms'] = np.array([])
        self._input_parameters['coordinates'] = np.array([])
        self._input_parameters['optimization'] = None
        self._input_parameters['stable'] = None
        self._input_parameters['print_level'] = 'N'  # default print level

    def set_calculation_parameter(self, key, value):
        """Set a parameter for the Gaussian calculation."""
        if key in required_input or key in optional_input:
            if key in self._input_parameters:
                self._input_parameters[key] = value
            else:
                raise KeyError(f"Invalid input parameter: {key}")
        else:
            raise KeyError(f"Invalid input parameter: {key}. Must be one of {required_input + optional_input}.")
        
    def set_atoms(self, atoms):
        """Set the atoms for the Gaussian calculation."""
        if isinstance(atoms, (list, np.ndarray)):
            self._input_parameters['atoms'] = np.array(atoms)
        else:
            raise TypeError("Atoms must be a list or numpy array.")
        
    def set_coordinates(self, coordinates):
        """Set the coordinates for the Gaussian calculation."""
        if isinstance(coordinates, (list, np.ndarray)):
            self._input_parameters['coordinates'] = np.array(coordinates)
        else:
            raise TypeError("Coordinates must be a list or numpy array.")
    
    def set_system_control_parameter(self, key, value):
        """Set a system control parameter."""
        if key in system_control:
            self._system_controls[key] = value
        else:
            raise KeyError(f"Invalid system control parameter: {key}")
        
    def get_print_level(self, input_str):
        """get the printing level from the input string."""
        assert isinstance(input_str, str), "Input must be a string."

        if not input_str.startswith('#'):
            raise ValueError("Input string does not start with '#' for print level extraction.")
        
        input_str = input_str.lower()
        # check whether the second letter in the string is one of T, N, P, or a ' ',
        # if false, raise an error; otherwise, return the second letter. If the second letter is ' ', return 'N'.
        if len(input_str) < 2 or input_str[1].lower() not in 'tnp ':
            raise ValueError("Invalid print level in input string.")
        return input_str[1] if input_str[1] != ' ' else 'N'
                    
    def get_method_basis(self, input_str):
        """Extract method and basis from the input string."""
        assert isinstance(input_str, str), "Input must be a string."
        if not input_str.startswith('#'):
            raise ValueError("Input string does not start with '#' for method/basis extraction.")
        input_str = input_str.lower()
        # split the string by spaces, and look for the second element for method/basis
        parts = input_str.split()
        if len(parts) < 2:
            raise ValueError(f" {str}\n Input string does not contain enough information for method/basis extraction.")
        if '/' not in parts[1]:
            raise ValueError(f" {str}\n Input string does not contain a valid method/basis format.\n Expecting \"<method>/<basis> right after the '#' character.")
        method_basis = parts[1].split('/')
        if len(method_basis) != 2:
            raise ValueError(f" {str}\n Input string does not contain a valid method/basis format.\n Expecting \"<method>/<basis> right after the '#' character.")
        return method_basis[0].strip(), method_basis[1].strip()
    
    def get_optimization_requirement(self, input_str):
        """Check if the geometry optimizaiton keyword is present in the input string."""
        assert isinstance(input_str, str), "Input must be a string."
        if not input_str.startswith('#'):
            raise ValueError("Input string does not start with '#' for optimization extraction.")
        input_str = input_str.lower()
        parts = input_str.split()
        if len(parts) < 3:
            return None
        # loop over the elements in the parts list, 
        # if an element is 'opt', return 'opt';
        # if an element starts with 'opt=', the element
        for part in parts:
            if part.startswith('opt=') or part == 'opt':
                return part
        return None
    
    def get_stable_requirement(self, input_str):
        """Check if the stable keyword is present in the input string."""
        assert isinstance(input_str, str), "Input must be a string."
        if not input_str.startswith('#'):
            raise ValueError("Input string does not start with '#' for stability extraction.")
        input_str = input_str.lower()
        parts = input_str.split()
        if len(parts) < 3:
            return None
        # loop over the elements in the parts list,
        # if an element is 'stable', return 'stable'
        for part in parts:
            if part == 'stable':
                return part
        return None
    
    def get_charge_multiplicity(self, input_str):
        """Extract charge and multiplicity from the input string."""
        assert isinstance(input_str, str), "Input must be a string."
        parts = input_str.split()
        if len(parts) != 2:
            raise ValueError(f"Expecting two values in the line for charge and multiplicity, " +
                             f"got the following instead.\n{input_str}")
        try:
            charge = int(parts[0])
            multiplicity = int(parts[1])
        except ValueError:
            raise ValueError("Charge and multiplicity must be integers.")
        return charge, multiplicity
    
    def get_atoms_and_coordinates(self, lines):
        """Extract atoms and coordinates from the remaining lines."""
        assert isinstance(lines, list), "Input must be a list of strings."
        atoms = []
        coordinates = []
        
        for line in lines:
            line = line.strip()
            if not line:
                return np.array(atoms), np.array(coordinates)
            parts = line.split()
            if len(parts) < 4:
                raise ValueError(f"Invalid atom line: {line}. Expecting at least 4 parts (atom symbol and 3 coordinates).")
            atom = parts[0]
            try:
                coords = [float(coord) for coord in parts[1:4]]
            except ValueError:
                raise ValueError(f"Invalid coordinates in line: {line}. Coordinates must be floats.")
            atoms.append(atom)
            coordinates.append(coords)
        
        return np.array(atoms), np.array(coordinates)
        
    def print_parameters(self):
        """Print the input parameters for the Gaussian calculation."""
        print("Input Parameters:")
        for key, value in self._input_parameters.items():
            print(f"{key}: {value}")
        print("\nSystem Control Parameters:")
        for key, value in self._system_controls.items():
            print(f"{key}: {value}")

    def save_gaussian_input_file(self, filename):
        """ Save the Gaussian input parameters to a file.
            if filename exists, rename filename to filename.bak_date,
            and show a warning to the user.
        """

        assert len(self._input_parameters['atoms']) > 0, "No atoms specified in the input parameters."
        assert len(self._input_parameters['coordinates']) > 0, "No coordinates specified in the input parameters."
        assert len(self._input_parameters['atoms']) == len(self._input_parameters['coordinates']), \
            "Number of atoms and coordinates do not match."

        if os.path.exists(filename):
            backup_filename = f"{filename}.bak_{np.datetime64('now', 's')}"
            os.rename(filename, backup_filename)
            print(f"Warning: {filename} already exists. Renamed to {backup_filename}.")

        with open(filename, 'w') as f:
            # write system control parameters
            for key, value in self._system_controls.items():
                f.write(f"%{key} = {value}\n")
            
            # write method and basis
            method = self._input_parameters['method']
            basis = self._input_parameters['basis']
            print_level = self._input_parameters.get('print_level', 'N')
            f.write(f"#{print_level} {method}/{basis} ")
            if self._input_parameters['optimization'] is not None:
                f.write(f"{self._input_parameters['optimization']} ")
            if self._input_parameters['stable'] is not None:
                f.write(f"{self._input_parameters['stable']} ")
            f.write("\n\n")
            
            # write title
            title = self._input_parameters['title']
            f.write(f"{title}\n\n")
            
            # write charge and multiplicity
            charge = self._input_parameters['charge']
            multiplicity = self._input_parameters['multiplicity']
            f.write(f"{charge} {multiplicity}\n")
            
            # write atoms and coordinates
            atoms = self._input_parameters['atoms']
            coordinates = self._input_parameters['coordinates']
            for atom, coord in zip(atoms, coordinates):
                f.write(f"{atom} {' '.join(map(str, coord))}\n")
            
            # write a blank line at the end
            f.write("\n")

    def read_gaussian_input_file(self, filename):
        """Read Gaussian input from a file."""
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        if_method_details_read = False

        # as the Gaussian input file is organized in a specific way,
        # namely first few lines are for system control parameters,
        # then the method, basis and other method details,
        # then a space,
        # then the title,
        # the another space,
        # then the charge and multiplicity,
        # at last a bunch of lines for atoms and coordinates,
        # and finally a blank line,
        # we can read the file line by line and extract the information.

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            if line.startswith('%'):
                # system control parameters
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip('%').strip().lower()
                    value = value.strip()
                    self.set_system_control_parameter(key, value)
                
            elif line.startswith('#'):
                # method and basis
                assert not if_method_details_read, "Method and basis details already read."

                print_level = self.get_print_level(line)
                self.set_calculation_parameter('print_level', print_level)

                method, basis = self.get_method_basis(line)
                self.set_calculation_parameter('method', method)
                self.set_calculation_parameter('basis', basis)

                require_optimization = self.get_optimization_requirement(line)
                self.set_calculation_parameter('optimization', require_optimization)

                require_stable = self.get_stable_requirement(line)
                self.set_calculation_parameter('stable', require_stable)

                if_method_details_read = True

                # by this time we should have read the method and basis.
                # then we skipt the loop, and manually read the following lines
                iline_method_details = i
                break

        title = lines[iline_method_details + 2]
        self.set_calculation_parameter('title', title)
        
        charge, multiplicity = self.get_charge_multiplicity(lines[iline_method_details + 4])
        self.set_calculation_parameter('charge', charge)
        self.set_calculation_parameter('multiplicity', multiplicity)

        # at last, use the remaining lines to read the atoms and the coordinates
        atoms, coordinates = self.get_atoms_and_coordinates(lines[iline_method_details + 5:])
        assert len(atoms) == len(coordinates), "Number of atoms and coordinates do not match."
        if len(atoms) == 0 or len(coordinates) == 0:
            raise ValueError("No atoms or coordinates found in the input file.")
        self.set_calculation_parameter('atoms', atoms)
        self.set_calculation_parameter('coordinates', coordinates)




            

            

                



