#!/usr/bin/env python
from subprocess import call
import os, sys

# Fix the residuals file for one subject
# The res4d file created by FSL contains the residuals, but each voxel is centered at zero so
# the next FSL analysis cannot distinguish brain from background and failes. 
# Here, we add a constant to the in-brain voxels. 

#command line options
if (len(sys.argv) < 2):
	print("\n\tusage: %s <subject>\n" % sys.argv[0])
	sys.exit()
else:
	subject = sys.argv[1]

print("Working on residuals for subject %s" % subject)
if "sub-" not in subject:
	subject = "sub-%s" % subject

basefolder = "/Volumes/BCI/SAGE"
outfolder = "%s/fsl-pre" % basefolder

for run in range(1,5):
    #add a constant to the in-brain voxels in the residuals file so that FSL can tell it from the background
    maskfile = "%s/%s/%s_run-0%d_pre.feat/mask.nii.gz" % (outfolder,subject,subject,run)
    newmaskfile = "%s/%s/%s_run-0%d_pre.feat/mask_high.nii.gz" % (outfolder,subject,subject,run)
    residfile = "%s/%s/%s_run-0%d_pre.feat/stats/res4d.nii.gz" % (outfolder,subject,subject,run)
    newresidfile = "%s/%s/%s_run-0%d_pre.feat/stats/res4d_bg.nii.gz" % (outfolder,subject,subject,run)
    command = "fslmaths %s -mul 10000 %s" % (maskfile,newmaskfile)
    print(command)
    call(command, shell = True)
    command = "fslmaths %s -add %s %s" % (residfile, newmaskfile, newresidfile)
    print(command)
    call(command, shell = True)