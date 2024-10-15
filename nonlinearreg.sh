#!/bin/bash
source /opt/antspyvenv/bin/activate
session_id="SNIPR02_E14051"
## DOWNLOAD THE SELECTED NIFTI FILE:
URI='/data/experiments/'${session_id}
resource_dir='NIFTI_LOCATION'
dir_to_receive_the_data="/workinginput/"
output_csvfile=${session_id}_NIFTI_LOCATION.csv
call_uploadsinglefile_with_URI_arguments=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile})
outputfiles_present=$(python /software/download_with_session_ID.py "${call_uploadsinglefile_with_URI_arguments[@]}")

## download the required files:

##which python
#python nonlinearregwithants.py
#/opt/antspyvenv/bin/python


