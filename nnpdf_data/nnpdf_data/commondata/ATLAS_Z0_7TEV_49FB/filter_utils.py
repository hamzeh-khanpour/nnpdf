"""
This module contains helper functions that are used to extract the data values 
from the rawdata files.
"""

import yaml
import pandas as pd
import numpy as np


def get_data_values():
    """
    returns the central data values in the form of a list.
    """

    data_central = []

    hepdata_table = f"rawdata/HEPData-ins1234228-v1-Table_1.yaml"

    with open(hepdata_table, 'r') as file:
        input = yaml.safe_load(file)

    values = input['dependent_variables'][0]['values']

    for value in values:
        # store data central and convert the units
        data_central.append(value['value'] * 1000)

    return data_central


def get_kinematics():
    """
    returns the kinematics in the form of a list of dictionaries.
    """
    kin = []

    hepdata_table = f"rawdata/HEPData-ins1234228-v1-Table_1.yaml"

    with open(hepdata_table, 'r') as file:
        input = yaml.safe_load(file)

    for i, M in enumerate(input["independent_variables"][0]['values']):

        kin_value = {'m_ll': {'min': None, 'mid': (0.5 * (M['low'] + M['high'])), 'max': None}}

        kin.append(kin_value)

    return kin


def get_systematics_dataframe():
    """
    returns the absolute systematic uncertainties in the form of a pandas dataframe.
    """
    sys_rawdata_path = "rawdata/ATLAS-49fb-Zhighmass.csv"

    df = pd.read_csv(sys_rawdata_path)
    data_central = np.array(get_data_values())

    # convert (MULT) percentage unc to absolute unc
    abs_unc_df = (df.T[2:] * data_central).T / 100

    return abs_unc_df


def get_systematics():
    """ """
    abs_unc_df = get_systematics_dataframe()

    uncertainties = []

    for i, unc_dp in enumerate(abs_unc_df.values.T):
        name = f"{abs_unc_df.columns[i]}"
        values = [unc_dp[j] for j in range(len(unc_dp))]
        uncertainties.append([{"name": name, "values": values}])

    return uncertainties


if __name__ == "__main__":
    get_data_values()
    get_systematics_dataframe()
