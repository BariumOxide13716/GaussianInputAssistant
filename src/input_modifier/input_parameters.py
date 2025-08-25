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
    'theory': ['mn15l', 'umn15l'], 
    'basis': ['jul-cc-pvtz'],
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


