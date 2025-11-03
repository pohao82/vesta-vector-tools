from setuptools import setup, find_packages

setup(
    name='vesta-vector-tools',
    version='0.1.0',
    packages=find_packages(),
    description='Tools for adding vectors to VESTA files and converting VASP MAGMOM strings to a N-by-3 np.array',
    author='Po-Hao Chang',
    author_email='your.email@example.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pohao82/vesta-vector-tools',
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    # This creates the command 'vesta-add-vec'
    entry_points={
        'console_scripts': [
            'vesta-add-vec = vesta_vector_tools.vesta_vector_adder:main',
            #'vasp-parse-magmom = vesta_tools.vasp_parser:vasp_cli',
        ],
    },
)
