import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Author @Muhammad Shoaib Manzoor"""


def df_maker(filename):
    """This function reads the file name and returns two dataframes
    One with countries as columns and one with"""
    
    #Removing unnecessary rows from the top & bottom.
    df = pd.read_csv(filename, skiprows=3)
    df.drop('Unnamed: 67', axis=1, inplace=True)
    df.dropna(axis=1, thresh=10, inplace=True)

    df_years = df.set_index(['Country Code', 'Indicator Code'])
    df_countries = df_years.T
    df_countries.columns.name = None
    return df_years, df_countries


def collation_plotter(df, countries, visual, indicator_code, indicator_name):
    """This function takes a dataframe with years as column, countries for
    which data is to be graphed, visual defines the visualization to be
    used for comparisson, the indicator code to be compared in graph
    and the indicator name to be displayed as label on the graph."""


    # Select the indicator and drop unnecessary columns
    indicator_set = df.xs(indicator_code, level='Indicator Code')/
                .drop(['Indicator Name', 'Country Name'],
                         axis=1, errors='ignore')
    
    # Filter out countries not in the given list
    countries_set = indicator_set.loc[countries, :]

    # Transpose the DataFrame for better visualization
    country_set_transposed = countries_set.T

    # Select data for every 5th year
    data_5yr = country_set_transposed.iloc[0::5, :]

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    data_5yr.plot(kind=visual, stacked=False)

    # Set plot labels and legend
    plt.ylabel(ylabel)
    plt.xlabel('Years')
    plt.legend(
        title='Countries', 
        loc='upper center', 
        frameon=False, 
        ncol=5, 
        borderaxespad=-4)

    # Show the plot
    plt.show()


def explorer(df, country_code, indicators, years):
    """"This function displays the correlation heatmap between the indicators 
    selected from the country code and the indicators parameters for 
    the number of years mentioned in the years parameter"""

    country_set = df[country_code]
    country_set = country_set.T.reset_index()

    # Selecting the mentioned indicators to narrow down the data.
    country_set = country_set[country_set['Indicator Name'].isin(indicators)]

    # pivotting the data by mean values for correlation function.
    pivotted_set = country_set.pivot_table(columns='Indicator Name', 
                                            values=years, aggfunc=np.mean)

    # Plotting a heat map using correlation matrix.
    sns.heatmap(
        pivotted_set.corr(),
        annot=True, 
        cmap='coolwarm', 
        fmt='.2f', 
        linewidths=.5)

    print('/nBrief Description of Data: ', pivotted_set.describe())
    print('/nMeadian values of each Indicator: ', pivotted_set.median())
    print('/nStandard deviation between each Indicators: ', /
        pivotted_set.std())



filename = './Data/API_19_DS2_en_csv_v2_6183479.csv'

df_years, df_countries = df_maker(filename)

# Countries to be used for comparrison.
countries = ['DEU', 'FRA', 'GBR', 'ITA']

# Lets have a look at the populations of the selected countries.
collation_plotter(df_years, countries, 'line','SP.POP.TOTL', 
                    'Population Total')

collation_plotter(df_years, countries, 'line','EN.ATM.CO2E.KT', 
                    'Carbon Emissions(KT)')

# Naming all the indicators for the country with the highest Carbon emissions.
indicator_names = ['Electric power consumption (kWh per capita)',
'Energy use (kg of oil equivalent per capita)',
'Annual freshwater withdrawals, total (billion cubic meters)',
'Urban population growth (annual %)', 'CO2 emissions (kt)']

# Country selected to have the most Carbon emissions.
country_name = ['Germany']
country_code = 'DEU'

# Years to evaluate each indicator for.
years_data = ['1960','1965','1970','1975','1980','1985',
                '1990','1995','2000','2005','2010','2015','2020']

explorer(df_countries, country_code, indicator_names, years_data)