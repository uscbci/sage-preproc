# sage-preproc
Preprocessing pipeline for SAGE project

1. First, sage_flywheel_fmrprep runs fmriprep using docker on any subject that appears to be unprocessed. 

2. Then sage_fsl_preproc uses FSL to take confound regressors created by fmriprep and regress them out of the data. Also does spatial smoothing and temporal filtering. This script also calls sage_confound_selection.py in order to extract the desired confounds from the fmriprep results. 