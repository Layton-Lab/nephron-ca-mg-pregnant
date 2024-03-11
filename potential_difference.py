import matplotlib

# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import os
import argparse
import matplotlib as mpl
label_size = 16
#mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size

seg_list = ['PT', 'S3', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CCD', 'OMCD', 'IMCD']
# seg_list = ['PT', 'S3', 'mTAL', 'cTAL', 'DCT', 'CNT']
seg_early = ['PT', 'S3', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT']
seg_late = ['CCD', 'OMCD', 'IMCD']

# solute_list = ['Na','K','Cl','HCO3','urea','NH4', 'TA', 'Volume']

humOrrat = 'rat'  # set to 'hum' for human model, 'rat for rat model

# conversion factors
if humOrrat == 'rat':
    sup_ratio = 2.0 / 3.0
    neph_per_kidney = 36000  # number of nephrons per kidney
elif humOrrat == 'hum':
    sup_ratio = 0.85
    neph_per_kidney = 1000000
jux_ratio = 1 - sup_ratio
neph_weight = [sup_ratio, 0.4 * jux_ratio, 0.3 * jux_ratio, 0.15 * jux_ratio, 0.1 * jux_ratio, 0.05 * jux_ratio]

p_to_mu = 1e-6  # convert pmol to micromole
cf_solute = neph_per_kidney * p_to_mu

nl_to_ml = 1e-6  # convert nl to ml
cf_volume = neph_per_kidney * nl_to_ml

mu_conv = 1e-3  # from mumol to mmol
min_per_day = 1440
solute_conversion = cf_solute  # mu_conv #* min_per_day
volume_conversion = cf_volume

fig_labels = ['PT', 'S3', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CCD', 'OMCD', 'IMCD', 'urine']


def get_vals(solute, fname, sex):
    os.chdir(fname)

    file_sup_L = open(sex + '_' + humOrrat + '_cTAL_potential_gradient_Lumen_Cell_sup.txt', 'r')

    '''
    file_jux1 = open(sex + '_' + humOrrat + '_cTAL_con_of_Mg_in_Lumen_jux1.txt', 'r')
    file_jux2 = open(sex + '_' + humOrrat + '_cTAL_con_of_Mg_in_Lumen_jux2.txt', 'r')
    file_jux3 = open(sex + '_' + humOrrat + '_cTAL_con_of_Mg_in_Lumen_jux3.txt', 'r')
    file_jux4 = open(sex + '_' + humOrrat + '_cTAL_con_of_Mg_in_Lumen_jux4.txt', 'r')
    file_jux5 = open(sex + '_' + humOrrat + '_cTAL_con_of_Mg_in_Lumen_jux5.txt', 'r')

    temp_jux1 = solute_conversion * neph_weight[1] * float(file_jux1.readline())
    temp_jux2 = solute_conversion * neph_weight[2] * float(file_jux2.readline())
    temp_jux3 = solute_conversion * neph_weight[3] * float(file_jux3.readline())
    temp_jux4 = solute_conversion * neph_weight[4] * float(file_jux4.readline())
    temp_jux5 = solute_conversion * neph_weight[5] * float(file_jux5.readline())

    delivery_early_sup[seg] = solute_conversion * neph_weight[0] * float(file_sup.readline())
    delivery_early_jux[seg] = temp_jux1 + temp_jux2 + temp_jux3 + temp_jux4 + temp_jux5
    delivery_early[seg] = delivery_early_sup[seg] + delivery_early_jux[seg]
    '''

    datalist_sup_L = []
    for i in file_sup_L:
        line = i.split(' ')
        datalist_sup_L.append(float(line[0]))

    file_sup_L.close()

    os.chdir('..')

    '''
    file_jux1.close()
    file_jux2.close()
    file_jux3.close()
    file_jux4.close()
    file_jux5.close()
    '''

    return datalist_sup_L


male_PD = get_vals('Mg', 'Male_rat_normal_multiple', 'male')
female_PD = get_vals('Mg', 'Female_rat_normal_multiple', 'female')
male_PD_NKCC2_100 = get_vals('Mg', 'Male_rat_HCa', 'male')        # NKCC2-100_Male_rat
female_PD_NKCC2_100 = get_vals('Mg', 'Female_rat_HCa', 'female')  # NKCC2-100_Female_rat

print("male", (np.average(male_PD) - np.average(male_PD_NKCC2_100)) / np.average(male_PD))
print("female", (np.average(female_PD) - np.average(female_PD_NKCC2_100)) / np.average(female_PD))

plt.plot(male_PD, label='Male Normal')
plt.plot(male_PD_NKCC2_100, label='Male NKCC2-100')
plt.plot(female_PD, label='Female Normal')
plt.plot(female_PD_NKCC2_100, label='Female NKCC2-100')
plt.legend()
plt.show()