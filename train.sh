#!/bin/bash
#SBATCH --time=23:59:00
#SBATCH --gres=gpu:2
#SBATCH --nodelist=${1:-n102}  # Default to n102 if no argument is provided

source ~/.bashrc
cd /mnt/beegfs/home/hassani/training_an_em/project/temporal-embeddings
conda activate ${2:-train-env}
python3 ${3:-train.py}
conda deactivate