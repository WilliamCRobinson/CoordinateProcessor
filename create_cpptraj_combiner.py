"""
This script is made to run for the way that we set up simulations here in the lindberg group.
It simply goes through the run directories in a simulation directory and creates a cpptraj script
that will combine the trajectories for further processing. 
 """
import glob
import os
ext = "run"
all_runs = [i for i in glob.glob("*.{}".format(ext))]
all_runs = sorted(all_runs, key=lambda a: int(a.split(".")[0]))
with open("cpptraj_run_combiner.in", "w") as f:
    for run in all_runs:
        os.chdir(run)
        if os.path.isfile("mdcrd"):
            f.writelines("trajin " + run + "/mdcrd\n")
        os.chdir("../")
    f.writelines("trajout combined_runs_modified_out\n")


