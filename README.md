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
