# 台積電股價預測系統（LSTM + CNN-LSTM + GRU 集成模型）

本專案利用深度學習結合技術指標（RSI、MACD、OBV）來預測台積電（2330.TW）股價。  
透過 LSTM、CNN-LSTM、GRU 三種模型的集成學習（Ensemble），提升預測準確率與穩定性。

---

## 📈 專案特色

- 使用技術指標：RSI、MACD、OBV  
- 以 60 天為時間序列視窗進行股價預測  
- 模型架構包含：LSTM、CNN-LSTM、GRU  
- 集成三模型預測結果並取平均  
- 儲存訓練模型與預測結果

---

## 🧰 環境需求

- Python 3.8 以上

### 安裝必要套件

```bash
pip install pandas numpy scikit-learn tensorflow ta matplotlib joblib openpyxl
🗂 專案結構
bash
複製
編輯
├── stock_predictor.py            # 模型訓練與預測主程式
├── 2330_history.xlsx             # 台積電歷史股價資料（需事先取得）
├── ensemble_prediction_results.csv  # 預測結果（輸出）
├── ensemble_model_1.h5 ~ 3.h5    # 模型權重儲存檔
├── ensemble_scaler.save          # 特徵標準化器儲存檔
└── README.md                     # 專案說明文件
▶️ 使用說明
準備資料
請自行準備並放置台積電歷史股價資料，檔名為 2330_history.xlsx，格式需包含日期（Date）、收盤價（Close）、成交量（Volume）等欄位。

執行訓練與預測

bash
複製
編輯
python stock_predictor.py
計算技術指標 RSI、MACD、OBV

正規化特徵並切分訓練與測試資料

訓練 LSTM、CNN-LSTM、GRU 三種模型

集成模型進行預測，並繪製預測結果與訓練損失圖

將模型與結果輸出至檔案

📊 輸出檔案
ensemble_prediction_results.csv ：包含日期、實際收盤價、集成模型預測收盤價

ensemble_model_1.h5 ~ ensemble_model_3.h5 ：訓練完成的模型權重

ensemble_scaler.save ：資料標準化器，方便未來資料轉換

⚠️ 法律聲明
本專案不包含爬蟲程式碼，需自行取得歷史股價資料。

請確保取得資料的合法性與合規性。

本專案僅供學術研究與學習用途，勿用於商業交易。
