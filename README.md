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
```

🗂 專案結構
```bash
├── LSTM_CNN_STOCK_v5.py            # 模型訓練與預測主程式
├── 2409.TW_history.xlsx             # 友達歷史股價資料（需事先取得）
├── ensemble_prediction_results.csv  # 預測結果（輸出）
├── ensemble_model_1.h5 ~ 3.h5    # 模型權重儲存檔
├── ensemble_scaler.save          # 特徵標準化器儲存檔
└── README.md                     # 專案說明文件
```
## 使用說明

### 準備資料

請準備友達（2409.TW）歷史股價資料，並命名為：

```
2409.TW_history.xlsx
```

檔案需包含以下欄位：

- Date（日期）  
- Close（收盤價）  
- Volume（成交量）  

---

### 安裝套件

請使用以下指令安裝所需套件：

```bash
pip install pandas numpy scikit-learn tensorflow ta matplotlib joblib openpyxl
```

---

### 執行訓練與預測流程

執行主程式：

```bash
python LSTM_CNN_STOCK_v5.py
```

流程說明如下：

#### 1. 資料讀取與技術指標計算

- 從 Excel 讀取歷史股價資料  
- 計算以下技術指標：  
  - RSI：判斷是否超買或超賣，有助預測轉折  
  - MACD：判斷趨勢方向與變化  
  - OBV：分析資金流向與量價背離  

#### 2. 資料處理

- 使用過去 60 天的資料預測下一天收盤價  

#### 3. 模型訓練

建立並訓練三種模型：

- LSTM：擅長處理長期依賴關係的時間序列  
- CNN-LSTM：提取短期變化與學習長期趨勢  
- GRU：結構簡單、效率高，效果接近 LSTM  

#### 4. 集成預測與視覺化

- 將三個模型的預測結果取平均  
- 繪製實際 vs 預測收盤價圖與訓練損失圖  

#### 5. 結果儲存

- 儲存預測結果 CSV  
- 儲存模型訓練權重與標準化器  

---

## 輸出檔案說明

| 檔案名稱 | 說明 |
|----------|------|
| `ensemble_prediction_results.csv` | 預測結果，包含日期、實際收盤價與預測收盤價 |
| `ensemble_model_1.h5` ~ `ensemble_model_3.h5` | 三個模型的訓練結果 |
| `ensemble_scaler.save` | 特徵標準化器，供未來資料轉換使用 |
---
## 成果展示

訓練loss圖:
![image](https://github.com/user-attachments/assets/140e8bd4-1361-4aad-8ae2-0ed636d25547)

股市預測圖:
![image](https://github.com/user-attachments/assets/7d7e9583-93d5-4369-af4d-1708370046ce)
---
## 結論

- **整體趨勢準確**  
  模型能掌握股價中長期趨勢，行情穩定時預測方向與實際相符。

- **價格誤差分析**  
  - 轉折點（如4月中旬大跌、8月初急跌、10月反彈）反應較慢，敏感度有限。  
  - 平均日誤差約 ±10～30元，高波動期誤差可達 ±40元以上。

- **高點偏保守**  
  股價創高時預測值偏低，模型不易捕捉突破行情。

- **低點偏樂觀**  
  大跌期間預測值偏高，模型對下跌風險反應不足。

- **模型穩定性佳**  
  預測波動平滑，適合短中期投資輔助，不建議當日交易依據。

## 心得

模型整體有一定延遲性，無法直接作為交易依據。  
後續嘗試加入每季財報資料至訓練集，但因財報更新頻率較低（一個月一次），導致訓練效果不理想。

後續會再繼續做各式各樣的嘗試




