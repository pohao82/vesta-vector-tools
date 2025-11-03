import numpy as np
import argparse
from .parse_magmom import parse_magmom_string

def generate_vesta_with_vectors(input_vesta, vectors_array, rgb_color=(0,0,255), 
                                arrow_width=1, center_arrow=True,
                                output_filename="structure_with_vec.vesta"):
    """
    Generates a new VESTA file by inserting the vector data.
    Minimum input:
        input_vesta - specify the vesta file to add the vector to.
        vectors_array - natoms-by-3 arrow; each row (1-by-3) is a moment or displacement vector of a site.
    """

    with open(input_vesta, 'r') as f:
        lines = f.readlines()

    new_lines = []
    vector_data_lines = []
    vector_color_data_lines = []

    # The overall vector scale (VECTS) will be set to 1.0.
    vector_color_r, vector_color_g, vector_color_b = (rgb_color)
    line_width = 0.300*arrow_width  # arrow stick thickness
    #site_scale = 5.000  # Site-specific scale multiplier

    # 1. Format the vector data for the VESTA VECTR section
    for i, vector in enumerate(vectors_array):
        index = i + 1
        x, y, z = vector
        # The VECTR line format is: index label 
        vector_line = (
            f"  {index} {x:12.6f} {y:12.6f} {z:12.6f} \n"
            f"     {index} 0  0  0  0 \n"
            " 0 0 0 0 0\n"
        )
        vector_data_lines.append(vector_line)

    # 2. Format the vector data for VECTT
    for i, vector in enumerate(vectors_array):
        index = i + 1
        vector_line = (
            f"  {index} {line_width} {vector_color_r} {vector_color_g} {vector_color_b} {int(center_arrow)}\n"
        )
        vector_color_data_lines.append(vector_line)

    # 2. Iterate through the original file content and insert/modify sections
    in_vectr_block = False
    for line in lines:
        stripped_line = line.strip()

        # a) Insert vector data into VECTR block
        if stripped_line == "VECTR":
            new_lines.append(line) # copy read in line into new_lines 
            new_lines.extend(vector_data_lines) # and append new block
            in_vectr_block = True
            continue

        if in_vectr_block:
            # Skip the placeholder lines "0 0 0 0 0" that were originally there
            if stripped_line == "0 0 0 0 0":
                new_lines.append(line)
                in_vectr_block = False
            continue

        # a) Insert vector data into VECTT block
        if stripped_line == "VECTT":
            new_lines.append(line)
            new_lines.extend(vector_color_data_lines)
            continue

        # b) Ensure the overall display scale (VECTS) is set
        if line.startswith("VECTS"):
            # Set to 1.0 (or any non-zero value) to ensure vectors are rendered.
            new_lines.append("VECTS 1.000000\n")
            continue

        # c) Ensure site-specific style (SITET) is preserved
        # don't modify the SITET block, but ensure no vector data interferes.
        if stripped_line == "SITET":
            new_lines.append(line)
            continue

        new_lines.append(line)

    # 3. Write the new content to a file
    with open(output_filename, 'w') as f:
        f.write(''.join(new_lines))

    print(f"Successfully generated new VESTA file: {output_filename}")


def vesta_cli():
    """CLI entry point for the VESTA vector adder."""

    parser = argparse.ArgumentParser(description="Add vector arrays to a VESTA file.")
    parser.add_argument("input_vesta_file", help="Path to the input VESTA file.")
    parser.add_argument('--magmom', help='vasp MAGMOM string', type=str, default=None)
    parser.add_argument('-o', '--output', help='Output VESTA file name with added vectors (default: output.vesta)', default='output.vesta')
    parser.add_argument('-n', '--natoms', dest='natoms', action='store', type=int, default=None, help='Number of atoms')
    parser.add_argument('--vector_file', help='file that stores the vector as a natoms-by-3 array', default=None)

    # Customize arrow style
    # arrow anchor mode 
    parser.add_argument('--arrow_mode', 
                        choices=['site','center'], type=str, 
                        default='center',
                        help=(' center(default): arrow is centered on the site |'
                              ' site: arrow starts at the site')
                        )
    # If converting from collinear magmom, choose the spin axis (sqa)
    parser.add_argument('-s', '--sqa', dest='sqa', action='store', type=int, default=2, help='spin axis, only relevant if magmom is collinear. (default=2, i.e. z-axis)')

    # size 
    parser.add_argument('-l', '--lscale', dest='scale', action='store', type=float, default=1, help='scale arrow length')
    parser.add_argument('-w', '--wscale', dest='width', action='store', type=float, default=1, help='scale arrow width')

    # color
    DEFAULT_RGB = [255, 0, 0]
    parser.add_argument('--rgb',
                        type=int,           # Casts each of the 3 inputs to an integer
                        nargs=3,            # Expects exactly 3 arguments 
                        metavar=('R', 'G', 'B'), # Names the arguments in the help message
                        default=DEFAULT_RGB,
                        help=f"RGB color tuple (3 integers separated by spaces, e.g., {DEFAULT_RGB})"
                        )

    return parser.parse_args()


def main():
    args = vesta_cli()
    input_vesta_file = args.input_vesta_file
    output_file      = args.output
    natoms           = args.natoms
    sqa              = args.sqa

    # customize arrow style
    scale = args.scale
    width = args.width
    rgb   = args.rgb

    # take care of vectors 
    magmom_str  = args.magmom
    vector_file = args.vector_file
    print(f"vectorfile: {vector_file}")
    print(f"magmom_str: {magmom_str}")

    if magmom_str is not None and vector_file is not None:
        raise ValueError("Vector source conflict! magmom and vector_file can not be both specified, need to pick one!")
    elif magmom_str is None and vector_file is None: 
        raise ValueError("Need to specify the vectors to add, either through vasp magmom string (--magmom) or vector file (--vector_file)")
    elif vector_file:
        print('read in vector file')
        vec_array = np.loadtxt(vector_file)
    elif magmom_str:
        print('magmom string specified')
        vec_array = parse_magmom_string(magmom_str, natoms, sqa=sqa)

    # default cneter
    center_arrow = False if args.arrow_mode.lower() == 'site' else True

    generate_vesta_with_vectors(input_vesta_file,
                                scale*vec_array,   # scaled vector array
                                rgb_color=rgb,
                                arrow_width=width, 
                                center_arrow=center_arrow, 
                                output_filename=output_file)


if __name__ == "__main__":
    main()
