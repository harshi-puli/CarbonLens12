import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#colors
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

#color pallette: 
# Warm earth tones
"#bc6c25"  # burnt orange
"#dda15e"  # sand
"#606c38"  # olive green

# Ocean blues
"#0077b6"  # deep ocean
"#90e0ef"  # light cyan

def co2_trends_country(df, c):
    c_df = df[df["Country"].isin(c)]

    #create a visualization of co2 per capita over the years.
    sns.lineplot(data = c_df, x="Year", y="co2_per_capita", hue = "Country")
    plt.xlabel("Year")
    plt.ylabel("Carbon Emissions per Capita (Metric Tons)")

    title_countries = ", ".join(c)
    if len(title_countries) > 30:
        title_countries = title_countries[:30] + "..."

    plt.title("Carbon Emissions per Capita by Year: " + title_countries)
    plt.suptitle("Correlations across energy, emissions, and population variables", 
                 fontsize=9, color="gray", y=0.98)
    
    file_path = "figures/co2_trends_" + c[0]
    plt.savefig(file_path, dpi = 100)
    plt.close()

    print(c_df.head())
    return c_df

def co2_trends_year(df, year):
    c_df = df[df["Year"] == year]
    c_df = c_df.sort_values("co2_per_capita", ascending = False, )
    c_df = c_df.iloc[0:5]

    #create a visualization of co2 per capita over the years.
    sns.barplot(data = c_df, x="Country", y="co2_per_capita", color="#2d6a4f")
    plt.xlabel("Country")
    plt.xticks(rotation=-5)
    plt.ylabel("Carbon Emissions per Capita (Metric Tons)")

    title = "Carbon Emissions per Capita for the Year " + str(year)
    plt.title(title, fontsize=14, pad=15)
    plt.suptitle("Correlations across energy, emissions, and population variables", 
                 fontsize=9, color="gray", y=0.98)
    
    file_path = "figures/co2_country_" + str(year)
    plt.savefig(file_path, dpi = 100)
    plt.close() 
    #plt.show()

    return c_df

def choropleth_co2(df):
    # filter out rows with no CO2 data
    df = df[df["co2_per_capita"].notna()]
    df = df[df["Year"] <= 2022]

    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="co2_per_capita",
        animation_frame="Year",
        color_continuous_scale=[
            "#606c38",   # low emissions — olive green
            "#dda15e",   # mid — sand
            "#bc6c25",   # high — burnt orange
        ],
        range_color=[0, 25],  # cap scale so small countries don't get washed out
        title="CO2 Emissions per Capita by Country over Time",
        labels={"co2_per_capita": "CO2 per Capita (metric tons)"}
    )

    fig.update_layout(
        sliders=[{
            "font": {"color": "white"},
            "currentvalue": {"font": {"color": "white"}}
        }],
        updatemenus=[{
            "font": {"color": "white"},
            "bgcolor": "#1a1a2e"
        }],
        paper_bgcolor="black",        # outer background
        plot_bgcolor="black",         # plot background
        title_font_color="white",
        title_font_size=16,
        geo=dict(
            showframe=False, 
            showcoastlines=True,
            projection_type="orthographic" ,  # ← fixes the squishing
            showland=True,
            landcolor="lightgray",            # ← colors countries with no data
            showocean=True,
            oceancolor="#0d1b2a",             # ← light blue ocean
            showcountries=True,
            countrycolor="white",              # ← white borders between countries
            bgcolor="black",
        ),
        coloraxis_colorbar=dict(
        title="Metric Tons",
        title_font_color="white",
        tickfont_color="white"
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    np.random.seed(42)
    stars = go.Scattergeo(
        lon=np.random.uniform(-180, 180, 200),
        lat=np.random.uniform(-90, 90, 200),
        mode="markers",
        marker=dict(size=1, color="white", opacity=0.6),
        showlegend=False,
        hoverinfo="skip"
    )
    fig.add_trace(stars)

    # save as interactive HTML — much better than PNG for a dashboard
    fig.write_html("figures/choropleth_globe.html")

    fig.update_layout(geo=dict(projection_type="natural earth"))
    fig.write_html("figures/choropleth_flat.html")

    print(f"{GREEN}...Choropleth saved!{RESET}")

    fig.show()

def co2_joint_comparison(df, feature, target="co2_total_kt", log=False, reg=True):
    clean_df = df[[feature, target]].dropna()
    
    kind = "reg" if reg else "scatter"
    
    g = sns.jointplot(
        data=clean_df, x=feature, y=target,
        kind=kind, height=7,
        joint_kws={"scatter_kws": {"alpha": 0.4, "color": "#52b788"},
                   "line_kws": {"color": "#1b4332", "linewidth": 2}} if reg else
                  {"alpha": 0.4, "color": "#2d6a4f"},
        marginal_kws={"color": "#606c38", "bins": 30}
    )
    
    if log:
        g.ax_joint.set_xscale("log")
        g.ax_joint.set_yscale("log")
    
    g.set_axis_labels(feature, target)
    g.figure.suptitle(f"CO2 Emissions vs {feature}", fontsize=14, fontweight="bold", y=1.02)
    plt.savefig(f"figures/joint_{feature}_vs_{target}.png", dpi=100, bbox_inches="tight")
    plt.close()

def co2_kde_comparison(df, c):
    c_df = df[df["Country"].isin(c)]
    c_df = c_df.dropna(subset=["co2_per_capita"])

    #create a visualization of co2 per capita over the years.
    sns.kdeplot(data=c_df, x="co2_per_capita", hue="Country", fill = True)
    plt.xlabel("Carbon Emissions per Capita (Metric Tons)") 
    plt.ylabel("Density")

    title_countries = ", ".join(c)
    if len(title_countries) > 30:
        title_countries = title_countries[:30] + "..."

    title = "Carbon Emissions per Capita: " + title_countries
    plt.title(title, fontsize=14)
    plt.suptitle("Correlations across energy, emissions, and population variables", 
                 fontsize=9, color="gray", y=0.98)
    
    file_path = "figures/co2_compare_dist_" + c[0]

    plt.savefig(file_path, dpi = 100)
    plt.close() 
    #plt.show()
    return c_df

def correlation_heatmap(df):
    cols = [
        "co2_total_kt",
        "co2_per_capita", 
        "Coal", "Oil", "Gas",        # fossil fuels
        "Solar", "Wind", "Hydropower", # renewables
        "Population"                   # from your population merge
    ]

    corr_df = df[cols].dropna()
    corr = corr_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr, 
        annot=True,
        fmt=".2f",
        cmap="BrBG",
        vmin=-1, vmax=1
    )

    plt.title("Feature Correlation Heatmap", fontsize=14, fontweight="bold", pad=15)
    plt.xticks(fontsize=9, rotation=45, ha="right")
    plt.yticks(fontsize=9, rotation=0)
    plt.suptitle("Correlations across energy, emissions, and population variables", 
                 fontsize=9, color="gray", y=0.98)
    plt.tight_layout() 
    plt.savefig("figures/correlation_heatmap.png", dpi=100)
    plt.close()

def main():
    print(f"{BLUE}Exploring cleaned data...🌎{RESET}")
    df = pd.read_csv("data/output/CO2_AND_ENERGY.csv")
    df_real = df[df["co2_total_kt"].notna()]
    df_real = df[df["Year"] <= 2022] # no real data so better to drop interpolated rows for now.

    print(df_real.sample(10))
    print(f"\n{CYAN}Carbon trends specifically for India{RESET}")
    c = co2_trends_country(df_real, ["India"])
    print(c.shape)

    countries_compare = ["Russia", "China", "India", "United States", "Nicaragua"]
    co2_trends_year(df_real, 1975)
    co2_kde_comparison(df_real, countries_compare)
    co2_trends_country(df_real, ["Russia", "China", "India", "United States", "Nicaragua"])
    correlation_heatmap(df_real)

    #joints
    co2_joint_comparison(df, "Coal", target="co2_total_kt", log=False, reg=True)
    co2_joint_comparison(df, "Solar", target="co2_total_kt", log=True, reg=False)
    co2_joint_comparison(df, "Gas", target="co2_total_kt", log=True, reg=False)

    #choropleth
    choropleth_co2(df)
if __name__ == "__main__":
    main()
