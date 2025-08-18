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
try:
    from input_keys import required_input, optional_input, system_control
except ImportError:
    try:
        from .input_keys import required_input, optional_input, system_control
    except ImportError:
        raise ImportError("Could not import required input keys. Ensure input_keys.py is in the same directory or accessible in the Python path.")

class GaussianInput:
    def __init__(self):
        self._input_parameters = {}
        self._system_controls = {}
        
        for key in required_input:
            self._input_parameters[key] = None
        for key in optional_input:
            self._input_parameters[key] = None
        for key in system_control:
            self._system_controls[key] = None
        # set default value for chkpath to the chkpoint file
        # where the script is running
        self._system_controls['chk'] = 'my_calculation.chk'
        self._system_controls['nprocshared'] = 1
        self._system_controls['mem'] = '1GB'

        self._input_parameters['title'] = 'Gaussian Calculation'
        self._input_parameters['print_level'] = 'N'  # default print level

        self._minimum_required_input_element = 1

    def get_info_in_method_line(self, input_str):
        """Check if the input string starts with a valid method line."""
        assert isinstance(input_str, str), "Input must be a string."
        if not input_str.startswith('#'):
            raise ValueError("Input string does not start with '#' for method line check.")
        if input_str.strip() == '#':
            raise ValueError("Input string is empty after '#' for method line check.")
        
        return input_str[1:].strip()

    def set_calculation_parameter(self, key, value):
        """Set a parameter for the Gaussian calculation."""
        if key in required_input or key in optional_input:
            if key in self._input_parameters:
                self._input_parameters[key] = value
            else:
                raise KeyError(f"Invalid input parameter: {key}")
        else:
            raise KeyError(f"Invalid input parameter: {key}. Must be one of {required_input + optional_input}.")

    def get_calculation_parameter(self, key):
        """Get a parameter for the Gaussian calculation."""
        if key in self._input_parameters:
            return self._input_parameters[key]
        else:
            raise KeyError(f"Invalid input parameter: {key}. Must be one of {required_input + optional_input}.")

    def get_system_control_parameter(self, key):
        """Get a system control parameter."""
        if key in self._system_controls:
            return self._system_controls[key]
        else:
            raise KeyError(f"Invalid system control parameter: {key}. Must be one of {system_control}.")

    def are_all_required_parameters_set(self):
        """Check if all required parameters are set."""
        assert isinstance(self._input_parameters, dict), "Input parameters must be a dictionary."
        all_required_parameters_set = True
        for key in required_input:
            if key not in self._input_parameters or self._input_parameters[key] is None:
                print(f"Required input parameter '{key}' is not set.")
                all_required_parameters_set = False       
        return all_required_parameters_set

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
        input_str = self.get_info_in_method_line(input_str)
        first_element = input_str.lower().split()[0]
        # if the first element is 'n', 'p', or 't', then it is a print level
        if first_element in [ 'n', 'p', 't']:
            self._minimum_required_input_element = 2
            return first_element.upper()
        else:
            self._minimum_required_input_element = 1
            return 'N'
                    
    def get_method_basis(self, input_str):
        # split the string by spaces, and look for the second element for method/basis
        input_str = self.get_info_in_method_line(input_str)
        parts = input_str.split()
        if len(parts) < self._minimum_required_input_element:
            raise ValueError(f" {str}\n Input string does not contain enough information for method/basis extraction.")

        method_basis_string = parts[self._minimum_required_input_element-1]
        
        if '/' not in method_basis_string:
            raise ValueError(f"Invalid method/basis format: {method_basis_string}. Expected format is 'method/basis[/aux_basis_for_density_fitting]'.")
        
        components = method_basis_string.split('/')
        if len(components) < 2 or len(components) > 3:
            raise ValueError(f"Invalid method/basis format: {method_basis_string}. Expected format is 'method/basis[/aux_basis_for_density_fitting]'.")
        
        method = components[0].strip()
        basis = components[1].strip()

        if len(components) == 3:
            density_fitting_basis = components[2].strip()
        else:
            density_fitting_basis = None
        
        return method, basis, density_fitting_basis

    def remove_ending(self, input_str, endings='\n'):
        """if input_str ends with one or multiple endings, remove them."""
        assert isinstance(input_str, str), "Input must be a string."
        while input_str.endswith(endings):
            input_str = input_str[:-len(endings)]
        return input_str

    def get_geometry_optimization(self, input_str):
        input_str = self.get_info_in_method_line(input_str)
        parts = input_str.split()
        if len(parts) < self._minimum_required_input_element+1:
            return None
        # loop over the elements in the parts list, 
        # if an element is 'opt', return 'opt';
        # if an element starts with 'opt=', the element
        for part in parts:
            if part.lower().startswith('opt'):
                return part
        return None
    
    def get_stability_check(self, input_str):
        input_str = self.get_info_in_method_line(input_str)
        parts = input_str.split()
        if len(parts) < self._minimum_required_input_element+1:
            return None
        # loop over the elements in the parts list,
        # if an element is 'stable', return 'stable'
        for part in parts:
            if part == 'stable':
                return part
        return None
    
    def get_initial_guess(self, input_str):
        """Extract the initial guess from the input string."""
        input_str = self.get_info_in_method_line(input_str)
        parts = input_str.split()
        if len(parts) < self._minimum_required_input_element+1:
            return None
        # loop over the elements in the parts list,
        # if an element is 'guess', return 'guess'
        for part in parts:
            if part.lower().startswith('guess='):
                return part
        return None
    
    def get_other_options(self, input_str):
        """Extract other options from the input string."""
        input_str = self.get_info_in_method_line(input_str)
        parts = input_str.split()
        if len(parts) < self._minimum_required_input_element+1:
            return None
        
        # initialize an empty list to hold other options
        other_options = []
        # loop over the elements in the parts list, excluding the first
        # self._minimum_required_input_element elements,
        # see if all self.get_geometry_optimization(part),
        # self.get_stability_check(part), self.get_initial_guess(part), return None
        # if so, append part to other_options
        for part in parts[self._minimum_required_input_element:]:
            modified_str = "# print_level method " + part
            if (self.get_geometry_optimization(modified_str) is None and
                self.get_stability_check(modified_str) is None and
                self.get_initial_guess(modified_str) is None):
                other_options.append(part)

        if other_options == []:
            return None
        else:
            return other_options
    
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
        _ = self.are_all_required_parameters_set()
    
    def save_input_dict_to_json(self, filename):
        """Save the input parameters to a JSON file."""
        import json
        assert isinstance(filename, str), "Filename must be a string."
        assert self.are_all_required_parameters_set(), "Not all required parameters are set."
        
        with open(filename, 'w') as f:
            # save both input parameters and system controls
            # combine _input_parameters and _system_controls into a single dictionary
            combined_dict = self._input_parameters.copy()
            # convert the numpy arrays to lists for JSON serialization
            for key in combined_dict:
                if isinstance(combined_dict[key], np.ndarray):
                    combined_dict[key] = combined_dict[key].tolist()
            combined_dict.update(self._system_controls)
            # write the combined dictionary to the JSON file
            json.dump(combined_dict, f, indent=4)
            
            
    def load_input_dict_from_json(self, filename):
        """Load input parameters from a JSON file."""
        import json
        assert isinstance(filename, str), "Filename must be a string."
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist.")
        
        with open(filename, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                if key in self._input_parameters:
                    if key in ['atoms', 'coordinates']:
                        # convert lists back to numpy arrays
                        if isinstance(value, list):
                            self._input_parameters[key] = np.array(value)
                        else:
                            raise ValueError(f"Expected a list for {key}, got {type(value)}.")
                    else:
                        self._input_parameters[key] = value
                elif key in self._system_controls:
                    self._system_controls[key] = value
                else:
                    raise KeyError(f"Invalid key in JSON file: {key}. Must be one of {required_input + optional_input + system_control}.")

    def save_gaussian_input_file(self, filename):
        """ Save the Gaussian input parameters to a file.
            if filename exists, rename filename to filename.bak_date,
            and show a warning to the user.
        """
        assert isinstance(filename, str), "Filename must be a string."
        assert self.are_all_required_parameters_set(), "Not all required parameters are set."
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
            f.write(f"#{print_level} {method}/{basis}")
            if self._input_parameters['density_fitting'] is not None:
                f.write(f"/{self._input_parameters['density_fitting']}")
            f.write(" ")
            if self._input_parameters['optimization'] is not None:
                f.write(f"{self._input_parameters['optimization']} ")
            if self._input_parameters['stable'] is not None:
                f.write(f"{self._input_parameters['stable']} ")
            if self._input_parameters['guess'] is not None:
                f.write(f"{self._input_parameters['guess']} ")
            if self._input_parameters['other_options'] is not None:
                f.write(" ".join(self._input_parameters['other_options']))
            # write a blank line after the method and basis
            f.write("\n\n")
            
            # write title
            title = self.remove_ending(self._input_parameters['title'], endings = '\n')
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
                    self.set_system_control_parameter(key.lower(), value)
                
            elif line.startswith('#'):
                # method and basis
                assert not if_method_details_read, "Method and basis details already read."

                print_level = self.get_print_level(line)
                self.set_calculation_parameter('print_level', print_level)

                method, basis, density_fitting_basis = self.get_method_basis(line)
                self.set_calculation_parameter('method', method)
                self.set_calculation_parameter('basis', basis)
                self.set_calculation_parameter('density_fitting', density_fitting_basis)

                do_geometry_optimization = self.get_geometry_optimization(line)
                self.set_calculation_parameter('optimization', do_geometry_optimization)

                do_stability_check = self.get_stability_check(line)
                self.set_calculation_parameter('stable', do_stability_check)

                set_initial_guess = self.get_initial_guess(line)
                self.set_calculation_parameter('guess', set_initial_guess)

                other_options = self.get_other_options(line)
                self.set_calculation_parameter('other_options', other_options)

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




            

            

                



