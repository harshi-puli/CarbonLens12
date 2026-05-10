import pandas as pd
import numpy as np
import seaborn as sns

#colors
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

#Data Cleaning
    #clean_co2(df) takes in the dataframe for the carbon data. 
def clean_co2(df): 
    df = df.rename(columns = {'Unnamed: 1':'Country'})
    df = df[df["Country"] != "Total, all countries or areas"]
    df["Value"] = df["Value"].str.replace(',', '').astype(float)
    df["Series"] = df["Series"].map({"Emissions (thousand metric tons of carbon dioxide)": "co2_total_kt", "Emissions per capita (Metric tons of carbon dioxide)":"co2_per_capita"})
    df = df.pivot_table(
            index = ["Country", "Year"],
            columns = "Series",
            values = "Value" ).reset_index()
    df.to_csv('data/processed/CO2_estimate_cleaned.csv', index=False)
    print(df.head())
    print(f"{GREEN}...Carbon Data Cleaned!{RESET}")
    return df
    
    #clean_consumption(df) takes in the dataframe for the energy consumption data. 
def clean_consumption(df): 
    # run this once to see what you're dealing with
    df = df[df["Code"].notna()]
    df = df.drop("Code", axis = 1) # unnecessary/redundant not always there.
    df = df.rename(columns = {'Entity':'Country'})
    df = df[~df["Country"].isin(["Africa", "Asia", "Northern America", "South America", "Europe", "Oceania"])] # excluding continents 
    df = df.fillna(0.0)
    df.to_csv('data/processed/energy_consumption_cleaned.csv', index=False)
    print(df.head())
    print(f"{GREEN}...Consumption Data Cleaned!{RESET}")
    return df

def merge_data(c_df, ce_df):
    df = c_df.merge(ce_df, left_on = ["Country", "Year"], right_on = ["Country", "Year"])
    df.to_csv('data/output/CO2_AND_ENERGY.csv', index = False)
    print(df.head())
    rint(f"{GREEN}...Merged{RESET}")
    return df


def explore_data(c_df, ce_df):
    #Exploring energy consumption data (ce_df)
    print(f"{CYAN}Exploring data...🌍{RESET}")
    print("\nThese are the energy consumption data columns:")

    column_list = []
    for column in ce_df.columns:
        column_list.append(column)
    print(column_list)

    print("\nNumber of unique values in dataset:")
    print(len(ce_df["Entity"].unique()))

    #Exploring carbon (c_df)
    print("\nThese are the co2 estimate initial columns:")

    column_list = []
    for column in c_df.columns:
        column_list.append(column)
    print(column_list)

def main():
    #Loading File paths
    consumption_data = pd.read_csv('data/raw/energy-consumption-by-source-and-country.csv', encoding='latin-1') 
    carbon_data = pd.read_csv('data/raw/CO2estimate.csv', encoding='latin-1', skiprows=1) # latin-1 encoding to avoid issues with characters not being in UTF-8.

    explore_data(carbon_data, consumption_data)

    #call clean_data()
    print("\nCleaning data...")
    print(f"{YELLOW}Energy Consumption{RESET}")
    consumption_data = clean_consumption(consumption_data)
    print(f"{YELLOW}Carbon - CO2 Estimate{RESET}")
    carbon_data = clean_co2(carbon_data)

    #call merge_data()
    print("\nMerging data...")
    full_data = merge_data(carbon_data, consumption_data)

if __name__ == "__main__":
    main()