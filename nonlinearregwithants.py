
import ants
import pickle
# Load the 3D CT and MRI images
ct_image = ants.image_read('/media/atul/WDJan20222/WASHU_WORKS/PROJECTS/SNIPR/deepregbasedregistration/scct_strippedResampled1.nii.gz')   # Template (CT)
mri_image = ants.image_read('/media/atul/WDJan20222/WASHU_WORKS/PROJECTS/SNIPR/deepregbasedregistration/mritemplate/mni_icbm152_t1_tal_nlin_sym_55_ext_bet_grayscct_strippedResampled1lin1.nii.gz')
# mri_image.nii') # Target (MRI)

registration_result = ants.registration(
    fixed=mri_image,                        # Target image (fixed)
    moving=ct_image,                        # Template image (moving)
    type_of_transform='SyN',                # Non-linear transformation: SyN (Symmetric Normalization)
    metric='Mattes',                        # Metric: Mutual Information (Mattes MI)
    syn_metric='Mattes',                    # Mutual Information for the SyN transform
    reg_iterations=[2000, 1000, 500, 200],  # Increasing the number of iterations at each level
    convergence_threshold=1e-7,             # Smaller convergence threshold for better accuracy
    convergence_window_size=15,             # Larger window size for better convergence estimation
    smoothing_sigmas=[4, 2, 1, 0],          # Apply more smoothing for coarser levels, refine as you move to finer levels
    shrink_factors=[8, 4, 2, 1],            # Multi-resolution strategy (start coarse, end fine)
    transform_parameters=(0.1,),            # Smaller gradient step size for better precision
    verbose=True,                           # Verbose mode to track progress
    histogram_matching=True                 # Enable histogram matching (useful for multi-modal images like CT and MRI)
)

# Extract the registered (warped) image
warped_ct_image = registration_result['warpedmovout']

# Save the warped CT image
ants.image_write(warped_ct_image, './warped_mri_to_ct_mi.nii')

# # Optional: Save the transform parameters (forward and inverse transforms)
# ants.write_transform(registration_result['fwdtransforms'], './forward_transform_mi.mat')
# ants.write_transform(registration_result['invtransforms'], './inverse_transform_mi.mat')
#
# print("Registration complete using Mutual Information. Warped CT image saved.")
# 3. Save the entire registration result using pickle for later reloading
with open('registration_result.pkl', 'wb') as f:
    pickle.dump(registration_result, f)