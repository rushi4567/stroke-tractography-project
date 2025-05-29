import nibabel as nib
import pandas as pd
import numpy as np

lesion_path = 'ATLAS_2/Training/R001/sub-r001s001/ses-1/anat/sub-r001s001_ses-1_space-MNI152NLin2009aSym_label-L_desc-T1lesion_mask.nii'
atlas_path = 'JHU_WM_tract/JHU-ICBM-labels-1mm.nii'

lesion_img = nib.load(lesion_path)
atlas_img = nib.load(atlas_path)

lesion_data = lesion_img.get_fdata()
atlas_data = atlas_img.get_fdata()



from nilearn.image import resample_to_img
resampled_lesion_img = resample_to_img(
    source_img=lesion_img, 
    target_img=atlas_img,
    interpolation='nearest')
lesion_data=resampled_lesion_img.get_fdata()

lesion_voxels = lesion_data > 0
overlap = atlas_data[lesion_voxels]

labels, counts = np.unique(overlap[overlap > 0], return_counts=True)

for label, count in zip(labels, counts):
    print(f"Label {int(label)}: {count} voxels")

#label tract names based off int value 

tracts = {
    2: "Anterior limb of internal capsule (L)",
    3: "Anterior limb of internal capsule (R)",
    4: "Posterior limb of internal capsule (L)",
    5: "Posterior limb of internal capsule (R)",
    6: "Retrolenticular part of internal capsule (L)",
    7: "Retrolenticular part of internal capsule (R)",
    8: "Anterior corona radiata (L)",
    9: "Anterior corona radiata (R)",
    10: "Superior corona radiata (L)",
    11: "Superior corona radiata (R)",
    12: "Posterior corona radiata (L)",
    13: "Posterior corona radiata (R)",
    14: "Posterior thalamic radiation (L)",
    15: "Posterior thalamic radiation (R)",
    16: "Sagittal stratum (L)",
    17: "Sagittal stratum (R)",
    18: "External capsule (L)",
    19: "External capsule (R)",
    20: "Cingulum (cingulate gyrus, L)",
    21: "Cingulum (cingulate gyrus, R)",
     22: "Superior corona radiata (R)",
    23: "Posterior corona radiata (L)",
    24: "Posterior corona radiata (R)",
    25: "Posterior thalamic radiation (L)",
    26: "Posterior thalamic radiation (R)",
    27: "Sagittal stratum (L)",
    28: "Sagittal stratum (R)",
    29: "External capsule (L)",
    30: "External capsule (R)",
    31: "Cingulum (cingulate gyrus, L)",
    32: "Cingulum (cingulate gyrus, R)",
    33: "Cingulum (hippocampus, L)",
    34: "Cingulum (hippocampus, R)",
    35: "Fornix / stria terminalis (L)",
    36: "Fornix / stria terminalis (R)",
    37: "Superior longitudinal fasciculus (L)",
    38: "Superior longitudinal fasciculus (R)",
    39: "Superior fronto-occipital fasciculus (L)",
    40: "Superior fronto-occipital fasciculus (R)",
    41: "Uncinate fasciculus (L)",
    42: "Uncinate fasciculus (R)",
    43: "Tapetum (L)",
    44: "Tapetum (R)",
    45: "Forceps major",
    46: "Forceps minor",
    47: "Parieto-occipital pontine tract (L)",
    48: "Parieto-occipital pontine tract (R)",
    49: "Temporo-parietal pontine tract (L)",
    50: "Temporo-parietal pontine tract (R)"
}


# create DataFrame to store the results
results = []
for label, count in zip(labels, counts):
    tract_name = tracts.get(int(label), "Unknown Tract")
    results.append({
        'Label': int(label),
        'Tract': tract_name,
        'OverlapVoxels': int(count)
    })

df = pd.DataFrame(results)
df.to_csv('tract_overlap_sub-r001s001.csv', index=False)
print(df)