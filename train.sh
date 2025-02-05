#!/bin/bash
#SBATCH --time=23:00:00
#SBATCH --gres=gpu:1
#SBATCH --nodelist=n102
#SBATCH --mail-user=im_hassani@esi.dz
#SBATCH --mail-type=ALL

source ~/.bashrc
#cd /mnt/beegfs/home/YOUR_LOGIN/(...)
#conda activate YOUR_CONDA_ENV
# python --version
#python YOUR_PYTHON_FILE.py
#conda deactivate
#Then print Hello and the nodename
python3 train.py