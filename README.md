# 股價預測系統（LSTM + CNN-LSTM + GRU 集成模型）

本專案利用深度學習結合技術指標（RSI、MACD、OBV）來預測友達股價。  
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

- Python 3.12

### 安裝必要套件

```bash
pip install pandas numpy scikit-learn tensorflow ta matplotlib joblib openpyxl
```bash
🗂 專案結構

├── LSTM_CNN_STOCK_v5.py            # 模型訓練與預測主程式
├── 2409.TW_history.xlsx             # 友達歷史股價資料（需事先取得）
├── ensemble_prediction_results.csv  # 預測結果（輸出）
├── ensemble_model_1.h5 ~ 3.h5    # 模型權重儲存檔
├── ensemble_scaler.save          # 特徵標準化器儲存檔
└── README.md                     # 專案說明文件
▶️ 使用說明
準備資料
請自行準備並放置友達歷史股價資料，檔名為2409.TW_history.xlsx，格式需包含日期（Date）、收盤價（Close）、成交量（Volume）等欄位。

##執行訓練與預測流程


#LSTM_CNN_STOCK_v5.py

從 Excel 讀取歷史股價資料

計算技術指標：

SI（相對強弱指標） 用來反映股價是否處於超買或超賣狀態，有助於捕捉可能的轉折點。

MACD（移動平均收斂擴散差值） 用於判斷趨勢的方向與變化，可幫助模型辨識多空轉折。

OBV（能量潮指標） 結合成交量與價格動向，有助於模型理解資金流向與量價背離現象。

使用 60 天的歷史數據預測下一天的收盤價

建立三種模型：

STM 擅長捕捉時間序列中的長期依賴關係，適合處理有記憶性的股價資料。

CNN-LSTM 結合 CNN 的局部特徵提取能力與 LSTM 的時序學習能力，能同時理解短期波動與長期趨勢。

GRU 結構簡單、計算效率高，適合資料量中等的時序預測任務，效果接近 LSTM。


模型結果進行集成平均，得出最終預測

繪製實際 vs 預測圖表與損失函數圖

儲存預測結果與模型檔案



📊 輸出檔案
ensemble_prediction_results.csv ：包含日期、實際收盤價、集成模型預測收盤價

ensemble_model_1.h5 ~ ensemble_model_3.h5 ：訓練完成的模型權重

ensemble_scaler.save ：資料標準化器，方便未來資料轉換

成果展示



