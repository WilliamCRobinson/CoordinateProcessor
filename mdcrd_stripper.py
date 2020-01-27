"""
This script works through a set of run directories and calls a batch script that calls cpptraj_stripper.
"""
import glob
import os
# Get the runs and sort numerically
ext = "run"
all_runs = [i for i in glob.glob("*.{}".format(ext))]
all_runs = sorted(all_runs, key=lambda a: int(a.split(".")[0]))
# Ensure that amber and thus cpptraj is loaded in
# This variable tells us if we are running on the main part of the simulation or the pre-equilibrium steps.
equil_runs = False
os.system("module load amber")
for run in all_runs:
    os.chdir(run)
    if not equil_runs:
        os.system("nohup srun cpptraj -i /home/wcr9/scripts/cpptraj_stripper.in -p ../common/cho_ger.parm7 &")
    else:
        os.system("nohup srun cpptraj -i /home/wcr9/scripts/cpptraj_stripper.in -p ../../common/cho_ger.parm7 &")


