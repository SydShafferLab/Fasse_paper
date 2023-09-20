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
image_dir = Path('/project/shafferslab/Dylan/PW019/q3d_files') # Path to all images

# ---------------------------------------------------------------------------------------------------------

nuclei_paths = sorted(list(image_dir.glob('*/*red*.tif')))

# Make the dataframe for the outputs
output_df = pd.DataFrame(columns = ['Mean_NGFR','Cell_num','Well_num','FOV','Time','Nuc_file','NGFR_file'])

# Run analysis in loop
for i in nuclei_paths:

    # Load the correct paths
    nuclei_path = str(i)
    ngfr_path = nuclei_path.replace('/red', '/green')
    
    # Run Cellori to find masks for nuclei
    masks, coords, image = Cellori(nuclei_path).segment(segmentation_mode='combined',nuclei_diameter=22)

    # Load in the ngfr image
    ngfr_image = cv2.imread(ngfr_path, cv2.IMREAD_UNCHANGED)

    # Expand the masks by a number of pixels and measure ngfr expression
    dil_struct = np.ones((15,15), dtype = np.uint8)
    expanded_masks = np.zeros_like(masks)
    mean_intensities = []
    for mask_num in np.unique(masks):
        if mask_num == 0:
            continue
        mask = masks == mask_num
        expanded_mask = ndimage.binary_dilation(mask, structure = dil_struct)
        expanded_masks[expanded_mask] = mask_num
        masked_pixels = ngfr_image[mask]
        mean_intensity = np.mean(masked_pixels)
        mean_intensities.append(mean_intensity)
        
    temp_df = pd.DataFrame(data = {'Mean_NGFR': mean_intensities,
                               'Cell_num': np.unique(masks)[np.unique(masks) > 0],
                               'Well_num': [nuclei_path.split('/')[-2]]*len(mean_intensities),
                               'FOV': [nuclei_path.split('/')[-1].split('_')[0][-3:]]*len(mean_intensities),
                               'Time': [nuclei_path.split('/')[-1].split('_')[1][:6]]*len(mean_intensities),
                               'Nuc_file': [nuclei_path.split('/')[-1]]*len(mean_intensities),
                               'NGFR_file': [ngfr_path.split('/')[-1]]*len(mean_intensities)})
    
    output_df = pd.concat([output_df, temp_df])


# Write to csv    
outpath = Path('/'.join(ngfr_path.split('/')[:-2])+'/output.csv')
output_df.to_csv(outpath)
