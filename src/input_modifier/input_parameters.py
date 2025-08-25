# This file contains a list of strings for required input parameters
# in a Gaussian calculation.

"""
The input_geometry dictionary is for the geometry of the molecular system.
"""

system_control = [
    'chk',
    'mem',
    'nprocshared'
]

print_level = ['p', 't', 'n']

electronic_structure_method = {
    'theory': ['mn15l', 'hf', 'ccsd', 'mp2', 'pbepbe', 'b3lyp', 'wb97x', 'm062x', 'pbe0'], 
    'basis': ['aug-cc-pvtz', 'jul-cc-pvtz', 'jun-cc-pvtz'],
    'df_basis': ['auto']
}

optional_standalone = [
    'opt',
    'freq',
    'nosymm'
]

optional_withvalue = {
    'stable': ['opt'],
    'guess': ['read']
}

input_geometry = [
    'title',
    'charge',
    'multiplicity',
    'atoms',
    'coordinates'
]


