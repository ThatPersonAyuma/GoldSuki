import pandas as pd

def align_datasets(df_local, df_global_gold, df_global_usd):
    """
    Menyelaraskan data lokal dan global (Time Series Alignment).
    """
    print("[INFO] Menyelaraskan data (Merge Asof)...")
    
    df_local = df_local.sort_values('Date')
    df_global_gold = df_global_gold.sort_values('Date')
    df_global_usd = df_global_usd.sort_values('Date')

    df_global_gold = df_global_gold.rename(columns={'Close': 'Close_GLD_USD'})
    df_global_usd = df_global_usd.rename(columns={'Close': 'Close_USDIDR'})
    
    # Menggabungkan data harga saham GLD dan kurs USD/IDR
    df_usd_gld = pd.merge(
        df_global_gold[['Date', 'Close_GLD_USD']],
        df_global_usd[['Date', 'Close_USDIDR']],
        on='Date',
        how='inner'
    )

    # konversi mata uang
    df_usd_gld['Close_GLD_IDR_PerShare'] = df_usd_gld['Close_GLD_USD'] * df_usd_gld['Close_USDIDR']

    df_global_gold = df_usd_gld[['Date', 'Close_GLD_IDR_PerShare']].sort_values('Date')
    df_global_gold = df_global_gold.rename(columns={'Close_GLD_IDR_PerShare': 'Close_GLD_IDR_PerShare'})

    # Merge 1: Gabungkan Emas Lokal dengan Emas Global (mencari data global terakhir yang tersedia)
    df_merged = pd.merge_asof(
        df_local, 
        df_global_gold, 
        on='Date', 
        direction='backward'
    )

    # Merge 2: Gabungkan hasilnya dengan Kurs USD
    df_merged = pd.merge_asof(
        df_merged, 
        df_global_usd, 
        on='Date', 
        direction='backward'
    )

    # Hapus baris yang memiliki nilai kosong (NaN)
    df_clean = df_merged.dropna().reset_index(drop=True)
    
    return df_clean