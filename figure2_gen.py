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
# Load US states shapefile
# -----------------------
states = gpd.read_file("cb_2018_us_state_5m.shp")

states = states[~states["NAME"].isin([
    "Puerto Rico",
    "Virgin Islands",
    "Guam",
    "Commonwealth of the Northern Mariana Islands",
    "American Samoa"
])]

gdf = states.merge(
    df,
    left_on="NAME",
    right_on="U.S. State",
    how="left"
)

# -----------------------
# Create figure layout (MAPS BIG)
# -----------------------
fig = plt.figure(figsize=(10, 12))
gs = fig.add_gridspec(
    nrows=3,
    ncols=2,
    height_ratios=[1.2, 1.2, 0.8],
    width_ratios=[1, 1]
)

# -----------------------
# Panel A: Travel choropleth (full width)
# -----------------------
ax1 = fig.add_subplot(gs[0, :])
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
# Panel B: Clinic access choropleth (full width)
# -----------------------
ax2 = fig.add_subplot(gs[1, :])
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
# Panel C: Scatterplot (bottom-left)
# -----------------------
ax3 = fig.add_subplot(gs[2, 0])

x = df["% change in the no. of abortion clinics, 2017-2020"]
y = df["% of residents obtaining abortions who traveled out of state for care, 2020"]

ax3.scatter(x, y, alpha=0.8)
ax3.set_xlabel("% change in abortion clinics (2017–2020)")
ax3.set_ylabel("% traveling out of state (2020)")
ax3.set_title("Clinic Change vs. Travel")

# Subtle regression line
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 100)
ax3.plot(x_line, slope * x_line + intercept, linestyle="--", color="gray")

# -----------------------
# Bottom-right: empty space for visual breathing room
# -----------------------
ax4 = fig.add_subplot(gs[2, 1])
ax4.axis("off")

# -----------------------
# Overall title
# -----------------------
fig.suptitle(
    "Clinic Reductions Coincide with Increased Travel and Limited Local Access",
    fontsize=14,
    y=0.98
)

plt.tight_layout()
plt.savefig("figure2.png", dpi=300, bbox_inches="tight")
plt.close()