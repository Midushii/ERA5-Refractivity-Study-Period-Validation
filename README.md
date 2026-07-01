# Study Period Validation for Electromagnetic Wave Propagation using ERA5 Reanalysis

## Overview

This repository contains the computational analysis carried out to identify a statistically representative study period for electromagnetic wave propagation modelling over Mumbai, India.

The work utilizes ERA5 reanalysis data to characterize the atmospheric refractive environment through the computation of radio refractivity, vertical refractivity gradients and propagation regimes. A sequence of statistical analyses was performed to evaluate the temporal stability of atmospheric conditions before proceeding towards electromagnetic wave prediction.

The validated study period obtained from this analysis forms the basis for the subsequent development of an EM wave propagation prediction framework.

---

## Study Area

**Location:** Mumbai, India

**Domain**

- Latitude : 18.75°N – 19.25°N
- Longitude : 72.50°E – 73.00°E

---

## Datasets

**ERA5 Hourly Reanalysis (ECMWF)**

**Single-Level Variables**

- 2 m Temperature
- 2 m Dewpoint Temperature
- Surface Pressure
- Sea Surface Temperature
- Boundary Layer Height

**Pressure-Level Variables**

- Temperature
- Specific Humidity
- Geopotential

Pressure Levels

- 1000 hPa
- 925 hPa
- 850 hPa

---

## Methodology

The workflow implemented in this repository includes:

- Computation of atmospheric radio refractivity
- Computation of geopotential height
- Estimation of vertical refractivity gradients
- Classification of electromagnetic propagation regimes
- Monthly and seasonal refractivity analysis
- Interannual statistical analysis
- Similarity analysis between atmospheric states
- Linear trend analysis
- Confidence interval analysis
- Validation of the representative study period

---

## Repository Structure

```
Study_Period_Validation/

├── 01_Data/
├── 02_Python_Codes/
├── 03_Tables/
├── 04_Figures/
├── 05_Report/
└── 06_Presentation/
```

---

## Current Status

✓ ERA5 datasets processed

✓ Atmospheric refractivity computed

✓ Statistical validation of the study period completed

✓ Representative study period identified

⏳ Electromagnetic wave propagation prediction in progress

---

## Software

Python 3.13

Major Libraries

- NumPy
- Pandas
- Xarray
- SciPy
- Matplotlib

---

## Author

Midushi Maheshwari 


2026