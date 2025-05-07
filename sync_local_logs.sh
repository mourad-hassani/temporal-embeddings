while true; do
    rsync -avz hassani@slurm:/mnt/beegfs/home/hassani/training_an_em/project/temporal-embeddings/logs/ ./logs
    sleep 20
done