#!/usr/bin/env python
from subprocess import call
import os, socket

# We are using different parameters on different host computers
host = socket.gethostname()
print("Running on host %s" % host)

basefolder = "/Volumes/BCI/SAGE"
outfolder = "%s/fsl-pre" % basefolder
datafolder = "%s/BIDS_data" % basefolder
dir_path = os.path.dirname(os.path.realpath(__file__))

donefolders = [fol for fol in os.listdir(outfolder) if ".feat"  in fol]
datafolders = [fol for fol in os.listdir(datafolder) if "sub-" in fol]

to_do = []
for subject in datafolders:
    if subject not in donefolders:
        to_do.append(subject)

print("Subjects to do:")
print(to_do)
to_do.sort()

template = "%s/sage_preproc_fmri.fsf" % dir_path

print ("template is %s" % template)

# DEBUGGING
to_do = ["sub-12582"]

for subject in to_do:

    print("Working on subject %s" % subject)

    # Create confound files for this subject
    command = "%s/sage_confound_selection.py %s" % (dir_path,subject)
    print(command)
    call(command,shell=True)

    for run in range(1,5):

        #Create design file for this subject/run
        outfile = "%s/designs/%s-run0%d.fsf" % (outfolder,subject,run)
        print ("Will create %s" % outfile)
        command = "sed -e \'s/DEFINESUBJECT/%s/g\' -e \'s/DEFINERUN/%s/g\' %s > %s" % (subject,run,template,outfile)
        print(command)
        call(command, shell=True)

        #run feat
        command = "feat %s" % outfile
        print(command)
        call(command, shell=True)