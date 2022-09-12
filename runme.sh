#!/usr/bin/bash
#SBATCH --partition=fat
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --requeue
#SBATCH --mincpus=2
#SBATCH --mem=64G
#SBATCH -t 24:00:00
#SBATCH --error=slurm-%j.err
#SBATCH --output=slurm-%j.out
#SBATCH --job-name=yimi_test1
#SBATCH --mail-user=y.zhao1@student.tue.nl
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --export=ALL

python3 third_test_script.py
