"""Functions for writing data and labels to HDF5 files.
"""

import os
from typing import Tuple

import h5py
import numpy as np

from h5utils.project_path import datadir


def write_data_and_label(
    file_path: str,
    dataset_name: str,
    data_array: np.ndarray,
    label_array: np.ndarray,
) -> None:
    """
    Writes data and label to an HDF5 file.

    Args:
        file_path (str): The path to the HDF5 file.
        dataset_name (str): The name of the dataset in the HDF5 file.
        data_array (np.ndarray): The data to be written to the dataset.
        label_array (np.ndarray): The label to be added as an attribute to the
            dataset.

    Returns:
        None
    """

    # Check if the HDF5 file exists; if not, create it and set up the dataset.
    if not os.path.exists(file_path):
        setup_hdf5_file(file_path, dataset_name, data_array.shape)

    # Open the HDF5 file in read/write mode.
    with h5py.File(file_path, 'r+') as file:
        dataset = file[dataset_name]  # Open the specified dataset.

        # Write the data to the dataset.
        dataset[...] = data_array

        # Add the label as an attribute to the dataset.
        dataset.attrs['label'] = label_array


def setup_hdf5_file(
    file_path: str,
    dataset_name: str,
    shape: Tuple[int, ...],
) -> None:
    """
    Sets up an HDF5 file with a specified dataset.

    Args:
        file_path (str): The path to the HDF5 file.
        dataset_name (str): The name of the dataset to create.
        shape (Tuple[int, ...]): The shape of the dataset to create.

    Returns:
        None
    """

    with h5py.File(file_path, 'a') as file:
        file.require_dataset(
            dataset_name,
            shape=shape,
            chunks=(
                1,
                *shape[1:],
            ),  # Chunking with chunk size based on the shape.
            dtype=np.float32,  # Set the data type of the dataset.
        )


def print_hdf5_structure(group: h5py.Group, indent: int = 2) -> None:
    """Recursively prints the structure of an HDF5 file.

    Args:
        group (h5py.Group): The HDF5 group to print.
        indent (int, optional): The number of spaces for indentation. Defaults
            to 2.

    Returns:
        None
    """

    print("HDF5 File Structure:")

    # Iterate through each item in the current HDF5 group.
    for name, item in group.items():
        # Check if the item is a group.
        if isinstance(item, h5py.Group):
            # Print the group name with indentation.
            print(" " * indent + f"group: {name}/")
            # Recursively print the structure of the subgroup.
            print_hdf5_structure(item, indent + 2)

        # Check if the item is a dataset
        elif isinstance(item, h5py.Dataset):
            # Print the dataset name, shape, and data type with indentation.
            print(" " * indent + "dataset:")
            print(" " * (indent + 4) + f"{name} (shape: {item.shape}, "
                  f"dtype: {item.dtype})")

            # If the dataset has attributes, print their names and shapes.
            if len(item.attrs.keys()) > 0:
                print(" " * (indent) + "attributes:")
                for attr_name, attr_value in item.attrs.items():
                    # Print the attribute name and shape with additional
                    # indentation.
                    print(" " * (indent + 4) +
                          f"{attr_name}: (shape={attr_value.shape},"
                          f" dtype={attr_value.dtype})")

                    # Print the attribute values if they are small.
                    if attr_value.size < 10:
                        print(
                            " " * (indent + 4) + f"values: "
                            f"{[label.decode('utf-8') for label in attr_value]}"
                        )


def main() -> None:
    """Function to demonstrate usage of HDF5 writing and structure printing.
    """

    # Path to the HDF5 file and dataset name.
    file_path = os.path.join(datadir('example_directory'), 'example.h5')
    dataset_name = 'example_dataset'

    # Example data array.
    data = np.random.rand(10, 3, 256, 256).astype(np.float32)

    # Example label strings for each element (10 in total).
    label = np.array([f"label_{i}" for i in range(data.shape[0])], dtype='S')

    # Write the data and label to the HDF5 file.
    write_data_and_label(file_path, dataset_name, data, label)

    # Print the structure of the HDF5 file.
    with h5py.File(file_path, "r") as file:
        print_hdf5_structure(file)


if __name__ == "__main__":
    # Run the main function if the script is executed.
    main()
