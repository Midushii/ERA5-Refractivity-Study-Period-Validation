"""
===========================================================
01_Surface_Refractivity_Analysis.py

Author : Vini
Project: Atmospheric Characterization for Electromagnetic
         Wave Propagation using ERA5 Reanalysis

Purpose
-------
This script computes near-surface radio refractivity (N)
using ERA5 single-level reanalysis data and performs an
initial assessment of long-term atmospheric behaviour over
Mumbai.

The analysis includes

1. Radio refractivity calculation
2. Monthly mean variation
3. Seasonal mean variation
4. Annual mean variation
5. Diurnal variation
6. Summary statistics

Input
-----
ERA5 Single-Level NetCDF file

Variables required

- 2 m temperature
- 2 m dewpoint temperature
- Surface pressure

Output
------
Monthly_Refractivity.png
Seasonal_Refractivity.png
Annual_Refractivity.png
Diurnal_Refractivity.png
Surface_Refractivity_Statistics.csv

===========================================================
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Load ERA5 Dataset
# ---------------------------------------------------------

FILE = "ERA5_Single_Level.nc"

ds = xr.open_dataset(FILE)

print("\nDataset Loaded Successfully\n")
print(ds)

# ---------------------------------------------------------
# Read Variables
# ---------------------------------------------------------

T = ds["t2m"]              # Kelvin
Td = ds["d2m"]             # Kelvin
P = ds["sp"] / 100         # Convert Pa → hPa

# ---------------------------------------------------------
# Water Vapour Pressure
# Tetens Equation
# ---------------------------------------------------------

Tc = T - 273.15
Tdc = Td - 273.15

e = 6.112 * np.exp((17.67 * Tdc) / (Tdc + 243.5))

# ---------------------------------------------------------
# Radio Refractivity
#
# N = 77.6(P/T) + 3.73×10^5 (e/T²)
# ---------------------------------------------------------

N = (77.6 * P / T) + (3.73e5 * e / (T ** 2))

print("\nRadio Refractivity Computed Successfully\n")

# ---------------------------------------------------------
# Convert to DataFrame
# ---------------------------------------------------------

df = N.to_dataframe(name="Refractivity").reset_index()

time_name = "time"

df["Month"] = df[time_name].dt.month
df["Year"] = df[time_name].dt.year
df["Hour"] = df[time_name].dt.hour

# ---------------------------------------------------------
# Seasons
# ---------------------------------------------------------

def season(month):

    if month in [12,1,2]:
        return "DJF"

    elif month in [3,4,5]:
        return "MAM"

    elif month in [6,7,8,9]:
        return "JJAS"

    else:
        return "ON"

df["Season"] = df["Month"].apply(season)

# ---------------------------------------------------------
# Monthly Mean
# ---------------------------------------------------------

monthly = df.groupby("Month")["Refractivity"].mean()

plt.figure(figsize=(8,5))

plt.plot(
    monthly.index,
    monthly.values,
    marker="o",
    linewidth=2
)

plt.xlabel("Month")
plt.ylabel("Mean Refractivity (N-units)")
plt.title("Monthly Mean Surface Refractivity")

plt.grid(True)

plt.tight_layout()

plt.savefig("Monthly_Refractivity.png", dpi=300)

plt.show()

# ---------------------------------------------------------
# Seasonal Mean
# ---------------------------------------------------------

seasonal = (
    df.groupby("Season")["Refractivity"]
      .mean()
      .reindex(["DJF","MAM","JJAS","ON"])
)

plt.figure(figsize=(7,5))

plt.bar(
    seasonal.index,
    seasonal.values
)

plt.xlabel("Season")
plt.ylabel("Mean Refractivity (N-units)")
plt.title("Seasonal Mean Surface Refractivity")

plt.tight_layout()

plt.savefig("Seasonal_Refractivity.png", dpi=300)

plt.show()

# ---------------------------------------------------------
# Annual Mean
# ---------------------------------------------------------

annual = df.groupby("Year")["Refractivity"].mean()

plt.figure(figsize=(10,5))

plt.plot(
    annual.index,
    annual.values,
    marker="o"
)

plt.xlabel("Year")
plt.ylabel("Mean Refractivity (N-units)")
plt.title("Annual Mean Surface Refractivity")

plt.grid(True)

plt.tight_layout()

plt.savefig("Annual_Refractivity.png", dpi=300)

plt.show()

# ---------------------------------------------------------
# Diurnal Variation
# ---------------------------------------------------------

hourly = df.groupby("Hour")["Refractivity"].mean()

plt.figure(figsize=(7,5))

plt.plot(
    hourly.index,
    hourly.values,
    marker="o"
)

plt.xlabel("Hour (UTC)")
plt.ylabel("Mean Refractivity (N-units)")
plt.title("Mean Diurnal Variation")

plt.grid(True)

plt.tight_layout()

plt.savefig("Diurnal_Refractivity.png", dpi=300)

plt.show()

# ---------------------------------------------------------
# Summary Statistics
# ---------------------------------------------------------

statistics = pd.DataFrame({

    "Mean":[df["Refractivity"].mean()],
    "Standard Deviation":[df["Refractivity"].std()],
    "Minimum":[df["Refractivity"].min()],
    "Maximum":[df["Refractivity"].max()]

})

statistics.to_csv(
    "Surface_Refractivity_Statistics.csv",
    index=False
)

print("\nSummary Statistics\n")
print(statistics)

print("\nAnalysis Completed Successfully.\n")