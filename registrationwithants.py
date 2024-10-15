
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
    outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.nii.gz')
    T_outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.pkl')
    registration_result = ants.registration(
        fixed=fixedimage,                        # Target image (fixed)
        moving=movingimage,                        # Template image (moving)
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
    outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.nii.gz')
    T_outputfilename=os.path.join(output_dir,'mov_'+os.path.basename(movingimage).split('.nii')[0]+'_fix_'+os.path.basename(fixedimage).split('.nii')[0]+'.pkl')

    # Perform linear (Affine) registration with advanced parameters
    registration_result = ants.registration(
        fixed=fixedimage,                        # Target image (fixed)
        moving=movingimage,                        # Template image (moving)
        type_of_transform='Affine',             # Linear transformation: Affine (can change to 'Rigid')
        metric='Mattes',                        # Metric: Mutual Information (Mattes MI) for multi-modal registration
        reg_iterations=[2000, 1000, 500],       # Number of iterations for refinement
        convergence_threshold=1e-6,             # Convergence threshold for better precision
        convergence_window_size=10,             # Window size for convergence
        smoothing_sigmas=[2, 1, 0],             # Smoothing applied at different levels
        shrink_factors=[4, 2, 1],               # Multi-resolution strategy (coarse to fine)
        transform_parameters=(0.1,),            # Step size for gradient descent optimization
        verbose=True,                           # Verbose output for tracking
        histogram_matching=True                 # Histogram matching for multi-modal images
    )

    # Save the registered (warped) CT image
    warped_ct_image = registration_result['warpedmovout']
    ants.image_write(warped_ct_image, outputfilename)

    # # Save the forward and inverse transforms (automatically saved by ANTs)
    # forward_transform = registration_result['fwdtransforms'][0]
    # inverse_transform = registration_result['invtransforms'][0]
    # print(f"Forward transform saved to: {forward_transform}")
    # print(f"Inverse transform saved to: {inverse_transform}")
    #
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