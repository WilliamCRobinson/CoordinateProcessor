"""
April 2020
The purpose of this script is to run through the five different simulations in each of the cell membrane types
and convert the combined e1_e2_main_mdcrd.crd files to .dcd files.
"""
import os
il_conc = [0, 8, 16, 32, 64]
for element in il_conc:
    os.chdir(str(element)+"-ILs")
    os.system("nohup srun --time 05:00:00 --job-name=converter"
              " cpptraj -i /home/wcr9/scripts/cpptrajcrd2dcd.in -p ./common/cho_ger.parm7 &")
    os.system("nohup srun --time 05:00:00 --job-name=stripped_converter"
              " cpptraj -i /home/wcr9/scripts/cpptrajcrd2dcdstripped.in -p ./strip.cho_ger.parm7 &")
    os.chdir("../")
