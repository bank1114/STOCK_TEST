import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Flatten, GRU
from tensorflow.keras.callbacks import EarlyStopping
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volume import OnBalanceVolumeIndicator
import joblib

# 讀取資料
#df = pd.read_excel('2330_history.xlsx', parse_dates=['Date'], index_col='Date')
df = pd.read_excel('2409.TW_history.xlsx', parse_dates=['Date'], index_col='Date')

# 加入技術指標
df['RSI'] = RSIIndicator(df['Close']).rsi()
df['MACD'] = MACD(df['Close']).macd_diff()
df['OBV'] = OnBalanceVolumeIndicator(df['Close'], df['Volume']).on_balance_volume()
df = df.dropna()

# 特徵選擇
features = df[['Close', 'RSI', 'MACD', 'OBV']]
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)

# 時序特徵處理
seq_len = 60
X, y = [], []
for i in range(seq_len, len(scaled_features)):
    X.append(scaled_features[i-seq_len:i])
    y.append(scaled_features[i, 0])  # Close作為預測目標
X, y = np.array(X), np.array(y)

# 訓練 / 測試切分
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# 模型1：LSTM
def build_lstm(input_shape):
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(LSTM(64))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# 模型2：CNN-LSTM
def build_cnn_lstm(input_shape):
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(LSTM(64))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# 模型3：GRU
def build_gru(input_shape):
    model = Sequential()
    model.add(GRU(128, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(GRU(64))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# 建立模型
input_shape = (X_train.shape[1], X_train.shape[2])
models = [build_lstm(input_shape), build_cnn_lstm(input_shape), build_gru(input_shape)]
#models = [build_cnn_lstm(input_shape)]

histories = []

# 訓練模型
early_stop = EarlyStopping(patience=50, restore_best_weights=True)
for i, model in enumerate(models):
    print(f"Training model {i+1}...")
    history = model.fit(
        X_train, y_train, epochs=300, batch_size=32, verbose=1,
        validation_data=(X_test, y_test),
        callbacks=[early_stop]
    )
    histories.append(history)

# 預測並取平均
predictions = np.array([model.predict(X_test) for model in models])
avg_prediction = np.mean(predictions, axis=0)
avg_prediction = avg_prediction.reshape(-1, 1)

# 反轉標準化
scaled_close = scaled_features[:, 0].reshape(-1, 1)
close_scaler = MinMaxScaler()
close_scaler.min_, close_scaler.scale_ = scaler.min_[0], scaler.scale_[0]
predicted_close = close_scaler.inverse_transform(avg_prediction)
actual_close = close_scaler.inverse_transform(y_test.reshape(-1, 1))

# 繪圖：預測 vs 實際
dates = df.index[-len(y_test):]
plt.figure(figsize=(12, 6))
plt.plot(dates, actual_close, label='Actual Close', color='blue')
plt.plot(dates, predicted_close, label='Predicted (Ensemble)', color='red')
plt.title('Actual vs Predicted (Ensemble)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 繪圖：損失函數
for i, history in enumerate(histories):
    plt.plot(history.history['loss'], label=f'Model {i+1} Train Loss')
    plt.plot(history.history['val_loss'], label=f'Model {i+1} Val Loss')
plt.title('Loss over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 儲存結果
ensemble_df = pd.DataFrame({
    'Date': dates,
    'Actual_Close': actual_close.flatten(),
    'Predicted_Close': predicted_close.flatten()
})
ensemble_df.to_csv('ensemble_prediction_results.csv', index=False)

# 儲存模型與Scaler
for i, model in enumerate(models):
    model.save(f'ensemble_model_{i+1}.h5')
joblib.dump(scaler, 'ensemble_scaler.save')
