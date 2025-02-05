#!/bin/bash
#SBATCH --time=23:00:00
#SBATCH --gres=gpu:2
#SBATCH --nodelist=n102

source ~/.bashrc
cd /mnt/beegfs/home/hassani/training_an_em/project/temporal-embeddings
conda activate train-env
python3 train.py
conda deactivate