from apriori_implementation import apriori
import pandas
import numpy as np
import os

file_path = os.path.realpath('..') + '/apriori_implementacao/resources/house-votes-84.data'

raw = pandas.read_csv(file_path, header=None)

etl_raw = raw.copy()

etl_raw[1] = np.where(raw[1] == 'n', 'handicapped-infants_NAY', np.where(raw[1] == 'y', 'handicapped-infants_YEA', 'handicapped-infants_UNKNOWN'))
etl_raw[2] = np.where(raw[2] == 'n', 'water-project-cost-sharing_NAY', np.where(raw[2] == 'y', 'water-project-cost-sharing_YEA', 'water-project-cost-sharing_UNKNOWN'))
etl_raw[3] = np.where(raw[3] == 'n', 'adoption-of-the-budget-resolution_NAY', np.where(raw[3] == 'y', 'adoption-of-the-budget-resolution_YEA', 'adoption-of-the-budget-resolution_UNKNOWN'))
etl_raw[4] = np.where(raw[4] == 'n', 'physician-fee-freeze_NAY', np.where(raw[4] == 'y', 'physician-fee-freeze_YEA', 'physician-fee-freeze_UNKNOWN'))
etl_raw[5] = np.where(raw[5] == 'n', 'el-salvador-aid_NAY', np.where(raw[5] == 'y', 'el-salvador-aid_YEA', 'el-salvador-aid_UNKNOWN'))
etl_raw[6] = np.where(raw[6] == 'n', 'religious-groups-in-schools_NAY', np.where(raw[6] == 'y', 'religious-groups-in-schools_YEA', 'religious-groups-in-schools_UNKNOWN'))
etl_raw[7] = np.where(raw[7] == 'n', 'anti-satellite-test-ban_NAY', np.where(raw[7] == 'y', 'anti-satellite-test-ban_YEA', 'anti-satellite-test-ban_UNKNOWN'))
etl_raw[8] = np.where(raw[8] == 'n', 'aid-to-nicaraguan-contras_NAY', np.where(raw[8] == 'y', 'aid-to-nicaraguan-contras_YEA', 'aid-to-nicaraguan-contras_UNKNOWN'))
etl_raw[9] = np.where(raw[9] == 'n', 'mx-missile_NAY', np.where(raw[9] == 'y', 'mx-missile_YEA', 'mx-missile_UNKNOWN'))
etl_raw[10] = np.where(raw[10] == 'n', 'immigration_NAY', np.where(raw[10] == 'y', 'immigration_YEA', 'immigration_UNKNOWN'))
etl_raw[11] = np.where(raw[11] == 'n', 'synfuels-corporation-cutback_NAY', np.where(raw[11] == 'y', 'synfuels-corporation-cutback_YEA', 'synfuels-corporation-cutback_UNKNOWN'))
etl_raw[12] = np.where(raw[12] == 'n', 'education-spending_NAY', np.where(raw[12] == 'y', 'education-spending_YEA', 'education-spending_UNKNOWN'))
etl_raw[13] = np.where(raw[13] == 'n', 'superfund-right-to-sue_NAY', np.where(raw[13] == 'y', 'superfund-right-to-sue_YEA', 'superfund-right-to-sue_UNKNOWN'))
etl_raw[14] = np.where(raw[14] == 'n', 'crime_NAY', np.where(raw[14] == 'y', 'crime_YEA', 'crime_UNKNOWN'))
etl_raw[15] = np.where(raw[15] == 'n', 'duty-free-exports_NAY', np.where(raw[15] == 'y', 'duty-free-exports_YEA', 'duty-free-exports_UNKNOWN'))
etl_raw[16] = np.where(raw[16] == 'n', 'export-administration-act-south-africa_NAY', np.where(raw[16] == 'y', 'export-administration-act-south-africa_YEA', 'export-administration-act-south-africa_UNKNOWN'))


dataset_size = etl_raw.shape[0]

transactions_list = []
for i in range(dataset_size):
    transactions_list.append(",".join(list(etl_raw.iloc[i,:])))

data = {'col': transactions_list}

df = pandas.DataFrame.from_dict(data)

apriori(df, 0.45, 0.8)



