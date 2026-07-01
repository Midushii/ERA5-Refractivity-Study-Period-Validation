import xarray as xr
import pandas as pd
import numpy as np

# =========================
# LOAD DATA
# =========================

ds = xr.open_dataset(
    "era5-pressure.grib",
    engine="cfgrib"
)

print("Dataset loaded.")

# =========================
# SPATIAL MEAN
# =========================

t = ds["t"].mean(
    dim=["latitude", "longitude"]
)

q = ds["q"].mean(
    dim=["latitude", "longitude"]
)

z = ds["z"].mean(
    dim=["latitude", "longitude"]
)

# =========================
# HEIGHT (m)
# =========================

h = z / 9.80665

# =========================
# PRESSURE LEVELS
# =========================

P = ds["isobaricInhPa"]

P3 = xr.DataArray(
    P.values,
    dims=["isobaricInhPa"],
    coords={
        "isobaricInhPa": P
    }
)

# =========================
# VAPOUR PRESSURE
# =========================

e = (
    q * P3
) / (
    0.622 + 0.378 * q
)

# =========================
# REFRACTIVITY
# =========================

N = (
    77.6 * P3 / t
    +
    3.73e5 * e / (t**2)
)

print("N calculated.")

# =========================
# SAVE TO NETCDF
# =========================

xr.Dataset({

    "N": N,
    "h": h,
    "t": t,
    "q": q

}).to_netcdf(
    "processed_pressure.nc"
)

print("Saved:")
print("processed_pressure.nc")