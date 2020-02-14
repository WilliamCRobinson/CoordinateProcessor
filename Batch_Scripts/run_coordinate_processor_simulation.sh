#!/bin/bash
#SBATCH --job-name=T2H
#SBATCH --time=08:00:00
#SBATCH --mem=5000
#SBATCH --output=outT2H
#SBATCH --error=errorT2H
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wcr9@nau.edu
module load amber
source activate seaborn_env
python /home/wcr9/scripts/create_cpptraj_combiner.py
cpptraj -i cpptraj_run_combiner.in -p /common/cho_ger.parm7
cd ./equil1/
python /home/wcr9/scripts/create_cpptraj_combiner.py
cpptraj -i cpptraj_run_combiner.in -p ../common/cho_ger.parm7
cd ../equil2/
python /home/wcr9/scripts/create_cpptraj_combiner.py
cpptraj -i cpptraj_run_combiner.in -p ../common/cho_ger.parm7
cd ../
cpptraj -i /home/wcr9/scripts/cpptraj_combine_combined.in -p /common/cho_ger.parm7
cpptraj -i /home/wcr9/scripts/cpptraj_stripper.in -p /common/cho_ger.parm7
python /home/wcr9/scripts/coordinate_processor.py
