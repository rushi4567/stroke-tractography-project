import nibabel as nib
import pandas as pd
import numpy as np

lesion_path = 'ATLAS_2/Training/R001/sub-r001s001/ses-1/anat/sub-r001s001_ses-1_space-MNI152NLin2009aSym_label-L_desc-T1lesion_mask.nii'
atlas_path = 'JHU_WM_tract/JHU-ICBM-labels-1mm.nii'

lesion_img = nib.load(lesion_path)
atlas_img = nib.load(atlas_path)

lesion_data = lesion_img.get_fdata()
atlas_data = atlas_img.get_fdata()

#ensure voxel resolution matches both atlas and lesion image

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
    2: "middle cerebellar peduncle",
    3:	"pontine crossing tract",
    4:	"genu of corpus callosum",
    5:	"body of corpus callosum",
    6:	"splenium of corpus callosum",
    7:	"fornix",
    8:	"corticospinal tract r",
    9:	"medial lemniscus l",
    12:	"inferior cerebellar peduncle r",
    13:	"inferior cerebellar peduncle l",
    14:	"superior cerebellar peduncle r",
    15:	"superior cerebellar peduncle l",
    16:	"cerebral peduncle r",
    17:	"cerebral peduncle l",
    18:	"anterior limb of internal capsule r",
    19:	"anterior limb of internal capsule l",
    20:	"posterior limb of internal capsule r",
    21: "posterior limb of internal capsule l",
    22:	"retrolenticular part of internal capsule r",
    23:	"retrolenticular part of internal capsule l",
    24:	"anterior corona radiata r",
    25:	"anterior corona radiata l",
    26: "superior corona radiata r",
    27:	"superior corona radiata l",
    28:	"posterior corona radiata r",
    29:	"posterior corona radiata l",
    30:	"posterior thalamic radiation",
    31:	"posterior thalamic radiation",
    32:	"sagittal stratum",
    33:	"sagittal stratum",
    34:	"external capsule r",
    35:	"external capsule l",
    36:	"cingulum",
    37:	"cingulum",
    38:	"cingulum",
    39:	"cingulum",
    40:	"fornix",
    41:	"fornix",
    42:	"superior longitudinal fasciculus r",
    43:	"superior longitudinal fasciculus l",
    44:	"superior fronto-occipital fasciculus",
    45:	"superior fronto-occipital fasciculus",
    46:	"uncinate fasciculus r",
    47:	"uncinate fasciculus l",
    48:	"tapetum r",
    49:	"tapetum l",
}


# create dataframe to store results
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