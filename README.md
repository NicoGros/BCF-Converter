# BCF Converter

BCF Converter is a Python desktop application for converting Bruker BCF files containing spectral data to HDF5 format. This conversion was required to use PyMca in order to perform data analysis with tools not available in the Bruker M6 JETSTREAM software

The application was developed during a PhD placement at the Victoria and Albert Museum (V&A) in collaboration with the University of Namur for use in scientific and analytical workflows and is made available for public use and dissemination.

## Features

BCF Converter provides a simple graphical interface to:

- open BCF files;
- identify and load spectral data;
- display a preview based on a selected spectral region;
- convert the spectral cube to HDF5;
- preserve basic spectral-axis metadata;
- compress the HDF5 dataset using gzip.

The application uses HyperSpy for BCF data loading and HDF5 for the output format.

## Installation

### Windows executable

The recommended way to use BCF Converter on Windows is to download the latest standalone executable from the GitHub releases page.

No Python installation is required.

Extract the downloaded archive and run:

```text
BCF Converter.exe
```

### Running from source

BCF Converter requires Python.

Create a virtual environment:

```text
python -m venv .venv
```

Activate it and install the dependencies:

```text
pip install -r requirements.txt
```

Run the application:

```text
python main.py
Usage
Click Open BCF.
Select a .bcf file.
The spectral cube is loaded and a preview is displayed.
Click Convert to HDF5.
Select the output location.
```

The resulting HDF5 file contains the spectral data in the data dataset together with basic dimensional and spectral-axis metadata.

## Output format

The HDF5 file contains:


```text
data
```

with attributes including:


```text
width
height
channels
energy_offset
energy_scale
energy_units
```

where available in the source BCF file.

The spectral data are stored using gzip compression.

## Citation

If you use BCF Converter in research resulting in a publication, please cite the software and, where applicable, the associated scientific publication describing its development or use.

See CITATION.cff for the recommended citation.

## Contributing

Bug reports, suggestions, and contributions are welcome.

Please see CONTRIBUTING.md for development and contribution guidelines.

## License

See the LICENSE file for the terms under which BCF Converter is distributed. There is no license at the moment.

## Acknowledgements

BCF Converter was developed during a PhD placement at the Victoria and Albert Museum, in the context of my PhD thesis at the University of Namur.
