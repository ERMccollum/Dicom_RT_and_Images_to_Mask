__author__ = 'Brian M Anderson'
# Created on 4/16/2020


Contour_Names = ['Lung (Left)', 'Lung (Right)']
image_path = r'\\mymdafiles\di_data1\Morfeus\Lung_Exports\From_Raystation'
'''
This will print if any rois are missing at certain locations
'''
check_rois = False
if check_rois:
    from .Image_Array_And_Mask_From_Dicom_RT import Dicom_to_Imagestack
    Dicom_Reader = Dicom_to_Imagestack(get_images_mask=False,Contour_Names=Contour_Names)
    Dicom_Reader.down_folder(image_path)

'''
This will turn the dicom into niftii files
'''
nifti_path = r'\\mymdafiles\di_data1\Morfeus\Lung_Exports\Nifti_Files'
write_files = False
if write_files:
    from .Image_Array_And_Mask_From_Dicom_RT import Dicom_to_Imagestack, os
    Dicom_Reader = Dicom_to_Imagestack(get_images_mask=False, Contour_Names=Contour_Names, desc='Test')
    Dicom_Reader.down_folder(image_path)
    Dicom_Reader.write_parallel(out_path=nifti_path, excel_file=os.path.join('.', 'MRN_Path_To_Iteration.xlsx'))

'''
Distribute the nifti files to other folders
'''
distribute = False
if distribute:
    from Pre_Processing.Dicom_RT_and_Images_to_Mask.Distribute_Train_Test_Validation import distribute
    distribute('HN',niftii_path=nifti_path, excel_file=os.path.join('.','MRN_Path_To_Iteration.xlsx'))

'''
Now that they're distributed, turn them into the tfrecord structure
# '''
make_single_images = True
nifti_path = r'I:\Morfeus\BReber\HN_Status_Pred\Nifti_Files'
if make_single_images:
    from Pre_Processing.Make_Single_Images.Make_TFRecord_Class import write_tf_record
    from Pre_Processing.Make_Single_Images.Image_Processors_Module.Image_Processors_TFRecord import *
    image_processors = [Add_Dose(), Clip_Images_By_Extension(extension=16), Distribute_into_3D(min_z=64, max_z=64, mirror_small_bits=True)] #, Add_Dose(), Sum_Dose(),
    write_tf_record(os.path.join(nifti_path, 'Train'), record_name='Train', image_processors=image_processors,
                      is_3D=True, rewrite=False, thread_count=5)
    # write_tf_record(os.path.join(nifti_path, 'Validation'), record_name='Validation', image_processors=image_processors,
    #                   is_3D=True, rewrite=True, thread_count=5)
    # write_tf_record(os.path.join(nifti_path, 'Test'), record_name='Test', image_processors=image_processors,
    #                   is_3D=True, rewrite=True, thread_count=5)