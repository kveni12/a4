import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# =====================================================
# 1. Load abortion data
# =====================================================
df = pd.read_excel("abortion_data_guttmacher.xlsx")

df = df[[
    "U.S. State",
    "% of residents obtaining abortions who traveled out of state for care, 2020",
    "% of counties without a known abortion provider, 2014",
    "% change in the no. of abortion providers, 2014-2017",
    "No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020",
    "No. of abortions per 1,000 women aged 15–44, by state of residence, 2020"
]].dropna()

# =====================================================
# 2. Load US states shapefile
# =====================================================
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

# Contiguous U.S. only
conus = gdf[~gdf["NAME"].isin(["Alaska", "Hawaii"])]

# =====================================================
# 3. Prepare dot plot data (sorted)
# =====================================================
dot_df = df.sort_values(
    "No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020",
    ascending=True
)

n_states = len(dot_df)

# Spacing between states
spacing = 1.0
y_pos = np.arange(n_states) * spacing

# =====================================================
# 4. Dynamic figure height (KEY FIX)
# =====================================================
dot_plot_height = n_states *0.1   # adjust 0.20–0.25 if needed
map_row_height = 6                # controls choropleth size

total_height = map_row_height + dot_plot_height * 2 + 2

fig = plt.figure(figsize=(15, total_height))

gs = fig.add_gridspec(
    nrows=3,
    ncols=2,
    height_ratios=[map_row_height, dot_plot_height, dot_plot_height],
    width_ratios=[1.3, 1.3]   # slightly wider maps
)

# =====================================================
# Panel 1 — Out-of-state travel (map)
# =====================================================
ax1 = fig.add_subplot(gs[0, 0])
conus.plot(
    column="% of residents obtaining abortions who traveled out of state for care, 2020",
    ax=ax1,
    legend=True,
    cmap="OrRd",
    edgecolor="white",
    linewidth=0.5
)
ax1.set_title("Out-of-State Travel for Abortion Care (2020)")
ax1.set_aspect("equal")
ax1.axis("off")

# =====================================================
# Panel 2 — Provider access (map)
# =====================================================
ax2 = fig.add_subplot(gs[0, 1])
conus.plot(
    column="% of counties without a known abortion provider, 2014",
    ax=ax2,
    legend=True,
    cmap="Blues",
    edgecolor="white",
    linewidth=0.5
)
ax2.set_title("Counties Without an Abortion Provider (2014)")
ax2.set_aspect("equal")
ax2.axis("off")

# =====================================================
# Panel 3 — Rate by state of OCCURRENCE
# =====================================================
ax3 = fig.add_subplot(gs[1, 0])

ax3.scatter(
    dot_df["No. of abortions per 1,000 women aged 15–44, by state of occurrence, 2020"],
    y_pos,
    color="darkgreen",
    alpha=0.75
)

ax3.set_yticks(y_pos)
ax3.set_yticklabels(dot_df["U.S. State"], fontsize=7)
ax3.set_ylim(-spacing, y_pos.max() + spacing)

ax3.set_xlabel("Abortions per 1,000 women (state of occurrence)")
ax3.set_title("Abortion Rate by State of Occurrence (2020)")

ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

# =====================================================
# Panel 5 — Rate by state of RESIDENCE
# =====================================================
ax5 = fig.add_subplot(gs[1, 1], sharex=ax3)

ax5.scatter(
    dot_df["No. of abortions per 1,000 women aged 15–44, by state of residence, 2020"],
    y_pos,
    color="gray",
    alpha=0.75
)

ax5.set_yticks(y_pos)
ax5.set_yticklabels(dot_df["U.S. State"], fontsize=7)
ax5.set_ylim(-spacing, y_pos.max() + spacing)

ax5.set_xlabel("Abortions per 1,000 women (state of residence)")
ax5.set_title("Abortion Rate by State of Residence (2020)")

ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)

# =====================================================
# Panel 4 — Scatterplot (middle-right)
# =====================================================
ax4 = fig.add_subplot(gs[2, 0])

x = df["% change in the no. of abortion providers, 2014-2017"]
y = df["% of residents obtaining abortions who traveled out of state for care, 2020"]

ax4.scatter(x, y, alpha=0.8)

ax4.set_xlabel("% change in abortion providers (2014–2017)")
ax4.set_ylabel("% traveling out of state (2020)")
ax4.set_title("Provider Change vs. Out-of-State Travel")

# Trend line
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 100)
ax4.plot(x_line, slope * x_line + intercept, linestyle="--", color="gray")

# =====================================================
# Bottom-right empty panel
# =====================================================
ax_empty = fig.add_subplot(gs[2, 1])
ax_empty.axis("off")

# =====================================================
# Overall title
# =====================================================
fig.suptitle(
    "Access, Displacement, and Measurement:\nHow Abortion Care Concentration Depends on What We Count",
    fontsize=15,
    y=0.995
)

plt.tight_layout()
plt.savefig("figure2.png", dpi=300, bbox_inches="tight")
plt.close()