"""
This script runs from a POPx directory and runs through and deletes the histogram data directories.
This is to ensure that we have a clean run each time time we test. plus theres so many output files. So many.
"""

import shutil
import glob
import os

hist_dir = "histogram_data"

ext = "run"
all_runs = [i for i in glob.glob("*.{}".format(ext))]
for run in all_runs:
    os.chdir(run)
    shutil.rmtree(hist_dir)
    os.chdir("../")
