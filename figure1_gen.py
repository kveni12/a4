import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_excel("abortion_data_guttmacher.xlsx")

# Column names
state_col = "U.S. State"
x_col = "% change in the no. of abortion clinics, 2017-2020"
y_col = "% change in abortion rate, 2017-2020"

# Drop missing values
plot_df = df[[state_col, x_col, y_col]].dropna()

x = plot_df[x_col].values
y = plot_df[y_col].values

# Create figure
plt.figure(figsize=(8, 6))

# Scatter plot
plt.scatter(x, y, alpha=0.8, label="U.S. states")

# Regression line
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(min(x), max(x), 100)
y_line = slope * x_line + intercept
plt.plot(
    x_line,
    y_line,
    linestyle="--",
    linewidth=2,
    color="red",
    label="Linear trend"
)

# ---- Define BIVARIATE outliers ----
# Top/bottom 10% thresholds for BOTH axes
x_low, x_high = np.percentile(x, [10, 90])
y_low, y_high = np.percentile(y, [10, 90])

for _, row in plot_df.iterrows():
    is_x_outlier = row[x_col] <= x_low or row[x_col] >= x_high
    is_y_outlier = row[y_col] <= y_low or row[y_col] >= y_high

    if is_x_outlier and is_y_outlier:
        plt.text(
            row[x_col],
            row[y_col],
            row[state_col],
            fontsize=9,
            ha="right",
            va="bottom"
        )

# Labels and title
plt.xlabel("% change in number of abortion clinics (2017–2020)")
plt.ylabel("% change in abortion rate (2017–2020)")
plt.title("States That Lost Abortion Clinics Saw Larger Declines in Abortion Rates")

# Boxed legend
plt.legend(frameon=True, edgecolor="black")

# Save figure
plt.savefig("figure1.png", dpi=300, bbox_inches="tight")
plt.close()