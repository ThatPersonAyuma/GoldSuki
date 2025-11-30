import yfinance as yf
import pandas as pd
import os

def get_global_data(ticker, start_date, end_date):
    """Mengambil data dari Yahoo Finance."""
    print(f"[INFO] Mengunduh data {ticker}...")
    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval='1wk')
        
        # Fix untuk update yfinance terbaru yang mungkin menghasilkan MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df = df.reset_index()
        
        # Pastikan kolom tanggal bernama 'Date' dan zona waktu dihapus
        if 'Date' in df.columns:
            # Pastikan kolom Date benar-benar bertipe datetime sebelum mencoba .dt
            if pd.api.types.is_datetime64_any_dtype(df['Date']):
                if df['Date'].dt.tz is not None:
                    df['Date'] = df['Date'].dt.tz_localize(None)
            
        return df
    except Exception as e:
        print(f" Gagal mengunduh {ticker}: {e}")
        return pd.DataFrame()

def get_local_data(filepath):
    """Membaca CSV Lokal dengan penanganan format angka Indonesia."""
    print(f"[INFO] Membaca file lokal: {filepath}")
    
    if not os.path.exists(filepath):
        print(f" File tidak ditemukan: {filepath}")
        return None

    try:
        # PERBAIKAN UTAMA DI SINI:
        # Kita memberitahu pandas bahwa kolom tanggal bernama 'Tanggal'
        df = pd.read_csv(
            filepath,
            decimal=',',       # Menangani desimal koma (4.269,80)
            thousands='.',     # Menangani ribuan titik
            parse_dates= ["Tanggal"], # NAMA KOLOM HARUS MASUK LIST
            dayfirst=True      # Format Indonesia DD/MM/YYYY
        )
        
        # Standarisasi nama kolom
        # 'Terakhir' adalah harga Close
        df = df.rename(columns={'Tanggal': 'Date', 'Terakhir': 'Close_Local'})
        
        df['Close_Local'] = df['Close_Local'] * 1000.0
        
        # Pastikan tipe data datetime
        if df['Date'].dt.tz is not None:
            df['Date'] = df['Date'].dt.tz_localize(None)
             
        return df.sort_values('Date')
    except Exception as e:
        print(f" Gagal membaca CSV: {e}")
        return None