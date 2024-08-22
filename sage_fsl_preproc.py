#!/usr/bin/env python
from subprocess import call
import os, socket

# We are using different parameters on different host computers
host = socket.gethostname()
print("Running on host %s" % host)

basefolder = "/Volumes/BCI/SAGE"
outfolder = "%s/fsl-pre" % basefolder
datafolder = "%s/BIDS_data" % basefolder
prepfolder = "%s/fmriprep" % basefolder

dir_path = os.path.dirname(os.path.realpath(__file__))

donefolders = [fol for fol in os.listdir(outfolder) if "sub-"  in fol]
readyfolders = [fol for fol in os.listdir(prepfolder) if "sub-" in fol and ".html" in fol]
datafolders = [fol for fol in os.listdir(datafolder) if "sub-" in fol]

print("Ready:")
print(readyfolders)
print("\nDone:")
print(donefolders)

to_do = []
for subject in readyfolders:
    if subject not in donefolders:
        to_do.append(subject[0:9])

print("\nSubjects to do:")
print(to_do)
to_do.sort()

template = "%s/sage_preproc_fmri.fsf" % dir_path

print ("template is %s" % template)

# DEBUGGING

for subject in to_do:

    print("Working on subject %s" % subject)

    # Create confound files for this subject
    command = "%s/sage_confound_selection.py %s" % (dir_path,subject)
    print(command)
    call(command,shell=True)

    for run in range(1,5):

        print("Working on run %d" % run)

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

        #add a constant to the in-brain voxels in the residuals file so that FSL can tell it from the background
        command = "%s/sage_fix_residuals.py %s" % (dir_path,subject)
