#!/bin/bash
source /opt/antspyvenv/bin/activate
session_id="SNIPR02_E14051"
session_metadata_filename=${session_id}_metadata.csv
call_uploadsinglefile_with_URI_arguments=('call_get_metadata_session' ${session_id} ${nifti_reg_filename} ${resource_dirname})
outputfiles_present=$(python /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")
## download the required files:

##which python
#python nonlinearregwithants.py
#/opt/antspyvenv/bin/python


