import nd2
import tifffile
import os

# Folder containing ND2 files
input_folder = '/Users/dylanschaff/Library/CloudStorage/GoogleDrive-dyschaff@sydshafferlab.com/My Drive/Schaff_Shared/Cloud/Experiment_IDs/DLS071'

# Common quadrant size
quadrant_size_X = 9267
quadrant_size_Y = 9249

# Iterate through the ND2 files in the folder
for filename in os.listdir(input_folder):
    print(filename)
    if filename.endswith('.nd2'):
        nd2_file_path = os.path.join(input_folder, filename)

        # Load the ND2 image
        image = nd2.imread(nd2_file_path)

        # Split into quadrants
        q1 = image[:, :quadrant_size_X, :quadrant_size_Y]
        q2 = image[:, :quadrant_size_X, quadrant_size_Y:2*quadrant_size_Y]
        q3 = image[:, quadrant_size_X:2*quadrant_size_X, :quadrant_size_Y]
        q4 = image[:, quadrant_size_X:2*quadrant_size_X, quadrant_size_Y:2*quadrant_size_Y]

        # Create an output directory for the quadrants
        output_dir = os.path.join(input_folder, os.path.splitext(filename)[0])
        os.makedirs(output_dir, exist_ok=True)

        # Save the quadrants as TIF files
        for i, quadrant in enumerate([q1, q2, q3, q4], start=1):
            tifffile.imwrite(os.path.join(output_dir, f'q{i}.tif'), quadrant, metadata={'axes': 'CYX'})
            # iterate through the channels and save individually
            colors = ['DAPI','488','Cy3','647']
            for z in range(quadrant.shape[0]):
                tifffile.imwrite(os.path.join(output_dir, f'{colors[z]}_q{i}.tif'), quadrant[z], metadata={'axes': 'YX'})

       
print("Quadrant splitting and saving complete.")
