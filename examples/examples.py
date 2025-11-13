from vesta_vector_tools.vesta_vector_adder import generate_vesta_with_vectors
from vesta_vector_tools.parse_magmom import parse_magmom_string
import numpy as np

# Noncollinear 
input_vesta_file = "HoAgGe_3x2/hoagge.vesta"
# generate_vesta_with_vectors takes in an Natom-by-3 array for the vectors to add 
# Read vector from a file
vec_array = np.loadtxt('HoAgGe_3x2/vec_file')
scale=0.5 # scale for the vector length
# Minimal input: vesta input_file and vector array
generate_vesta_with_vectors(input_vesta_file, scale*vec_array)

# Convert magmom_str to N-by-3 array
magmom_str ='108*0 0 5.5  0 -0 -5.5  0 -0 -5.5  0 0  5.5  0 0  5.5  0 0  5.5  0 4.7631  2.75  0 4.7631  2.75  0 -4.7631 -2.75  0 -4.7631 -2.75  0 4.7631  2.75  0 4.7631  2.75  0 4.7631 -2.75  0 -4.7631  2.75  0 -4.7631  2.75  0 -4.7631  2.75  0 -4.7631  2.75  0 4.7631 -2.75  0'
natoms= 54 # number of atoms needed for parsing magmom string (determine col or noncllinear)
magmom_array = parse_magmom_string(magmom_str, natoms) 
# with additional setup adjust arrow style and specify output name
scale = 0.3 
generate_vesta_with_vectors(input_vesta_file, scale*magmom_array, rgb_color=(100,100,100), arrow_width=1.5, center_arrow=False, output_filename="hoagge_vec2.vesta")

# Collinear magmom
input_vesta_file2 = "V2Se2O/V2Se2O.vesta"
magmom_str = '2 -2 2 -2 6*0.0'
natoms = 10 
scale =1.6
# converting collinear magmom to 3D vectors, default spin axis = z (sqa=2) 
magmom_array = parse_magmom_string(magmom_str, natoms)
generate_vesta_with_vectors(input_vesta_file2, scale*magmom_array, rgb_color=(0,0,255), arrow_width=1.2, center_arrow=True, output_filename="v2se2o_vec_z.vesta")

# switch spin axis to x (sqa=0)
magmom_array = parse_magmom_string(magmom_str, natoms, sqa=0) 
generate_vesta_with_vectors(input_vesta_file2, scale*magmom_array, rgb_color=(255,0,0), arrow_width=1.2, center_arrow=False, output_filename="v2se2o_vec_x.vesta")

