from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

def train_gold_model(df):
    """Melatih model Regresi Linear."""
    print("[INFO] Melatih model...")
    
    # Fitur (X) = Harga Global dan Kurs USD
    features = ['Close_GLD_IDR_PerShare', 'Close_USDIDR']
    target = 'Close_Local'
    
    X = df[features]
    y = df[target]

    # split Data (Tanpa Shuffle untuk Time Series)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prediksi untuk Evaluasi
    y_pred = model.predict(X_test)
    
    # Hitung Metrik
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse**0.5

    results = {
        'model': model,
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_pred
    }
    
    return results