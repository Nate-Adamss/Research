#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from typing import Optional, Union

def compute_pm_parallax(
    data: Union[str, pd.DataFrame],
    output_csv: Optional[str] = None,
    keep_nulls: bool = False,
    required_cols: Optional[list] = None,
    float_format: Optional[str] = "%.8g"
) -> pd.DataFrame:
    """
    Compute pm_total and pm_total_error from a CSV filename or DataFrame.

    Parameters
    ----------
    data : str or pandas.DataFrame
        Path to input CSV file OR a pandas DataFrame containing the columns:
        ra, dec, pmra, pmra_error, pmdec, pmdec_error, parallax, parallax_error
    output_csv : str or None
        If provided, write the resulting DataFrame to this CSV path.
    keep_nulls : bool
        If False (default) drop rows missing required numeric inputs.
        If True, keep rows and produce NaNs for computed fields when inputs are missing.
    required_cols : list or None
        Optional custom list of required columns. If None, the default required set is used.
    float_format : str or None
        Format string passed to DataFrame.to_csv to control numeric formatting.
        Set to None to disable formatting.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns: ra, dec, pm_total, pm_total_error, parallax, parallax_error
    """
    # default required columns
    if required_cols is None:
        required_cols = [
            "ra", "dec",
            "pmra", "pmra_error",
            "pmdec", "pmdec_error",
            "parallax", "parallax_error"
        ]

    # load DataFrame if a path is provided
    if isinstance(data, str):
        df = pd.read_csv(data, dtype=str, keep_default_na=False, na_values=['', 'NA', 'NaN', 'nan'])
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise TypeError("`data` must be a file path (str) or a pandas.DataFrame")

    # ensure required columns exist
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # coerce required numeric columns to floats (errors -> NaN)
    for c in required_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # drop or keep rows with missing numeric inputs
    subset = [c for c in required_cols]  # we require all of these to compute
    if not keep_nulls:
        df_clean = df.dropna(subset=subset).copy()
    else:
        df_clean = df.copy()

    # compute pm_total
    pmra = df_clean["pmra"].astype(float)
    pmdec = df_clean["pmdec"].astype(float)
    pm_total = np.sqrt(pmra**2 + pmdec**2)

    # compute pm_total_error using propagation:
    # sigma_pm = sqrt( (pmra * sigma_pmra)^2 + (pmdec * sigma_pmdec)^2 ) / pm_total
    sigma_pmra = df_clean["pmra_error"].astype(float)
    sigma_pmdec = df_clean["pmdec_error"].astype(float)
    numerator = np.sqrt((pmra * sigma_pmra)**2 + (pmdec * sigma_pmdec)**2)

    with np.errstate(divide='ignore', invalid='ignore'):
        pm_total_error = numerator / pm_total

    # replace inf with NaN
    pm_total_error = pd.Series(pm_total_error).replace([np.inf, -np.inf], np.nan).values

    # build output DataFrame (keep ra, dec, parallax, parallax_error from the cleaned DF)
    out_df = pd.DataFrame({
        "ra": df_clean["ra"].astype(float),
        "dec": df_clean["dec"].astype(float),
        "pm_total": pm_total,
        "pm_total_error": pm_total_error,
        "parallax": df_clean["parallax"].astype(float),
        "parallax_error": df_clean["parallax_error"].astype(float),
    }, index=df_clean.index)

    # write to CSV if requested
    if output_csv is not None:
        if float_format is None:
            out_df.to_csv(output_csv, index=False)
        else:
            out_df.to_csv(output_csv, index=False, float_format=float_format)

    return out_df

