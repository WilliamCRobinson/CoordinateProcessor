"""
This script is made to run for the way that we set up simulations here in the lindberg group.
It simply goes through the run directories in a simulation directory and creates a cpptraj script
that will combine the trajectories for further processing. 
 """
import glob
ext = "run"
all_runs = [i for i in glob.glob("*.{}".format(ext))]
all_runs = sorted(all_runs, key=lambda a: int(a.split(".")[0]))
with open("cpptraj_run_combiner.in","w") as f:
    f.writelines("parm /common/cho_ger.parm7\n")
    for run in all_runs:
        f.writelines("trajin " + run + "/mdcrd\n")
    f.writelines("trajout combined_runs_modified_out\n")


