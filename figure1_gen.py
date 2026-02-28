import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_excel("abortion_data_guttmacher.xlsx")

# Define columns (exact names from your dataset)
x_col = "% change in the no. of abortion clinics, 2017-2020"
y_col = "% change in abortion rate, 2017-2020"

# Keep only rows with valid data
plot_df = df[[x_col, y_col, "U.S. State"]].dropna()

# Extract values
x = plot_df[x_col].values
y = plot_df[y_col].values

# Create scatter plot
plt.figure(figsize=(7, 5))
plt.scatter(x, y)

# Fit and plot regression line
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(min(x), max(x), 100)
y_line = slope * x_line + intercept
plt.plot(x_line, y_line)

# Labels and title (intentionally persuasive framing)
plt.xlabel("% change in number of abortion clinics (2017–2020)")
plt.ylabel("% change in abortion rate (2017–2020)")
plt.title("States That Lost Abortion Clinics Saw Larger Declines in Abortion Rates")

# Save figure
plt.savefig("figure1.png", bbox_inches="tight", dpi=300)
plt.close()