<h1 align="center">h5utils: Some basic tools for interfacing with h5py</h1>

## Installation

Run the command below to install the package to be used in your Python environment.

```bash
pip install git+https://github.com/alisiahkoohi/h5utils
```

For further development and to run the examples, clone the repository
and install the package in editable mode.

```bash
git clone ttps://github.com/alisiahkoohi/h5utils
cd h5utils/
pip install -e .
```

## Usage

The package provides the following functions:

- `write_data_and_label(file_path, dataset_name, data_array, label_array)`: Writes data and label to an HDF5 file.
- `print_hdf5_structure(group, indent=2)`: Recursively prints the structure of an HDF5 file.


To write data and labels to an HDF5 file:

```python
from h5utils import write_data_and_label, datadir

# Path to the HDF5 file and dataset name.
file_path = os.path.join(datadir('example_directory'), 'example.h5')
dataset_name = 'example_dataset'

# Example data array.
data = np.random.rand(10, 3, 256, 256).astype(np.float32)

# Example label strings for each element (10 in total).
label = np.array([f"label_{i}" for i in range(data.shape[0])], dtype='S')

# Write the data and label to the HDF5 file.
write_data_and_label(file_path, dataset_name, data, label)
```

To print the structure of an HDF5 file:

```python
import h5py
from h5utils import print_hdf5_structure, datadir

# Path to the HDF5 file.
file_path = os.path.join(datadir('example_directory'), 'example.h5')

with h5py.File(file_path, 'r') as file:
    print_hdf5_structure(file)
```

Replace `file_path` with the path to the HDF5 file you want to inspect.
`datadir` is a helper function that returns the absolute path to the
`data` directory located in the repository.


## Examples

The `examples/` directory contains a Python script that demonstrates how
to use the package to write a JPEG image and its label to an HDF5 file
and then read the data back.

```bash
python examples/write_jpg_to_h5.py
```

## Questions

Please contact alisk@rice.edu for questions.

## Author

Ali Siahkoohi
