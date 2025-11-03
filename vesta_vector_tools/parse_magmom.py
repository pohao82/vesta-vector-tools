import argparse
import numpy as np

def parse_magmom_string(magmom_str, natoms, format='array', sqa=2):
    """
    Parses a VASP MAGMOM string into the app's moment dictionary format.
    Handles both collinear (e.g., '2*5.0 2*-5.0') and non-collinear formats.

    Input: 
        magmom_str: MAGMOM strings from vasp INCAR  
        natoms:     Number of atoms
        format:     np array or dict
        sqa:        choose what direction to be spin axis (x/y/z=/0/1/2) only relevant for collinear magmom

    Output:
        moments_output 
         
    """
    # Clean the input string
    s = magmom_str.lower().replace('magmom', '').replace('=', '').strip()

    # uncontract the array.
    parts = s.split()
    expanded_values = []
    for part in parts:
        if '*' in part:
            count, value = part.split('*')
            expanded_values.extend([float(value)] * int(count))
        else:
            expanded_values.append(float(part))

    # get natom-by-3 moment array first 
    # Check if collinear or non-collinear based on the number of values
    if len(expanded_values) == natoms:
        # Collinear: [m1, m2, ...] -> { '0': [m1,0,0], '1': [m2,0,0], ... }
        moments_array = np.zeros((natoms,3))
        for i, val in enumerate(expanded_values):
            moments_array[i, sqa] = float(val)
    elif len(expanded_values) == 3 * natoms:
        # Non-collinear: [m1x, m1y, m1z, m2x, ...] -> { '0': [m1x,m1y,m1z], ... }
        moments_array = np.array(expanded_values).reshape((natoms, 3))
    else:
        raise ValueError(f"Invalid number of moments. Expected {natoms} (collinear) "
                         f"or {3*natoms} (non-collinear), but got {len(expanded_values)}.")

    if format.lower() == 'dict':
        moments_output = {str(i): vec.tolist() for i, vec in enumerate(moments_array)}
    elif format.lower() == 'array':
        moments_output = moments_array
        

    #return moments_dict
    return moments_output


## noncollinar 
##magmom_str ='108*0 0 5.5  0 -0 -5.5  0 -0 -5.5  0 0  5.5  0 0  5.5  0 0  5.5  0 4.7631  2.75  0 4.7631  2.75  0 -4.7631 -2.75  0 -4.7631 -2.75  0 4.7631  2.75  0 4.7631  2.75  0 4.7631 -2.75  0 -4.7631  2.75  0 -4.7631  2.75  0 -4.7631  2.75  0 -4.7631  2.75  0 4.7631 -2.75  0'
##natoms= 54
#
# collinear 
#magmom_str = '16*0 3 3 -3 -3 -3 3 3 -3 3 -3 3 -3 -3 3 -3 3 32*0'
#natoms= 64
##magmom_array = parse_magmom_string(magmom_str, natoms, 'dict')
#magmom_array = parse_magmom_string(magmom_str, natoms)

#[print(f'{i}: {magmom_array[i]}') for i in magmom_array.keys()]
#print(magmom_array)
