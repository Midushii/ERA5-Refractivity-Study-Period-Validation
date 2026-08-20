import xarray as xr
import pandas as pd
import numpy as np

ds = xr.open_dataset(
    "era5-pressure.grib",
    engine="cfgrib"
)

print("Dataset loaded.")

t = ds["t"].mean(
    dim=["latitude", "longitude"]
)

q = ds["q"].mean(
    dim=["latitude", "longitude"]
)

z = ds["z"].mean(
    dim=["latitude", "longitude"]
)


h = z / 9.80665

P = ds["isobaricInhPa"]

P3 = xr.DataArray(
    P.values,
    dims=["isobaricInhPa"],
    coords={
        "isobaricInhPa": P
    }
)

e = (
    q * P3
) / (
    0.622 + 0.378 * q
)


N = (
    77.6 * P3 / t
    +
    3.73e5 * e / (t**2)
)

print("N calculated.")

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
