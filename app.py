import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import matplotlib.pyplot as plt
import streamlit as st  
import time

# =========================
# TV Datafeed + Streamlit
# =========================
tv = TvDatafeed()
st.title('Stock Price Prediction')

user = st.text_input(
    'Nhập mã cổ phiếu (ví dụ: HPG, VNM, VIC...)',
    'HPG'
)
ticker = user.upper().strip()

# Loading message
loading_msg = st.empty()
loading_msg.text("Đang lấy dữ liệu từ HOSE, vui lòng chờ vài giây...")

# Lấy dữ liệu từ HOSE
time.sleep(2)
df = tv.get_hist(
    symbol=ticker,
    exchange='HOSE',
    interval=Interval.in_daily,
    n_bars=5000
)
loading_msg.empty()

# Check mã không thuộc HOSE
if df is None or df.empty:
    st.warning(
        f"Mã cổ phiếu **{ticker}** hiện chưa được hỗ trợ.\n"
        "Vui lòng thử lại với mã thuộc **HOSE** như: HPG, VNM, VIC, FPT..."
    )
    st.stop()

# Chuẩn hóa dữ liệu
df.reset_index(inplace=True)
df.rename(columns={'datetime': 'time'}, inplace=True)
for col in ['open', 'high', 'low', 'close']:
    df[col] = df[col] / 1000

# Chia dữ liệu train/test
split = int(len(df) * 0.7)
data_training = df[['close']].iloc[:split].copy()
data_testing = df[['close']].iloc[split:].copy()

# =========================
# Load model + scaler
# =========================
model = load_model("model/trade_long_term/model_keras_04012026_C2.keras")
scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(data_training)  # chỉ fit trên train

# =========================
# Dự đoán 5 ngày tiếp theo (Fix Drift + Sideway)
# =========================
future_days = 5
window_size = 100
last_window = df[['close']].tail(window_size)
last_scaled = scaler.transform(last_window)

future_predictions = []
current_window = last_scaled.copy()

# Volatility dynamic
returns = df['close'].pct_change()
volatility = returns.rolling(20).std().iloc[-1]
max_change = volatility * 2
max_change = max(0.01, min(0.05, max_change))
alpha = 0.7

for i in range(future_days):
    x_input = np.array([current_window])
    next_pred = model.predict(x_input, verbose=0)

    anchor = current_window[-1][0] if i == 0 else future_predictions[-1]
    blended = alpha * next_pred[0][0] + (1 - alpha) * anchor

    prev = current_window[-1][0]
    change = np.clip(blended - prev, -max_change, max_change)
    blended = prev + change

    future_predictions.append(blended)
    current_window = np.vstack((current_window[1:], [[blended]]))

future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1,1))

# =========================
# Tạo ngày cho dự đoán
# =========================
last_date = df['time'].iloc[-1]
future_dates = pd.date_range(start=last_date, periods=future_days+1, freq='B')[1:]

# Biểu đồ dự đoán 5 ngày
st.subheader(f'Dự đoán {future_days} ngày tiếp theo của {ticker}')
fig = plt.figure(figsize=(12,6))
real_time = df['time'].tail(50)
real_price = df['close'].tail(50)

plt.plot(real_time, real_price, label='Real Price', color='blue')
extended_dates = [real_time.iloc[-1]] + list(future_dates)
extended_prices = [real_price.iloc[-1]] + list(future_predictions.flatten())
plt.plot(extended_dates, extended_prices, linestyle='--', marker='o', color='red', label='Prediction')
plt.axvspan(future_dates[0], future_dates[-1], color='orange', alpha=0.1)
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# Nhận xét xu hướng ngắn hạn
current_price = df['close'].iloc[-1]
price_min = future_predictions.min()
price_max = future_predictions.max()
change_min = (price_min - current_price)/current_price*100
change_max = (price_max - current_price)/current_price*100
change_end = (future_predictions[-1][0] - current_price)/current_price*100
threshold_sideway = 2.0
if abs(change_end) < threshold_sideway:
    trend = "↔️ Sideway"
elif change_end > 0:
    trend = "📈 Tăng"
else:
    trend = "📉 Giảm"

future_dates_list = pd.date_range(start=pd.to_datetime(df['time'].iloc[-1])+pd.Timedelta(days=1),
                                  periods=future_predictions.shape[0], freq='B')
future_df = pd.DataFrame({
    "Ngày": future_dates_list.strftime('%d/%m'),
    "Giá dự đoán": future_predictions.flatten()
})

st.subheader("Nhận định ngắn hạn (5 ngày kế tiếp)")
st.write(f"""
- Xu hướng dự đoán: **{trend}**
- Khoảng giá dự kiến: từ **{price_min:.2f}** đến **{price_max:.2f}**
- Mức độ dự kiến thay đổi: từ **{change_min:.2f}%** đến **{change_max:.2f}%**
- Giá hiện tại: **{current_price:.2f}**
- Giá dự kiến sau {future_days} phiên: **{future_predictions[-1][0]:.2f}**
""")
st.info("⚠️ Đây là thông tin tham khảo, không phải khuyến nghị đầu tư.")
st.table(future_df)