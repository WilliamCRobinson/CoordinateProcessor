import os
import datetime
import glob
import shutil as shu


def make_directory(dir):
    """Makes a directory if it doesnt already exist"""
    if not os.path.exists(dir):
        os.mkdir(dir)


hist_dir = "histogram_data"

# Now make a list of all the run directories.
ext = "run"
all_runs = [i for i in glob.glob("*.{}".format(ext))]
# Loop through the run directories
for run in all_runs:
    time = str(datetime.datetime.now()).split(".")[-1]
    os.chdir(run)
    make_directory(hist_dir)
    shu.copy("mdcrd", hist_dir)
    os.chdir(hist_dir)
    with open(run + "coordprocrun.sh", "w") as file:
        file.writelines("#!/bin/bash\n")
        file.writelines("#SBATCH --job-name=" + time + "_run_coord_proc\n")
        file.writelines("#SBATCH --output=" + time + "_run_coord_proc_out.out\n")
        file.writelines("#SBATCH --error=" + time + "_run_coord_proc_error.out\n")
        file.writelines("#SBATCH --time=00:30:00\n")
        file.writelines("#SBATCH --ntasks 1\n")
        file.writelines("#SBATCH --cpus-per-task 1\n")
        file.writelines("#SBATCH --mem=2000\n")
        file.writelines("#SBATCH --mail-type=ALL\n")
        file.writelines("#SBATCH --mail-user=wcr9@nau.edu\n")
        file.writelines("module load amber\n")
        file.writelines("cpptraj -i /home/wcr9/scripts/cpptraj.in -p ../../common/cho_ger.parm7\n")
        file.writelines("module load anaconda/latest\n")
        file.writelines(".conda/envs/seaborn_env/bin/python /home/wcr9/scripts/coordinate_processor.py\n")
    os.system("sbatch " + run + "coordprocrun.sh")
    os.chdir("../../")
