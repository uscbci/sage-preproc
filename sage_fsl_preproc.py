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

exit()

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
        maskfile = "%s/%s_run-0%d_pre.feat/mask.nii.gz" % (outfolder,subject,run)
        newmaskfile = "%s/%s_run-0%d_pre.feat/mask_high.nii.gz" % (outfolder,subject,run)
        residfile = "%s/%s_run-0%d_pre.feat/stats/res4d.nii.gz" % (outfolder,subject,run)
        newresidfile = "%s/%s_run-0%d_pre.feat/stats/res4d_bg.nii.gz" % (outfolder,subject,run)
        command = "fslmaths %s -mul 10000 %s" % (maskfile,newmaskfile)
        print(command)
        call(command, shell = True)
        command = "fslmaths %s -add %s %s" % (residfile, newmaskfile, newresidfile)
        print(command)
        call(command, shell = True)