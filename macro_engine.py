import pandas as pd

def fetch_fred_data():
    """
    Pulls key macroeconomic series directly from FRED CSV endpoints.
    Series:
    - T10Y2Y: 10-Year Minus 2-Year Treasury Spread (Yield Curve)
    - FEDFUNDS: Federal Funds Effective Rate
    - CPIAUCSL: Consumer Price Index (Inflation proxy)
    - UNRATE: Unemployment Rate
    """
    series_dict = {
        'T10Y2Y': 'Yield_Spread',
        'FEDFUNDS': 'Fed_Funds_Rate',
        'CPIAUCSL': 'CPI',
        'UNRATE': 'Unemployment'
    }
    
    dfs = []
    for code, name in series_dict.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={code}"
        df = pd.read_csv(url, parse_dates=['observation_date'], index_col='observation_date')
        # Clean up data values (convert '.' to NaN)
        df[code] = pd.to_numeric(df[code], errors='coerce')
        df = df.rename(columns={code: name})
        dfs.append(df)
        
    # Combine all series into a single dataframe and drop missing rows
    macro_df = pd.concat(dfs, axis=1).dropna()
    
    # Calculate Year-over-Year Inflation from CPI
    macro_df['Inflation_YoY'] = macro_df['CPI'].pct_change(12) * 100
    
    return macro_df
 
