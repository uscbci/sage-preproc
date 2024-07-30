#!/usr/bin/env python

import os
import shutil
import csv
import pandas as pd
import sys
from subprocess import call

#command line options
if (len(sys.argv) < 2):
	print("\n\tusage: %s <subject>\n" % sys.argv[0])
	sys.exit()
else:
	subject = sys.argv[1]

print("Working on confounds for subject %s" % subject)

DATA_BASE="/Volumes/BCI/SAGE"
OUTPUT_DIR="%s/fsl-pre/confound_files" % DATA_BASE
INPUT_DIR="%s/fmriprep" % DATA_BASE

task_names = ["hiAP_run-01", "hiAP_run-02","hiAP_run-03","hiAP_run-04"]

for i in range(len(task_names)):
	task_name = task_names[i]

	print("Working on task %s" % task_name)

	conf_file = "%s/%s/ses-EichSAGE/func/%s_ses-EichSAGE_task-%s_desc-confounds_timeseries.tsv" % (INPUT_DIR, subject, subject, task_name)

	print("Confound file: %s" % conf_file)
	confs = pd.read_csv(conf_file,sep='\t')

	target_cols = ["a_comp_cor_00", "trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]

	newdf = confs.loc[:, confs.columns.isin(target_cols) | confs.columns.str.contains('motion') ]

	final_file = "%s/sub-%s_confounds_%s.tsv" % (OUTPUT_DIR, subject, task_name)

	newdf.to_csv(final_file,sep="\t",index=False)


print("Done with confound creation for %s" % subject)
print('\n')
