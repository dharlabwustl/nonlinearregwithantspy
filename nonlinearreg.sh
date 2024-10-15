#!/bin/bash
source /opt/antspyvenv/bin/activate
# Function to get the column number given the column name
get_column_number() {
    local csv_file="$1"   # The CSV file to search in
    local column_name="$2" # The column name to find

    # Get the header (first line) of the CSV file
    header=$(head -n 1 "$csv_file")
    # Split the header into an array of column names
    IFS=',' read -r -a columns <<< "$header"

    # Loop through the columns and find the index of the column name
    for i in "${!columns[@]}"; do
        if [[ "${columns[$i]}" == "$column_name" ]]; then
            # Print the 1-based index (cut and other tools expect 1-based indexes)
            echo $((i ))
            return
        fi
    done

    # If the column is not found, print an error and return a failure status
    echo "Column '$column_name' not found!" >&2
    return 1
}




session_id="SNIPR02_E14051"
## DOWNLOAD THE SELECTED NIFTI FILE INFORMATION:
URI='/data/experiments/'${session_id}
resource_dir='NIFTI_LOCATION'
dir_to_receive_the_data="/workinginput/"
output_csvfile=${session_id}_NIFTI_LOCATION.csv
call_function=('call_get_resourcefiles_metadata_saveascsv_args' ${URI} ${resource_dir} ${dir_to_receive_the_data} ${output_csvfile})
outputfiles_present=$(python /software/download_with_session_ID.py "${call_function[@]}")
column_name="URI"
column_number=$(get_column_number "${dir_to_receive_the_data}/${output_csvfile}" "$column_name")
echo ${column_number}
nifti_locationfile_url=$(awk -F',' -v row=2 -v col=$((column_number+1)) 'NR==row {print $col}' ${dir_to_receive_the_data}/${output_csvfile})
echo ${value}
call_function=('call_download_a_singlefile_with_URIString' ${nifti_locationfile_url} $(basename ${nifti_locationfile_url} ) ${dir_to_receive_the_data} ${output_csvfile})
outputfiles_present=$(python /software/download_with_session_ID.py "${call_function[@]}")


##which python
#python nonlinearregwithants.py
#/opt/antspyvenv/bin/python


