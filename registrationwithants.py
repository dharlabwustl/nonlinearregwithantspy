
import ants
import pickle,sys,os,argparse
# from download_upload_with_snipr import *
# Load the 3D CT and MRI images
def call_nonlinearregistration(args):
    movingimage = args.stuff[1]## fixed ##ants.image_read('/software/cttemplate/scct_strippedResampled1.nii.gz')   # Template (CT)
    fixedimage = args.stuff[2] ## ants.image_read('/software/mritemplate/mni_icbm152_t1_tal_nlin_sym_55_ext_bet_grayscct_strippedResampled1lin1.nii.gz')
    # mri_image.nii') # Target (MRI)
    output_dir=args.stuff[3]
    nonlinearregistration(movingimage,fixedimage,output_dir)

def nonlinearregistration(movingimage,fixedimage,output_dir):
    # movingimage = sys.argv[1] ## fixed ##ants.image_read('/software/cttemplate/scct_strippedResampled1.nii.gz')   # Template (CT)
    # fixedimage = sys.argv[2] ## ants.image_read('/software/mritemplate/mni_icbm152_t1_tal_nlin_sym_55_ext_bet_grayscct_strippedResampled1lin1.nii.gz')
    # # mri_image.nii') # Target (MRI)
    # output_dir=sys.argv[3]
    movingimage_ant=ants.image_read(movingimage)
    fixedimage_ant=ants.image_read(fixedimage)
    outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.nii.gz')
    T_outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.pkl')
    registration_result = ants.registration(
        fixed=fixedimage_ant,                        # Target image (fixed)
        moving=movingimage_ant,                        # Template image (moving)
        type_of_transform='SyN',                # Non-linear transformation: SyN (Symmetric Normalization)
        metric='Mattes',                        # Metric: Mutual Information (Mattes MI)
        syn_metric='Mattes',                    # Mutual Information for the SyN transform
        reg_iterations=[20000, 10000, 5000, 2000],  # Increasing the number of iterations at each level
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
    ants.image_write(warped_ct_image, outputfilename)

    # # Optional: Save the transform parameters (forward and inverse transforms)
    # ants.write_transform(registration_result['fwdtransforms'], './forward_transform_mi.mat')
    # ants.write_transform(registration_result['invtransforms'], './inverse_transform_mi.mat')
    #
    # print("Registration complete using Mutual Information. Warped CT image saved.")
    # 3. Save the entire registration result using pickle for later reloading
    with open(T_outputfilename, 'wb') as f:
        pickle.dump(registration_result, f)
def call_linearregistration(args):
    movingimage = args.stuff[1]## fixed ##ants.image_read('/software/cttemplate/scct_strippedResampled1.nii.gz')   # Template (CT)
    fixedimage = args.stuff[2] ## ants.image_read('/software/mritemplate/mni_icbm152_t1_tal_nlin_sym_55_ext_bet_grayscct_strippedResampled1lin1.nii.gz')
    # mri_image.nii') # Target (MRI)

    output_dir=args.stuff[3]
    linearregistration(movingimage,fixedimage,output_dir)

def linearregistration(movingimage,fixedimage,output_dir):
    # movingimage = sys.argv[1] ## fixed ##ants.image_read('/software/cttemplate/scct_strippedResampled1.nii.gz')   # Template (CT)
    # fixedimage = sys.argv[2] ## ants.image_read('/software/mritemplate/mni_icbm152_t1_tal_nlin_sym_55_ext_bet_grayscct_strippedResampled1lin1.nii.gz')
    # # mri_image.nii') # Target (MRI)
    # output_dir=sys.argv[3]
    movingimage_ant=ants.image_read(movingimage)
    fixedimage_ant=ants.image_read(fixedimage)
    outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.nii.gz')
    T_outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.pkl')

    # Perform an initial rigid registration to roughly align the images
    initial_registration = ants.registration(
        fixed=fixedimage_ant,                        # Target image (fixed)
        moving=movingimage_ant,                        # Template image (moving)
        type_of_transform='Rigid',              # Initial rigid registration
        metric='Mattes',                        # Mutual Information (MI) for multi-modal registration
        reg_iterations=[3000, 2000, 1000],       # Increase iterations for better alignment
        convergence_threshold=1e-7,              # Small convergence threshold
        convergence_window_size=10,
        smoothing_sigmas=[3, 2, 1],              # Smoothing for coarse to fine alignment
        shrink_factors=[6, 4, 2],                # More coarse to fine strategy
        transform_parameters=(0.05,),            # Small step size for gradient descent
        verbose=True,
        histogram_matching=True
    )

    # Apply the rigidly aligned image for the affine registration
    rigidly_aligned_ct = initial_registration['warpedmovout']

    # Perform the affine registration with finer parameters
    registration_result = ants.registration(
        fixed=fixedimage_ant,                        # Target image (fixed)
        moving=rigidly_aligned_ct,              # Rigidly aligned template (CT)
        type_of_transform='Affine',             # Affine transformation (linear)
        metric='Mattes',                        # Mutual Information for multi-modal registration
        reg_iterations=[5000, 3000, 2000, 1000],# Increased iterations for higher resolution accuracy
        convergence_threshold=1e-9,             # Smaller threshold for better convergence
        convergence_window_size=20,             # Larger window size for checking convergence
        smoothing_sigmas=[4, 2, 1, 0],          # Reduced smoothing at finer levels (down to 0)
        shrink_factors=[8, 6, 4, 2, 1],         # More levels of shrinking for higher accuracy
        transform_parameters=(0.01,),           # Very small step size for gradient descent optimization
        verbose=True,
        histogram_matching=True        # Histogram matching enabled
    )

    # Save the warped (registered) CT image
    warped_ct_image = registration_result['warpedmovout']
    ants.image_write(warped_ct_image, outputfilename) #'warped_ct_to_mri_affine_improved.nii')



# Save the entire registration result using pickle for future use
    with open(T_outputfilename, 'wb') as f:
        pickle.dump(registration_result, f)

    print("Affine registration complete. Warped CT image saved.")


def main():
    print("WO ZAI ::{}".format("main"))
    parser = argparse.ArgumentParser()
    parser.add_argument('stuff', nargs='+')
    args = parser.parse_args()
    name_of_the_function=args.stuff[0]
    return_value=0
    if name_of_the_function == "call_nonlinearregistration":
        return_value=call_nonlinearregistration(args)
    if name_of_the_function == "call_linearregistration":
        print("WO ZAI ::{}".format(name_of_the_function))
        return_value=call_linearregistration(args)
    if "call" not in name_of_the_function:
        globals()[args.stuff[0]](args)
    return return_value
if __name__ == '__main__':
    main()