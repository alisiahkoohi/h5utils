import os

import h5py
import numpy as np
from skimage import data
import matplotlib.pyplot as plt

from h5utils import write_data_and_label, print_hdf5_structure, datadir


def main() -> None:
    """Writing and reading a JPEG file to an HDF5 file.


    Demonstrates the process of writing an image to an HDF5 file, reading it
    back, and displaying it using matplotlib. This includes normalizing the
    image, adjusting its shape to fit a specific format, and handling the data
    within an HDF5 file.

    Steps:
        1. Load a sample image.
        2. Normalize and reshape the image.
        3. Write the image and label to an HDF5 file.
        4. Print the structure of the HDF5 file.
        5. Read the image and label back from the HDF5 file.
        6. Display the image using matplotlib with the label as the title.
    """

    # Load a sample image from skimage.
    image = data.astronaut()

    # Cast the image to type np.float32 and normalize to [0, 1].
    data_array = image.astype(np.float32) / 255.0

    # Add a new axis and permute to match the expected shape in torch:
    # (1, channels, height, width).
    data_array = data_array[np.newaxis, ...].transpose(0, 3, 1, 2)

    # Example label (e.g., a string)
    label_array = np.array(['astronaut'], dtype='S')

    # Path to the HDF5 file and dataset name.
    file_path = os.path.join(datadir('example_directory'), 'astronaut.h5')
    dataset_name = 'image'

    # Write the data and label to the HDF5 file.
    write_data_and_label(file_path, dataset_name, data_array, label_array)

    # Print the structure of the HDF5 file.
    with h5py.File(file_path, 'r') as file:
        print_hdf5_structure(file)

    # Read the image back from the HDF5 file.
    file = h5py.File(file_path, 'r')
    image = file[dataset_name][0]
    label = file[dataset_name].attrs['label'][0].decode('utf-8')
    file.close()

    # Permute the image back to the original shape so that it can be displayed.
    image = image.transpose(1, 2, 0)

    # Plot the image while using the label as title.
    plt.figure(dpi=150)
    plt.imshow(image)
    plt.title(label)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
