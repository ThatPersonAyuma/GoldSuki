import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns 

def format_rupiah(nominal):
    """Memformat nominal angka (jutaan) menjadi string Rupiah dengan separator titik."""
    return "{:,.0f}".format(nominal).replace(",", "X").replace(".", ",").replace("X", ".")

def plot_results(dates, y_test, y_pred):
    """
    Membuat plot perbandingan antara Harga Aktual dan Prediksi Model.
    Sumbu Y dikustomisasi untuk menampilkan Nominal Rupiah Asli.
    """
    
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    df_plot = pd.DataFrame({
        'Tanggal': dates,
        'Harga Aktual (IDR)': y_test,
        'Prediksi Model (IDR)': y_pred
    })

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df_plot['Tanggal'], df_plot['Harga Aktual (IDR)'], 
            label='Harga Aktual (IDR)', 
            linestyle='-', 
            color='#1f77b4')

    ax.plot(df_plot['Tanggal'], df_plot['Prediksi Model (IDR)'], 
            label='Prediksi Model (IDR)', 
            linestyle='--', 
            color='#ff7f0e')


    ax.set_title('Prediksi Harga Emas: Aktual vs Model', fontsize=16)
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Harga (IDR)')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.xticks(rotation=45) 

    formatter = ticker.FuncFormatter(lambda x, p: format_rupiah(x))
    ax.yaxis.set_major_formatter(formatter)
    
    plt.legend()

    plt.tight_layout()
    
    plt.show()

# def print_metrics(metrics):
#     """Mencetak metrik evaluasi model."""
#     print("\n--- Metrik Evaluasi Model ---")
#     print(f"Mean Squared Error (MSE): {format_rupiah(metrics['mse'])}")
#     print(f"Root Mean Squared Error (RMSE): {format_rupiah(metrics['rmse'])}")
#     print(f"Mean Absolute Error (MAE): {format_rupiah(metrics['mae'])}")
#     print(f"R-squared (R2): {metrics['r2']:.4f}")
def print_metrics(metrics, dataset_name="Test"):
    """Mencetak metrik evaluasi model untuk dataset tertentu."""
    print(f"\n--- Metrik Evaluasi Model ({dataset_name}) ---")
    print(f"Mean Squared Error (MSE): {format_rupiah(metrics['mse'])}")
    print(f"Root Mean Squared Error (RMSE): {format_rupiah(metrics['rmse'])}")
    print(f"Mean Absolute Error (MAE): {format_rupiah(metrics['mae'])}")
    print(f"R-squared (R2): {metrics['r2']:.4f}")
