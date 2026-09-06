# import numpy as np
# import pandas as pd
# from tvDatafeed import TvDatafeed, Interval
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import load_model
# import matplotlib.pyplot as plt
# import streamlit as st  
# import time

# # =========================
# # TV Datafeed + Streamlit
# # =========================
# tv = TvDatafeed()

# st.title('Stock Price Prediction')

# user = st.text_input(
#     'Nhập mã cổ phiếu (ví dụ: HPG, SHS, BSR...)',
#     'HPG'
# )

# ticker = user.upper().strip()


# # Loading message
# loading_msg = st.empty()
# loading_msg.text("Đang lấy dữ liệu thị trường, vui lòng chờ vài giây...")


# # thử lần lượt các sàn
# exchanges = ["HOSE", "HNX", "UPCOM"]

# df = None
# selected_exchange = None


# for exchange in exchanges:
#     try:
#         df = tv.get_hist(
#             symbol=ticker,
#             exchange=exchange,
#             interval=Interval.in_daily,
#             n_bars=5000
#         )
#         if df is not None and not df.empty:
#             selected_exchange = exchange
#             break
#     except:
#         continue


# loading_msg.empty()


# # nếu không tìm thấy mã
# if df is None or df.empty:
#     st.warning(
#         f"Mã cổ phiếu **{ticker}** không tồn tại trên HOSE, HNX hoặc UPCOM.\n"
#         "Ví dụ hợp lệ: HPG, FPT, SHS, PVS, BSR, ACV..."
#     )
#     st.stop()

# # Chuẩn hóa dữ liệu
# df.reset_index(inplace=True)
# df.rename(columns={'datetime': 'time'}, inplace=True)
# for col in ['open', 'high', 'low', 'close']:
#     df[col] = df[col] / 1000
    
# # Chia dữ liệu train/test
# split = int(len(df) * 0.7)
# data_training = df[['close']].iloc[:split].copy()
# data_testing = df[['close']].iloc[split:].copy()

# # =========================
# # Load model + scaler
# # =========================
# model = load_model("model/trade_long_term/model_keras_04012026_C2.keras")
# scaler = MinMaxScaler(feature_range=(0,1))
# scaler.fit(data_training)  # chỉ fit trên train

# # =========================
# # Dự đoán 5 ngày tiếp theo (Fix Drift + Sideway)
# # =========================
# future_days = 5
# window_size = 100
# last_window = df[['close']].tail(window_size)
# last_scaled = scaler.transform(last_window)

# future_predictions = []
# current_window = last_scaled.copy()

# # Volatility dynamic
# returns = df['close'].pct_change()
# volatility = returns.rolling(20).std().iloc[-1]
# max_change = volatility * 2
# max_change = max(0.01, min(0.05, max_change))
# alpha = 0.7

# for i in range(future_days):
#     x_input = np.array([current_window])
#     next_pred = model.predict(x_input, verbose=0)

#     anchor = current_window[-1][0] if i == 0 else future_predictions[-1]
#     blended = alpha * next_pred[0][0] + (1 - alpha) * anchor

#     prev = current_window[-1][0]
#     change = np.clip(blended - prev, -max_change, max_change)
#     blended = prev + change

#     future_predictions.append(blended)
#     current_window = np.vstack((current_window[1:], [[blended]]))

# future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1,1))

# # =========================
# # Tạo ngày cho dự đoán
# # =========================
# last_date = df['time'].iloc[-1]
# future_dates = pd.date_range(start=last_date, periods=future_days+1, freq='B')[1:]

# # Biểu đồ dự đoán 5 ngày
# st.subheader(f'Dự đoán {future_days} ngày tiếp theo của {ticker}')
# fig = plt.figure(figsize=(12,6))
# real_time = df['time'].tail(50)
# real_price = df['close'].tail(50)

# plt.plot(real_time, real_price, label='Real Price', color='blue')
# extended_dates = [real_time.iloc[-1]] + list(future_dates)
# extended_prices = [real_price.iloc[-1]] + list(future_predictions.flatten())
# plt.plot(extended_dates, extended_prices, linestyle='--', marker='o', color='red', label='Prediction')
# plt.axvspan(future_dates[0], future_dates[-1], color='orange', alpha=0.1)
# plt.legend()
# plt.xticks(rotation=45)
# plt.grid(True, linestyle='--', alpha=0.5)
# st.pyplot(fig)

# # Nhận xét xu hướng ngắn hạn
# current_price = df['close'].iloc[-1]
# price_min = future_predictions.min()
# price_max = future_predictions.max()
# change_min = (price_min - current_price)/current_price*100
# change_max = (price_max - current_price)/current_price*100
# change_end = (future_predictions[-1][0] - current_price)/current_price*100
# threshold_sideway = 2.0
# if abs(change_end) < threshold_sideway:
#     trend = "↔️ Sideway"
# elif change_end > 0:
#     trend = "📈 Tăng"
# else:
#     trend = "📉 Giảm"

# future_dates_list = pd.date_range(start=pd.to_datetime(df['time'].iloc[-1])+pd.Timedelta(days=1),
#                                   periods=future_predictions.shape[0], freq='B')
# future_df = pd.DataFrame({
#     "Ngày": future_dates_list.strftime('%d/%m'),
#     "Giá dự đoán": future_predictions.flatten()
# })

# st.subheader("Nhận định ngắn hạn (5 ngày kế tiếp)")
# st.write(f"""
# - Xu hướng dự đoán: **{trend}**
# - Khoảng giá dự kiến: từ **{price_min:.2f}** đến **{price_max:.2f}**
# - Mức độ dự kiến thay đổi: từ **{change_min:.2f}%** đến **{change_max:.2f}%**
# - Giá hiện tại: **{current_price:.2f}**
# - Giá dự kiến sau {future_days} phiên: **{future_predictions[-1][0]:.2f}**
# """)
# st.info("⚠️ Đây là thông tin tham khảo, không phải khuyến nghị đầu tư.")
# st.table(future_df)

import numpy as np
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import plotly.graph_objects as go
import streamlit as st

# =========================
# Page config & global style
# =========================
st.set_page_config(
    page_title="Stock Price Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* ---- Global ---- */
    html, body, [class*="css"]  {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #f7f9fc;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---- Header ---- */
    .app-header {
        background: linear-gradient(135deg, #0f2748 0%, #1c4a8a 100%);
        padding: 28px 36px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(15, 39, 72, 0.18);
    }
    .app-header h1 {
        color: #ffffff;
        font-size: 30px;
        font-weight: 700;
        margin: 0;
    }
    .app-header p {
        color: #cfe0f5;
        font-size: 14px;
        margin: 6px 0 0 0;
    }

    /* ---- Metric cards ---- */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e7ecf3;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 2px 10px rgba(15, 39, 72, 0.05);
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #6b7280;
    }

    /* ---- Section titles ---- */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f2748;
        margin: 8px 0 14px 0;
        border-left: 4px solid #1c4a8a;
        padding-left: 10px;
    }

    /* ---- Badge ---- */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }
    .badge-up   { background:#e6f7ee; color:#0f9d58; }
    .badge-down { background:#fdecec; color:#d93025; }
    .badge-flat { background:#eef2f7; color:#5f6b7a; }

    /* ---- Disclaimer ---- */
    .disclaimer {
        background-color: #fff8e6;
        border: 1px solid #ffe3a3;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 13px;
        color: #6b5300;
        margin-top: 18px;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background-color: #0f2748;
    }
    section[data-testid="stSidebar"] * {
        color: #eaf1fb !important;
    }

    /* Ô nhập liệu (text input, select...) có nền trắng -> chữ phải tối */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        color: #0f2748 !important;
        background-color: #ffffff !important;
        caret-color: #0f2748 !important;
    }

    /* Nút bấm trong sidebar có nền trắng -> chữ phải tối */
    section[data-testid="stSidebar"] button p,
    section[data-testid="stSidebar"] button span,
    section[data-testid="stSidebar"] div[data-testid="stBaseButton-secondary"] p {
        color: #0f2748 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================
# Sidebar controls
# =========================
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình")
    ticker_input = st.text_input(
        "Mã cổ phiếu",
        value="HPG",
        help="Ví dụ: HPG, FPT, SHS, PVS, BSR, ACV..."
    )
    future_days = st.slider("Số phiên dự đoán", min_value=3, max_value=10, value=5)
    st.markdown("---")
    st.markdown(
        "**Sàn hỗ trợ:** HOSE · HNX · UPCOM  \n"
        "**Nguồn dữ liệu:** TradingView  \n"
        "**Mô hình:** LSTM (Keras)"
    )
    run_btn = st.button("🔍 Phân tích", use_container_width=True)

ticker = ticker_input.upper().strip()

# =========================
# Header
# =========================
st.markdown(
    f"""
    <div class="app-header">
        <h1>📈 Stock Price Prediction</h1>
        <p>Dự báo xu hướng giá cổ phiếu ngắn hạn dựa trên mô hình học sâu (LSTM)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# Data fetching
# =========================
tv = TvDatafeed()
exchanges = ["HOSE", "HNX", "UPCOM"]

with st.spinner(f"Đang lấy dữ liệu thị trường cho {ticker}..."):
    df = None
    selected_exchange = None
    for exchange in exchanges:
        try:
            df = tv.get_hist(
                symbol=ticker,
                exchange=exchange,
                interval=Interval.in_daily,
                n_bars=5000
            )
            if df is not None and not df.empty:
                selected_exchange = exchange
                break
        except Exception:
            continue

if df is None or df.empty:
    st.warning(
        f"Mã cổ phiếu **{ticker}** không tồn tại trên HOSE, HNX hoặc UPCOM.\n\n"
        "Ví dụ hợp lệ: HPG, FPT, SHS, PVS, BSR, ACV..."
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
model = load_model("exp/trainbase_04012026/model_keras_04012026_C2.keras")
scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit(data_training)

# =========================
# Dự đoán N ngày tiếp theo (Fix Drift + Sideway)
# =========================
window_size = 100
last_window = df[['close']].tail(window_size)
last_scaled = scaler.transform(last_window)

future_predictions = []
current_window = last_scaled.copy()

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

future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# =========================
# Ngày cho dự đoán
# =========================
last_date = df['time'].iloc[-1]
future_dates = pd.date_range(start=last_date, periods=future_days + 1, freq='B')[1:]

# =========================
# Tính toán chỉ số
# =========================
current_price = df['close'].iloc[-1]
price_min = future_predictions.min()
price_max = future_predictions.max()
change_min = (price_min - current_price) / current_price * 100
change_max = (price_max - current_price) / current_price * 100
change_end = (future_predictions[-1][0] - current_price) / current_price * 100
threshold_sideway = 2.0

if abs(change_end) < threshold_sideway:
    trend_label, badge_class, trend_icon = "Sideway", "badge-flat", "↔️"
elif change_end > 0:
    trend_label, badge_class, trend_icon = "Tăng", "badge-up", "📈"
else:
    trend_label, badge_class, trend_icon = "Giảm", "badge-down", "📉"

# =========================
# KPI cards
# =========================
st.markdown(f'<div class="section-title">Tổng quan · {ticker} ({selected_exchange})</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Giá hiện tại", f"{current_price:.2f}")
col2.metric(
    f"Giá dự kiến sau {future_days} phiên",
    f"{future_predictions[-1][0]:.2f}",
    f"{change_end:+.2f}%"
)
col3.metric("Khoảng giá dự kiến", f"{price_min:.2f} – {price_max:.2f}")
with col4:
    st.markdown(
        f"""<div style="padding-top:6px;">
        <div style="font-weight:600;color:#6b7280;font-size:14px;margin-bottom:8px;">Xu hướng dự báo</div>
        <span class="badge {badge_class}">{trend_icon} {trend_label}</span>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")

# =========================
# Biểu đồ dự đoán (Plotly - interactive)
# =========================
st.markdown('<div class="section-title">Biểu đồ giá & dự báo</div>', unsafe_allow_html=True)

real_time = df['time'].tail(50)
real_price = df['close'].tail(50)

extended_dates = [real_time.iloc[-1]] + list(future_dates)
extended_prices = [real_price.iloc[-1]] + list(future_predictions.flatten())

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=real_time, y=real_price,
    mode='lines', name='Giá thực tế',
    line=dict(color='#1c4a8a', width=2.5)
))
fig.add_trace(go.Scatter(
    x=extended_dates, y=extended_prices,
    mode='lines+markers', name='Dự đoán',
    line=dict(color='#d93025', width=2, dash='dash'),
    marker=dict(size=7, symbol='circle')
))
fig.add_vrect(
    x0=future_dates[0], x1=future_dates[-1],
    fillcolor="orange", opacity=0.08, line_width=0
)
fig.update_layout(
    template="plotly_white",
    height=460,
    margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_title=None,
    yaxis_title="Giá (nghìn đồng)",
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# Nhận định + bảng chi tiết
# =========================
future_dates_list = pd.date_range(
    start=pd.to_datetime(df['time'].iloc[-1]) + pd.Timedelta(days=1),
    periods=future_predictions.shape[0], freq='B'
)
future_df = pd.DataFrame({
    "Ngày": future_dates_list.strftime('%d/%m'),
    "Giá dự đoán": future_predictions.flatten().round(2),
})

left, right = st.columns([1.1, 1])
with left:
    st.markdown('<div class="section-title">Nhận định ngắn hạn</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        - Xu hướng dự đoán: **{trend_icon} {trend_label}**
        - Khoảng giá dự kiến: **{price_min:.2f} → {price_max:.2f}**
        - Mức thay đổi dự kiến: **{change_min:.2f}% → {change_max:.2f}%**
        - Giá hiện tại: **{current_price:.2f}**
        - Giá dự kiến sau {future_days} phiên: **{future_predictions[-1][0]:.2f}**
        """
    )

with right:
    st.markdown('<div class="section-title">Chi tiết dự đoán theo phiên</div>', unsafe_allow_html=True)
    st.dataframe(future_df, use_container_width=True, hide_index=True)

st.markdown(
    """<div class="disclaimer">⚠️ Đây là thông tin tham khảo dựa trên mô hình học máy, không phải khuyến nghị đầu tư.
    Nhà đầu tư nên tham khảo thêm các nguồn thông tin khác trước khi ra quyết định.</div>""",
    unsafe_allow_html=True,
)