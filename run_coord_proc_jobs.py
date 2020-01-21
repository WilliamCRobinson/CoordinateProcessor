import os
import datetime
import glob
import shutil as shu

def make_directory(dir)
    """Makes a directory if it doesnt already exist"""
    if not os.path.exists(dir):
        os.mkdir(dir)

hist_dir = "histogram_data"

#Now make a list of all the run directories.
ext = "run"
all_runs = [i for i in glob.glob("*.{}".format(ext))]

for run in all_runs:
    time = datetime.now()
    os.chdir(run)
    make_directory(hist_dir)
    shu.copy("mdcrd", hist_dir)
    os.chdir(hist_dir)
    with open(run+"coordprocrun.sh", "wh") as file:
        file.writelines("#!/bin/bash\n")
        file.writelines("#SBATCH --job-name=" + time + "_run_coord_proc\n")
        file.writelines("#SBATCH --output=.out/" + time + "_run_coord_proc\n")
        file.writelines("#SBATCH --error=.out/" + time + "_run_coord_proc\n")
        file.writelines("#SBATCH --time=1:00:00\n")
        file.writelines("#SBATCH --ntasks 1\n")
        file.writelines("#SBATCH --cpus-per-task 1\n")
        file.writelines("#SBATCH --mail-type=ALL\n")
        file.writelines("#SBATCH --mail-user=wcr9@nau.edu\n")
        file.writelines("module load python/3.latest\n")
        file.writelines("cpptraj -i /home/wcr9/scripts/cpptraj.in -p ../common/cho_ger.parm7")
        file.writelines("python /home/wcr9/scripts/coordinate_processor.py")
    os.system("sbatch " + run + "coordprocrun.sh")






