import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#colors
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"


def co2_trends_country(df, name):
    c_df = df[df["Country"] == name]

    #create a visualization of co2 per capita over the years.
    sns.lineplot(data = c_df, x="Year", y="co2_per_capita")
    plt.xlabel("Year")
    plt.ylabel("Carbon Emissions per Capita (Metric Tons)")

    title = name +  "'s Carbon Emissions per Capita by Year"
    plt.title(title)
    
    file_path = "figures/co2_trends_" + name
    plt.savefig(file_path, dpi = 100)
    plt.close() 
    #plt.show()

    print(c_df.head())
    return c_df

def co2_trends_year(df, year):
    c_df = df[df["Year"] == year]
    c_df = c_df.sort_values("co2_per_capita", ascending = False, )
    c_df = c_df.iloc[0:5]

    #create a visualization of co2 per capita over the years.
    sns.barplot(data = c_df, x="Country", y="co2_per_capita", hue="Country")
    plt.xlabel("Country")
    plt.xticks(rotation=-5)
    plt.ylabel("Carbon Emissions per Capita (Metric Tons)")

    title = "Carbon Emissions per Capita for the Year " + str(year)
    plt.title(title)
    
    file_path = "figures/co2_country_" + str(year)
    plt.savefig(file_path, dpi = 100)
    plt.close() 
    #plt.show()

    print(c_df.head())
    return c_df



def main():
    print(f"{BLUE}Exploring cleaned data...🌎{RESET}")
    df = pd.read_csv("data/output/CO2_AND_ENERGY.csv")
    df_real = df[df["co2_total_kt"].notna()]
    df_real = df[df["Year"] <= 2022] # no real data so better to drop interpolated rows for now.

    print(df.sample(10))
    print(f"\n{CYAN}Carbon trends specifically for India{RESET}")
    afghan = co2_trends_country(df, "India")
    print(afghan.shape)

    co2_trends_year(df, 1975)

if __name__ == "__main__":
    main()
