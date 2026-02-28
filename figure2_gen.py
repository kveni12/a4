import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------
# Load abortion data
# -----------------------
df = pd.read_excel("abortion_data_guttmacher.xlsx")

df = df[[
    "U.S. State",
    "% of residents obtaining abortions who traveled out of state for care, 2020",
    "% of counties without a known clinic, 2020",
    "% change in the no. of abortion clinics, 2017-2020"
]].dropna()

# -----------------------
# Load US states shapefile (5m resolution)
# -----------------------
states = gpd.read_file("cb_2018_us_state_5m.shp")

# Remove territories
states = states[~states["STUSPS"].isin(["PR", "VI", "GU", "MP", "AS"])]

# Merge shapefile with abortion data
gdf = states.merge(
    df,
    left_on="NAME",
    right_on="U.S. State",
    how="left"
)

# -----------------------
# Create multi-panel figure
# -----------------------
fig = plt.figure(figsize=(14, 6))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.9])

# -----------------------
# Panel A: Travel choropleth
# -----------------------
ax1 = fig.add_subplot(gs[0, 0])
gdf.plot(
    column="% of residents obtaining abortions who traveled out of state for care, 2020",
    ax=ax1,
    legend=True,
    cmap="OrRd",
    edgecolor="white",
    linewidth=0.4
)
ax1.set_title("Out-of-State Travel for Abortion Care (2020)")
ax1.axis("off")

# -----------------------
# Panel B: Clinic access choropleth
# -----------------------
ax2 = fig.add_subplot(gs[0, 1])
gdf.plot(
    column="% of counties without a known clinic, 2020",
    ax=ax2,
    legend=True,
    cmap="OrRd",
    edgecolor="white",
    linewidth=0.4
)
ax2.set_title("Counties Without an Abortion Clinic (2020)")
ax2.axis("off")

# -----------------------
# Panel C: Scatterplot
# -----------------------
ax3 = fig.add_subplot(gs[0, 2])

x = df["% change in the no. of abortion clinics, 2017-2020"]
y = df["% of residents obtaining abortions who traveled out of state for care, 2020"]

ax3.scatter(x, y, alpha=0.8)
ax3.set_xlabel("% change in abortion clinics (2017–2020)")
ax3.set_ylabel("% traveling out of state (2020)")
ax3.set_title("Clinic Change vs. Travel")

# Subtle regression line (contextual, not dominant)
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 100)
ax3.plot(x_line, slope * x_line + intercept, linestyle="--", color="gray")

# -----------------------
# Overall title and save
# -----------------------
fig.suptitle(
    "Clinic Reductions Coincide with Increased Travel and Limited Local Access",
    fontsize=14,
    y=1.03
)

plt.tight_layout()
plt.savefig("figure2.png", dpi=300, bbox_inches="tight")
plt.close()