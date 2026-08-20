import xarray as xr
import pandas as pd
import numpy as np

ds = xr.open_dataset("processed_pressure.nc")

N = ds["N"]
h = ds["h"]

years = np.unique(N.time.dt.year)

print("\nYears found:")
print(years)

stats = []

for yr in years:

    data = N.where(
        N.time.dt.year == yr,
        drop=True
    )

    values = data.values.flatten()
    values = values[~np.isnan(values)]

    mean = np.mean(values)
    std = np.std(values)
    minimum = np.min(values)
    maximum = np.max(values)

    cv = (std / mean) * 100

    stats.append([
        int(yr),
        mean,
        std,
        minimum,
        maximum,
        cv
    ])

year_df = pd.DataFrame(
    stats,
    columns=[
        "Year",
        "Mean_N",
        "Std_N",
        "Min_N",
        "Max_N",
        "CV_percent"
    ]
)

print("\n======================")
print("YEARLY STATISTICS")
print("======================")
print(year_df)

year_df.to_csv(
    "Yearly_Statistics.csv",
    index=False
)

results = []

for yr in years:

    Ny = N.where(
        N.time.dt.year == yr,
        drop=True
    )

    hy = h.where(
        h.time.dt.year == yr,
        drop=True
    )

    total = len(Ny.time)

    sub = 0
    superr = 0
    duct = 0

    for i in range(total):

        Nt = Ny.isel(time=i)
        ht = hy.isel(time=i)

        N1000 = float(
            Nt.sel(isobaricInhPa=1000)
        )

        N925 = float(
            Nt.sel(isobaricInhPa=925)
        )

        h1000 = float(
            ht.sel(isobaricInhPa=1000)
        )

        h925 = float(
            ht.sel(isobaricInhPa=925)
        )

        gradient = (
            (N925 - N1000)
            /
            (h925 - h1000)
        ) * 1000

        if gradient > -40:
            sub += 1

        elif gradient > -157:
            superr += 1

        else:
            duct += 1

    results.append([
        int(yr),
        sub * 100 / total,
        superr * 100 / total,
        duct * 100 / total
    ])

regime_df = pd.DataFrame(
    results,
    columns=[
        "Year",
        "Sub_refraction",
        "Super_refraction",
        "Ducting"
    ]
)

print("\n======================")
print("PROPAGATION REGIME")
print("======================")
print(regime_df)

regime_df.to_csv(
    "Propagation_Regime.csv",
    index=False
)

grad_results = []

for yr in years:

    Ny = N.where(
        N.time.dt.year == yr,
        drop=True
    )

    hy = h.where(
        h.time.dt.year == yr,
        drop=True
    )

    dNdh = (
        (
            Ny.sel(isobaricInhPa=925)
            -
            Ny.sel(isobaricInhPa=1000)
        )
        /
        (
            hy.sel(isobaricInhPa=925)
            -
            hy.sel(isobaricInhPa=1000)
        )
    ) * 1000

    grad_results.append([
        int(yr),
        float(dNdh.mean()),
        float(dNdh.std())
    ])

gradient_df = pd.DataFrame(
    grad_results,
    columns=[
        "Year",
        "Mean_dNdh",
        "Std_dNdh"
    ]
)

print("\n======================")
print("GRADIENT STATISTICS")
print("======================")
print(gradient_df)

gradient_df.to_csv(
    "Gradient_Statistics.csv",
    index=False
)
profiles = []

for yr in years:

    data = N.where(
        N.time.dt.year == yr,
        drop=True
    )

    profile = (
        data
        .mean(dim="time")
        .values
        .flatten()
    )

    profiles.append(profile)

corr = np.corrcoef(profiles)

similarity_df = pd.DataFrame(
    corr,
    index=years,
    columns=years
)

print("\n======================")
print("SIMILARITY MATRIX")
print("======================")
print(similarity_df)

similarity_df.to_csv(
    "Similarity_Matrix.csv"
)


meanN = (
    N.mean(dim="isobaricInhPa")
    .groupby("time.year")
    .mean()
)

x = meanN.year.values
y = meanN.values

slope, intercept = np.polyfit(
    x,
    y,
    1
)

y_pred = slope * x + intercept

r2 = (
    1
    -
    np.sum((y - y_pred) ** 2)
    /
    np.sum((y - np.mean(y)) ** 2)
)

print("\n======================")
print("TREND ANALYSIS")
print("======================")
print("Slope =", slope, "N/year")
print("R² =", r2)

ci_results = []

for yr in years:

    data = N.where(
        N.time.dt.year == yr,
        drop=True
    )

    values = data.values.flatten()
    values = values[~np.isnan(values)]

    n = len(values)

    mean = np.mean(values)
    std = np.std(values)

    ci = (
        1.96
        *
        std
        /
        np.sqrt(n)
    )

    lower = mean - ci
    upper = mean + ci

    ci_results.append([
        int(yr),
        mean,
        lower,
        upper
    ])

ci_df = pd.DataFrame(
    ci_results,
    columns=[
        "Year",
        "Mean_N",
        "CI_Lower",
        "CI_Upper"
    ]
)

print("\n======================")
print("95% CONFIDENCE INTERVALS")
print("======================")
print(ci_df)

ci_df.to_csv(
    "Confidence_Intervals.csv",
    index=False
)

months = N.time.dt.month

season = xr.full_like(
    months,
    "",
    dtype=object
)

season = xr.where(
    months.isin([12, 1, 2]),
    "DJF",
    season
)

season = xr.where(
    months.isin([3, 4, 5]),
    "MAM",
    season
)

season = xr.where(
    months.isin([6, 7, 8, 9]),
    "JJAS",
    season
)

season = xr.where(
    months.isin([10, 11]),
    "ON",
    season
)


print("SEASONS PRESENT")
print(np.unique(season.values))
print("ALL ANALYSES COMPLETED")


print("Files saved:")
print("Yearly_Statistics.csv")
print("Propagation_Regime.csv")
print("Gradient_Statistics.csv")
print("Similarity_Matrix.csv")
print("Confidence_Intervals.csv")
