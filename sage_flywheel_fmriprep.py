#!/usr/bin/env python
from subprocess import call
import os, socket, datetime

# We are using different parameters on different host computers due to processing power differences etc. 
host = socket.gethostname()
print("Running on host %s" % host)


volume = "BCI-1"

outfolder = "/Volumes/%s/SAGE/fmriprep" % volume
datafolder = "/Volumes/%s/SAGE/BIDS_data" % volume

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
    outfolder = "/Volumes/%s/SAGE/fmriprep/"
    datafolder = "/Volumes/%s/SAGE/BIDS_data" % volume
elif host == 'qualia.usc.edu':
    licencefile = '/usr/local/freesurfer/license.txt'
    nproc = 100
    fssubjectsdir = "/home/bciuser/fMRI/SAGE/freesurfer"
    workingdir = "/home/bciuser/fMRI/SAGE/fmriprep/working"
    outfolder = "/Volumes/%s/SAGE/fmriprep/"
    datafolder = "/Volumes/%s/SAGE/BIDS_data" % volume
elif host == 'calypso.usc.edu':
    licencefile = '/Applications/freesurfer/license.txt'
    nproc = 20
    fssubjectsdir = "/Users/jtkaplan/fMRI/SAGE/freesurfer"
    workingdir = "/Users/jtkaplan/fMRI/SAGE/fmriprep/working"
    outfolder = "/Users/jtkaplan/fMRI/SAGE/fmriprep"
    datafolder = "/Users/jtkaplan/fMRI/SAGE/BIDS_data"
else:
    print("host unrecognized")

# Run fmriprep
for subject in to_do:

    now = datetime.datetime.now()
    print(now)

    command = "fmriprep-docker -vv --env TZ America/Los_Angeles %s %s participant --participant-label %s --fs-license-file %s --nproc %d --fs-subjects-dir %s -w %s" % (datafolder,outfolder,subject,licencefile,nproc,fssubjectsdir,workingdir)
    print(command)
    call(command,shell=True)
