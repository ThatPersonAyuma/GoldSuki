from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

def train_gold_model(df):
    """Melatih model Regresi Linear."""
    print("[INFO] Melatih model...")
    
    # Fitur (X) = Harga Global dan Kurs USD
    # Moving Average
    df['MA_3'] = df['Close_Local'].rolling(3).mean()
    df['MA_7'] = df['Close_Local'].rolling(7).mean()
    features = ['Close_GLD_IDR_PerShare', 'Close_USDIDR', 'MA_3', 'MA_7']
    # features = ['Close_GLD_IDR_PerShare', 'Close_USDIDR', 'MA_7']
    # Lag Feature
    # df['Close_Local_t-1'] = df['Close_Local'].shift(1)
    # df['Close_Local_t-7'] = df['Close_Local'].shift(7)
    # features = ['Close_GLD_IDR_PerShare', 'Close_USDIDR', 'Close_Local_t-1', 'Close_Local_t-7']
    df = df.dropna()
    # features = ['Close_GLD_IDR_PerShare', 'Close_USDIDR']
    target = 'Close_Local'
    # print(df.columns)
    X = df[features]
    y = df[target]
    # print(X)
    # print(y)

    # split Data (Tanpa Shuffle untuk Time Series)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prediksi untuk Evaluasi
    # y_pred = model.predict(X_test)
    
    # # Hitung Metrik
    # mae = mean_absolute_error(y_test, y_pred)
    # r2 = r2_score(y_test, y_pred)
    
    # mse = mean_squared_error(y_test, y_pred)
    # rmse = mse**0.5

    # results = {
    #     'model': model,
    #     'mae': mae,
    #     'mse': mse,
    #     'rmse': rmse,
    #     'r2': r2,
    #     'X_test': X_test,
    #     'y_test': y_test,
    #     'y_pred': y_pred
    # }
    
    # return results
    # Prediksi untuk Evaluasi
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Hitung Metrik train
    mae_train = mean_absolute_error(y_train, y_train_pred)
    mse_train = mean_squared_error(y_train, y_train_pred)
    rmse_train = mse_train**0.5
    r2_train = r2_score(y_train, y_train_pred)

    # Hitung Metrik test
    mae_test = mean_absolute_error(y_test, y_test_pred)
    mse_test = mean_squared_error(y_test, y_test_pred)
    rmse_test = mse_test**0.5
    r2_test = r2_score(y_test, y_test_pred)

    results = {
        'model': model,
        'train': {
            'mae': mae_train,
            'mse': mse_train,
            'rmse': rmse_train,
            'r2': r2_train
        },
        'test': {
            'mae': mae_test,
            'mse': mse_test,
            'rmse': rmse_test,
            'r2': r2_test
        },
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_test_pred
    }
    return results
