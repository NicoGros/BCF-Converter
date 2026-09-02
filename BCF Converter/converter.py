"""
BCF Converter

BCF loading, spectral data extraction and HDF5 conversion.

Provides functions for loading Bruker BCF files using HyperSpy,
extracting spectral cubes and metadata, generating preview images,
and saving converted data to HDF5 format.

Copyright (c) 2026 Nicolas Gros

Licensed under the GPL-3.0 license.
See the LICENSE file in the project root for details.
"""

import h5py
import hyperspy.api as hs


def load_bcf(path):
    """Load a BCF file and return the spectral cube and metadata."""

    signal = hs.load(path)

    if isinstance(signal, list):
        spectral = [s for s in signal if s.data.ndim == 3]

        if not spectral:
            raise ValueError("No spectral cube found.")

        signal = spectral[0]

    cube = signal.data

    metadata = {}

    try:
        axis = signal.axes_manager[-1]

        metadata["energy_offset"] = axis.offset
        metadata["energy_scale"] = axis.scale
        metadata["energy_units"] = axis.units

    except Exception:
        pass

    return cube, metadata


def save_hdf5(cube, metadata, filename):

    height, width, depth = cube.shape

    with h5py.File(filename, "w") as h5:

        dset = h5.create_dataset(
            "data",
            data=cube,
            compression="gzip",
            compression_opts=4,
            shuffle=True,
        )

        dset.attrs["width"] = width
        dset.attrs["height"] = height
        dset.attrs["channels"] = depth

        for key, value in metadata.items():
            dset.attrs[key] = value


def roi_preview(cube, start=100, end=300):
    """Return an ROI image for preview."""

    return cube[:, :, start:end].sum(axis=2)
