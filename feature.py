import pandas as pd
import numpy as np

#colors
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

def engineer_features(df):
    renewable_cols = ['Solar', 'Wind', 'Hydropower', 'Biofuels', 'Other renewables']
    fossil_cols = ['Coal', 'Oil', 'Gas']

    # basic energy aggregates
    df['total_energy'] = df[renewable_cols + fossil_cols].sum(axis=1)
    df['total_renewable'] = df[renewable_cols].sum(axis=1)
    df['total_fossil'] = df[fossil_cols].sum(axis=1)

    # shares — these are your most important ML features
    df['renewable_share'] = df['total_renewable'] / df['total_energy']
    df['fossil_share'] = df['total_fossil'] / df['total_energy']

    # emissions intensity — how dirty is each unit of energy?
    df['co2_per_energy'] = df['co2_total_kt'] / df['total_energy']

    # per capita features — need population
    df['energy_per_capita'] = df['total_energy'] / df['Population']

    # economic features — need GDP
    df['gdp_per_capita'] = df['gdp_usd'] / df['Population']
    df['co2_per_gdp'] = df['co2_total_kt'] / df['gdp_usd']  # emissions intensity per dollar

    # year over year change — tells model about trends not just snapshots
    df = df.sort_values(['Country', 'Year'])
    df['co2_yoy_change'] = df.groupby('Country')['co2_total_kt'].pct_change()
    df['renewable_share_yoy'] = df.groupby('Country')['renewable_share'].diff()

    print(f"{CYAN}Engineered features:{RESET}")
    print(df[['Country', 'Year', 'renewable_share', 'fossil_share', 
              'co2_per_energy', 'gdp_per_capita', 'co2_yoy_change']].head(10))
    print(f"{MAGENTA}Shape: {df.shape}{RESET}")
    print(f"{GREEN}...Features engineered!{RESET}")
    return df

def main():
    df = pd.read_csv('data/output/CO2_AND_ENERGY.csv')
    print(f"Loaded model dataset: {df.shape}")
    
    df = engineer_features(df)
    
    # check nulls after feature engineering
    print("\nNull counts:")
    print(df.isnull().sum())
    
    df.to_csv('data/processed/features.csv', index=False)

if __name__ == "__main__":
    main()