import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def df_maker(filename):
    """This function reads the file name and returns two dataframes
    One with countries as columns and one with"""
    df = pd.read_csv(filename, skiprows=3)
    df.drop('Unnamed: 67', axis=1, inplace=True)
    df_years = df.set_index(['Country Code', 'Indicator Code'])
    df_countries = df_years.T
    df_countries.columns.name = None
    return df_years, df_countries


filename = './Data/API_19_DS2_en_csv_v2_6183479.csv'

df_years, df_countries = df_maker(filename)

