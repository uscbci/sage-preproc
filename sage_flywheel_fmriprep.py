#!/usr/bin/env python
from subprocess import call
import os, socket

# We are using different parameters on different host computers due to processing power differences etc. 
host = socket.gethostname()
print("Running on host %s" % host)

outfolder = "/Volumes/BCI/SAGE/fmriprep"
datafolder = "/Volumes/BCI/SAGE/BIDS_data"

donefolders = [fol for fol in os.listdir(outfolder) if "sub-" in fol and ".html" not in fol]
datafolders = [fol for fol in os.listdir(datafolder) if "sub-" in fol]

to_do = []
for subject in datafolders:
    if subject not in donefolders:
        to_do.append(subject)


numtodo = len(to_do)
print("Subjects to do (%d):" % numtodo)
print(to_do)
to_do.sort()

# Make sure docker.sock is writeable
call("sudo chmod 777 /var/run/docker.sock",shell=True)

# Set paths and num processors depending on host
if host=='cortex.usc.edu':
    licencefile = '/Applications/freesurfer/license.txt'
    nproc = 6
    fssubjectsdir = "/Applications/freesurfer/subjects"
    workingdir = "/Users/bciuser/fMRI/sage/fmriprep/working"
elif host == 'qualia.usc.edu':
    licencefile = '/usr/local/freesurfer/license.txt'
    nproc = 100
    fssubjectsdir = "/home/bciuser/fMRI/SAGE/freesurfer"
    workingdir = "/home/bciuser/fMRI/SAGE/fmriprep/working"
else:
    print("host unrecognized")

# Run fmriprep
for subject in to_do:
    command = "fmriprep-docker -vv /Volumes/BCI/SAGE/BIDS_data /Volumes/BCI/SAGE/fmriprep/ participant --participant-label %s --fs-license-file %s --nproc %d --fs-subjects-dir %s -w %s" % (subject,licencefile,nproc,fssubjectsdir,workingdir)
    print(command)
    call(command,shell=True)
