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

es_method = { # standing for electronic structure method
    'theory': ['mn15l', 'umn15l'], 
    'basis': ['jul-cc-pvtz'],
    'df_basis': ['auto']
}

optional_switch = [
    'opt',
    'freq',
    'nosymm'
]

optional_method = {
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


