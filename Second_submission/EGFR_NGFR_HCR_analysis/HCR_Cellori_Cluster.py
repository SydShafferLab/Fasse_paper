# Load the needed paths
from pathlib import Path
import re
from cellori import Cellori, utils
import numpy as np
import pandas as pd
import cv2
from IPython.display import Image, display
from matplotlib import pyplot as plt
from scipy import ndimage
import glob
import csv

# Put in the correct path to the image directory ----------------------------------------------------------

# Get all of the paths for nuclei (red) channels
image_dir = Path('project/shafferslab/Dylan/DLS071/images_for_analysis') # Path to all images

# ---------------------------------------------------------------------------------------------------------

nuclei_paths = sorted(list(image_dir.glob('*/*DAPI*.tif')))

# Make the dataframe for the outputs
output_df = pd.DataFrame(columns = ['Mean_488','Mean_647','Cell_num', 'Coords_X', 'Coords_Y','Nuc_file','file_488','file_647'])
error_images = []

# Run analysis in loop
for i in nuclei_paths[0:2]:

    # Load the correct paths
    nuclei_path = str(i)

    print(nuclei_path)

    path_488 = nuclei_path.replace('/DAPI', '/488')
    path_647 = nuclei_path.replace('/DAPI', '/647') 
    try:

        # Run Cellori to find masks for nuclei
        masks, coords, _ = Cellori(nuclei_path).segment(segmentation_mode='combined', threshold_locality=.7, sigma=5, nuclei_diameter=10)

        # Load in the 488 and 647 images
        image_488 = cv2.imread(path_488, cv2.IMREAD_UNCHANGED)
        image_647 = cv2.imread(path_647, cv2.IMREAD_UNCHANGED)

        # Expand the masks by a number of pixels and measure ngfr expression
        dil_struct = np.ones((15,15), dtype = np.uint8)
        expanded_masks = np.zeros_like(masks)
        mean_intensities_488 = []
        mean_intensities_647 = []

        print(len(np.unique(masks)))
        for mask_num in np.unique(masks)[np.unique(masks) > 0][0:2]:
            print(mask_num)
            if mask_num == 0:
                continue
            mask = masks == mask_num
            expanded_mask = ndimage.binary_dilation(mask, structure = dil_struct)
            expanded_masks[expanded_mask] = mask_num

            masked_pixels_488 = image_488[mask]
            mean_intensity_488 = np.mean(masked_pixels_488)
            mean_intensities_488.append(mean_intensity_488)

            masked_pixels_647 = image_647[mask]
            mean_intensity_647 = np.mean(masked_pixels_647)
            mean_intensities_647.append(mean_intensity_647)

        

        temp_df = pd.DataFrame(data = {'Mean_488': mean_intensities_488,
                                        'Mean_647': mean_intensities_647,
                                    'Cell_num': np.unique(masks)[np.unique(masks) > 0][0:2],
                                    'Coords_X': coords[:,0][0:2],
                                    'Coords_Y': coords[:,1][0:2],
                                    'Nuc_file': [nuclei_path.split('/')[-1]]*len(mean_intensities_488),
                                    'file_488': [(path_488.split('/')[-2]+'/'+path_488.split('/')[-1])]*len(mean_intensities_488),
                                    'file_647': [(path_647.split('/')[-2]+'/'+path_647.split('/')[-1])]*len(mean_intensities_647)})

        output_df = pd.concat([output_df, temp_df])
    except:
        error_images.append(nuclei_path.split('/')[-1])
        pass
        

# Write to CSVs    
outpath = Path(str(image_dir)+'/cellori_output.csv')
output_df.to_csv(outpath)

outpath_errors = Path(str(image_dir)+'/cellori_error_images.csv')
pd.DataFrame(error_images).to_csv(outpath_errors, header = False)
