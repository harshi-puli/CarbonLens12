import pandas as pd
import numpy as np
import re

#colors
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

#country name mapping 
country_mapping = {
    "United States of America": "United States",
    "Russian Federation": "Russia",
    "Viet Nam": "Vietnam",
    "Republic of Korea": "South Korea",
    "Dem. Rep. of the Congo": "Democratic Republic of Congo",
    "China, Hong Kong SAR": "Hong Kong",
    "Türkiye": "Turkey",
    "Syrian Arab Republic": "Syria",
    "Brunei Darussalam": "Brunei",
    "Bolivia": "Bolivia",        # has trailing space issue, strip() will fix
    "Curaçao": "Curacao",        # accent mismatch
    "Netherlands Antilles": "Netherlands Antilles",  # strip() will fix
    "Côte d\x92Ivoire": "Ivory Coast"
}

gdp_mapping = {
    "Cote d'Ivoire": "Ivory Coast",
    "Korea, Rep.": "South Korea",
    "Congo, Dem. Rep.": "Democratic Republic of Congo",
    "Iran, Islamic Rep.": "Iran",
    "Turkiye": "Turkey",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Bahamas, The": "Bahamas",
    "Gambia, The": "Gambia",
    "St. Lucia": "Saint Lucia",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Vincent and the Grenadines": "Saint Vincent & Grenadines",
    "St. Martin": "Saint Martin",
    "Venezuela, RB": "Venezuela",
    "Egypt, Arab Rep.": "Egypt",
    "Tanzania": "United Rep. of Tanzania",
    "Slovak Republic": "Slovakia",
    "Hong Kong SAR, China": "Hong Kong",
    "Moldova": "Republic of Moldova",
    "Yemen, Rep.": "Yemen",
    "Congo, Rep.": "Republic of Congo",
    "West Bank and Gaza": "State of Palestine",
    "Micronesia, Fed. Sts.": "Micronesia",
    "Lao PDR": "Lao People's Dem. Rep.",
    "Macao SAR, China": "China, Macao SAR",
    "Korea, Dem. People's Rep.": "Dem. People's Rep. Korea",
}

gdp_aggregates = [
    "IDA total", "Africa Eastern and Southern", "Sub-Saharan Africa",
    "Upper middle income", "Euro area", "IBRD only", "South Asia",
    "Post-demographic dividend", "European Union", "Africa Western and Central",
    "Small states", "Arab World", "Latin America & Caribbean",
    "Other small states", "Middle income", "Early-demographic dividend",
    "Lower middle income", "Europe & Central Asia", "IDA only",
    "Caribbean small states", "IDA & IBRD total", "High income",
    "East Asia & Pacific", "North America", "OECD members",
    "Low & middle income", "Not classified", "IDA blend",
    "Least developed countries: UN classification", "Low income",
    "Late-demographic dividend", "Pre-demographic dividend",
    "Fragile and conflict affected situations", "Pacific island small states",
    "Latin America & the Caribbean", "Central Europe and the Baltics",
    "Middle East, North Africa, Afghanistan & Pakistan", "Middle East, North Africa, Afghanistan & Pakistan", "South Asia", "Europe & Central Asia",
    "East Asia & Pacific", "Sub-Saharan Africa", "Latin America & Caribbean", "Latin America & the Caribbean",
    'Heavily indebted poor countries', 'Sub-Saharan Africa', "Middle East, North Africa, Afghanistan & Pakistan",
    "Virgin Islands", "Guam", "Channel Islands", 
    "San Marino", "Monaco", "Somalia, Fed. Rep.", "Republic of Congo",
]

def normalize_name(name):
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\[.*?\]', '', name)
    return name.strip()

#Data Cleaning
    #clean_co2(df) takes in the dataframe for the carbon data. 
def clean_co2(df): 
    df = df.rename(columns = {'Unnamed: 1':'Country'})
    df = df[df["Country"] != "Total, all countries or areas"]
    df = df[~df["Country"].isin(["Africa", "Asia", "Northern America", "South America", "Europe", "Oceania", "World"])] # excluding continents 
    df["Country"] = df["Country"].apply(normalize_name)
    df["Country"] = df["Country"].replace(country_mapping)
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

    #clean_co2(df) takes in the dataframe for the carbon data. 
def clean_population(df): 
    df = df.rename(columns = {'Entity':'Country', 'all years': 'Population'})
    df = df[df["Code"].notna()]
    df = df.drop("Code", axis = 1)
    df = df[df["Country"] != "Total, all countries or areas"]
    df = df[~df["Country"].isin(["Africa", "Asia", "Northern America", "Americas", "South America", "Europe", "Oceania", "World"])] # excluding continents 
    df["Country"] = df["Country"].apply(normalize_name)
    df["Country"] = df["Country"].replace(country_mapping)

    df.to_csv('data/processed/population.csv', index=False)
    print(df.head())
    print(f"{GREEN}...Population Data Cleaned!{RESET}")
    return df
    
    #clean_consumption(df) takes in the dataframe for the energy consumption data. 
def clean_consumption(df): 
    # run this once to see what you're dealing with
    df = df[df["Code"].notna()]
    df = df.drop("Code", axis = 1) # unnecessary/redundant not always there.
    df = df.rename(columns = {'Entity':'Country'})
    df = df[~df["Country"].isin(["Africa", "Asia", "Northern America", "South America", "Europe", "Oceania", "World"])] # excluding continents 
    df = df.fillna(0.0)
    df["Country"] = df["Country"].replace(country_mapping)
    df["Country"] = df["Country"].apply(normalize_name)
    df.to_csv('data/processed/energy_consumption_cleaned.csv', index=False)
    print(df.head())
    print(f"{GREEN}...Consumption Data Cleaned!{RESET}")
    return df
def clean_gdp(df): 
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.rename(columns = {'Country Name':'Country', 'all years': 'Population'})
    df = df[df["Country Code"].notna()]
    df = df.drop(["Country Code", "Indicator Name","Indicator Code"], axis = 1) #redundant data
    df = df[df["Country"] != "Total, all countries or areas"]
    df = df[~df["Country"].isin(["Africa", "Asia", "Northern America", "Americas", "South America", "Europe", "Oceania", "World", "East Asia & Pacific"])] # excluding continents 
    df = df[~df["Country"].isin(gdp_aggregates)] # excluding continents 
    df["Country"] = df["Country"].apply(normalize_name)
    df["Country"] = df["Country"].apply(normalize_name)
    df["Country"] = df["Country"].replace(country_mapping)
    df["Country"] = df["Country"].replace(gdp_mapping)

    #melting columns into rows
    year_cols = [col for col in df.columns if col.isdigit()]

    df = df.melt(
            id_vars = ["Country"],
            value_vars=year_cols,
            var_name="Year",
            value_name="gdp_usd")
    
    df["Year"] = df["Year"].astype(int)

    df.to_csv('data/processed/gdp.csv', index=False)
    print(df.head())
    print(f"{GREEN}...Population Data Cleaned!{RESET}")
    return df

def merge_data(c_df, ce_df, p_df, g_df):
    df = pd.merge(c_df, ce_df, on=["Country", "Year"], how="outer")
    df = df.sort_values(["Country", "Year"])
    #filling in missing data with interpolation
    df["co2_total_kt"] = df.groupby("Country")["co2_total_kt"].transform(lambda x: x.interpolate(method="linear"))
    df["co2_per_capita"] = df.groupby("Country")["co2_per_capita"].transform(lambda x: x.interpolate(method="linear"))

    # add these three lines
    print("\nNull counts after merge:")
    print(df.isnull().sum())
    print(f"{MAGENTA}\nShape: {df.shape}{RESET}")

    df = pd.merge(df, p_df, on=["Country", "Year"], how="left")
    df = pd.merge(df, g_df, on=["Country", "Year"], how="left")

    #Drop rows with no energy values for the sake of ML process
    energy_cols = ["Coal", "Oil", "Gas", "Solar", "Wind", "Hydropower"]
    df = df.dropna(subset=energy_cols)
    print(df.shape)

    df.to_csv('data/output/CO2_AND_ENERGY.csv', index = False)
    print(df.head())
    print(f"{GREEN}...Merged Datasets{RESET}")
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
    population_data = pd.read_csv('data/raw/population/population.csv', encoding='latin-1')
    gdp_data = pd.read_csv('data/raw/GDP/gdp.csv', encoding='latin-1', skiprows=4) #Renamed csv file to be more concise (gdp)

    explore_data(carbon_data, consumption_data)

    #call clean_data()
    print("\nCleaning data...")
    print(f"{YELLOW}Energy Consumption{RESET}")
    consumption_data = clean_consumption(consumption_data)
    print(f"{YELLOW}Carbon - CO2 Estimate{RESET}")
    carbon_data = clean_co2(carbon_data)
    print(f"{YELLOW}\nPopulation Data{RESET}")
    population_data = clean_population(population_data)
    gdp_data = clean_gdp(gdp_data)

    #call merge_data()
    print("\nMerging data...")
    merged = merge_data(carbon_data, consumption_data, population_data, gdp_data)
            #checking shape
    print(merged.shape)

    #There is an issue with names not matching up. 
    co2_countries = set(carbon_data["Country"].unique())
    energy_countries = set(consumption_data["Country"].unique())

    print("\nIn CO2 but not energy:")
    print(sorted(co2_countries - energy_countries))

    print("\nIn energy but not CO2:")
    print(sorted(energy_countries - co2_countries))


if __name__ == "__main__":
    main()