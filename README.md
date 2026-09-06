# 📈 Vietnam Stock Price Prediction using LSTM

Mô hình dự báo giá cổ phiếu trên thị trường chứng khoán Việt Nam (**HOSE, HNX, UPCOM**) sử dụng mạng nơ-ron hồi quy **LSTM (Long Short-Term Memory)**, hỗ trợ nhà đầu tư phân tích xu hướng ngắn hạn và tham khảo trước khi ra quyết định giao dịch.

<p align="center">
  <img src="https://raw.githubusercontent.com/VgKiet/Vietnam-Stock-Price-Prediction-using-LSTM/master/image.png" alt="Demo giao diện Streamlit" width="850">
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white">
  <img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00?logo=tensorflow&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white">
</p>

<p align="center">
  🔗 <strong><a href="https://vietnam-stock-price-prediction-using-lstm.streamlit.app/">Xem demo trực tiếp</a></strong>
</p>

---

## 🧭 Tổng quan

Dự án thu thập dữ liệu giá lịch sử (giá mở cửa, cao nhất, thấp nhất, đóng cửa, khối lượng giao dịch) từ TradingView thông qua **TVDatafeed**, sau đó huấn luyện mô hình **LSTM** để:

- Dự đoán giá đóng cửa trong **5 phiên giao dịch tiếp theo**
- Nhận định xu hướng ngắn hạn: **tăng 📈 / giảm 📉 / sideway ↔️**
- Trực quan hóa kết quả qua giao diện web xây dựng bằng **Streamlit**

> ⚠️ Kết quả dự đoán chỉ mang tính chất tham khảo, **không phải khuyến nghị đầu tư**. Nhà đầu tư cần tự đánh giá và chịu trách nhiệm với quyết định giao dịch của mình.

---

## ✨ Tính năng chính

| Nhóm | Mô tả |
|---|---|
| 📥 Thu thập dữ liệu | Lấy dữ liệu lịch sử cổ phiếu theo thời gian thực từ TradingView qua TVDatafeed |
| 🧹 Xử lý dữ liệu | Làm sạch, chuẩn hóa dữ liệu với Pandas, NumPy, Scikit-learn |
| 🤖 Huấn luyện mô hình | Xây dựng và huấn luyện mạng LSTM bằng Keras/TensorFlow |
| 📊 Trực quan hóa | Biểu đồ giá thực tế vs. dự đoán kèm các đường trung bình động MA20, MA50, MA100, MA200 |
| 🔮 Dự báo ngắn hạn | Dự đoán giá 5 phiên tới và phân loại xu hướng tăng/giảm/sideway kèm % thay đổi dự kiến |
| 🖥️ Giao diện | Ứng dụng web tương tác, dễ sử dụng với Streamlit |

---

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ:** Python
- **Thu thập dữ liệu:** TVDatafeed
- **Xử lý dữ liệu:** Pandas, NumPy, Scikit-learn
- **Mô hình học sâu:** Keras, TensorFlow
- **Trực quan hóa:** Matplotlib
- **Giao diện:** Streamlit

---

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <link-repo>
cd <ten-thu-muc-du-an>
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Cài đặt thư viện

Các thư viện cần thiết đã được liệt kê trong `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Chạy ứng dụng

```bash
streamlit run app.py
```

Sau khi chạy, ứng dụng sẽ mở tại `http://localhost:8501`.

---

## 📖 Hướng dẫn sử dụng

1. Nhập mã cổ phiếu thuộc sàn **HOSE** (ví dụ: `HPG`, `VNM`, `VIC`, ...)
2. Sử dụng các tính năng trên giao diện:
   - **Dự đoán 5 ngày tiếp theo** — mô hình LSTM dự báo giá tương lai kèm biểu đồ so sánh giá thực tế và giá dự đoán
   - **Nhận định xu hướng ngắn hạn** — xác định cổ phiếu đang tăng 📈, giảm 📉 hay đi ngang ↔️, kèm mức % thay đổi dự kiến so với giá hiện tại

---

## 📊 Kết quả hiển thị

- Biểu đồ giá thực tế và giá dự đoán
- Bảng giá dự kiến theo từng ngày trong 5 phiên tiếp theo
- Nhận định xu hướng ngắn hạn: tăng 📈 / giảm 📉 / sideway ↔️
- Mức độ dự kiến thay đổi giá (%)

---

## ⚠️ Lưu ý

- Dự đoán chỉ mang tính chất **tham khảo**, không phải khuyến nghị đầu tư.
- Nhà đầu tư cần tự đánh giá và chịu trách nhiệm với quyết định giao dịch của mình.
- Chất lượng dự đoán phụ thuộc vào dữ liệu lịch sử và có thể không phản ánh chính xác các biến động thị trường bất thường.
