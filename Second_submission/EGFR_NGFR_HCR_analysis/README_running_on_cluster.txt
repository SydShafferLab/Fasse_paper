Setting up environment on cluster:
module load python/3.6.3
python -m virtualenv NGFR_Cellori
pip install cellori
pip install imageio
pip install openpiv
python -m pip install "dask[array]" --upgrade
pip install pandas

export the package versions on the cluster after installing
python -m pip freeze > /project/shafferslab/Dylan/DLS071/images_for_analysis/package_versions.txt

submit the job
module load python/3.6.3
source /home/dyschaff/NGFR_Cellori/bin/activate
bsub -e EGFR_NGFR_HCR.e -o EGFR_NGFR_HCR.o -M 256000 python "/project/shafferslab/Dylan/DLS071/images_for_analysis/HCR_Cellori_Cluster.py"