import data_loader
import data_processor
import model_trainer
import visualizer
import pandas as pd

LOCAL_CSV_PATH = 'Data Historis Emas Berjangka.csv' 
START_DATE = '2020-01-01'
END_DATE = '2025-11-29'

def main():
    df_gld = data_loader.get_global_data('GLD', START_DATE, END_DATE)
    df_usd = data_loader.get_global_data('USDIDR=X', START_DATE, END_DATE)
    df_local = data_loader.get_local_data(LOCAL_CSV_PATH)

    if df_local is not None and not df_gld.empty and not df_usd.empty:
        df_clean = data_processor.align_datasets(df_local, df_gld, df_usd)
        
        if df_clean.empty:
            print(" Data hasil gabungan kosong. Cek tanggal atau format data.")
            return

        results = model_trainer.train_gold_model(df_clean)
        
        visualizer.print_metrics(results)

        test_dates = df_clean.loc[results['X_test'].index, 'Date']
        visualizer.plot_results(test_dates, results['y_test'], results['y_pred'])
        
    else:
        print(" Program berhenti karena data tidak lengkap.")

if __name__ == "__main__":
    main()