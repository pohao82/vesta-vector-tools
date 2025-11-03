# VESTA Vector Tools 📐

A simple Python package for easily adding magnetic moment vectors (parsed from VASP MAGMOM strings) or general vector arrays to VESTA files. Provides both a command-line interface (CLI) for quick use and a Python library for scripting.

## 🚀 Installation

This package requires **NumPy**. It is recommended to install it in a dedicated virtual environment.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pohao82/vesta-vector-tools.git
    cd vesta-vector-tools
    ```

2.  **(Optional) In case you want to create and activate a virtual environment:**
    ```bash
    # Using Conda
    conda create -n vesta-dev python=3.11
    conda activate vesta-dev
    ```

3.  **Install in editable mode:**
    ```bash
    pip install -e .
    ```

## 💻 Command Line Usage (`vesta-add-vec`)

The tool is installed as a single executable, `vesta-add-vec`.

### Minimal Examples

| Input Method | Command |
| :--- | :--- |
| **VASP MAGMOM String** | `vesta-add-vec V2Se2O/V2Se2O.vesta --natoms 10 --magmom '2 -2 2 -2 6*0.0'` |
| **External Vector File** | `vesta-add-vec HoAgGe_3x2/hoagge.vesta --vector_file HoAgGe_3x2/vec_file` |

### Full Setup Example

This command applies a custom scale, width, color, and changes the arrow anchor mode.

```bash
vesta-add-vec V2Se2O.vesta --natoms 10 --magmom '2 -2 2 -2 6*0.0' \
    --rgb 0 255 0 --arrow_mode site -l 0.5 -w 1.5 -o my_vectors.vesta

Command line options:

--magmom
      description: VASP MAGMOM string (mutually exclusive with --vector_file)
      type: string
      example: '2 -2 2 -2 6*0.0'

-n  --natoms
      description: Total number of atoms (required for MAGMOM parsing)
      type: int
      example: 10

-s  --sqa
      description: Spin axis, (only relevant for collinear magmom string default z sqa=2)
      type: int
      default: 2

--vector_file
      description: Path to a file containing an N-by-3 vector array
      type: string
      example: vec_file

--rgb
      description: RGB color tuple (three integers)
      type: list(int)
      default: [255, 0, 0]
      example: [0, 255, 0]

--arrow_mode
      description: center (default) or site (arrow starts at the site)
      type: string
      default: center
      example: site

-l  --lscale
      description: Scale factor for the arrow length
      type: float
      default: 1.0
      example: 0.5

-w  --wscale
      description: Scale factor for the arrow width
      type: float
      default: 1.0
      example: 1.5

-o  --output
      description: Output VESTA file name
      type: string
      default: output.vesta
      example: my_vectors.vesta

```

## Important Notes
- The script only works properly if all the (equivalent) sites are listed (i.e. not reduced by symmetry)
- The script does not support multiple vecters on the same site.
- In the input magmom string is collinear, the spin quantization axis will be z by default. 
