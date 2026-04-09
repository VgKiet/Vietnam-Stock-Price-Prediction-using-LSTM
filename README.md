# Vietnam Stock Price Prediction using LSTM

## Tổng quan dự án
Dự án **Vietnam Stock Price Prediction using LSTM** nhằm phát triển một mô hình dự báo giá cổ phiếu trên thị trường Việt Nam, tập trung vào các cổ phiếu niêm yết trên sàn **HOSE, HNX, UPCOM**. Mục tiêu là giúp nhà đầu tư có thể phân tích xu hướng ngắn hạn, dự đoán giá tương lai trong 5 ngày tiếp theo, và hỗ trợ đưa ra quyết định giao dịch một cách tham khảo.

Dự án sử dụng dữ liệu lịch sử giá cổ phiếu, bao gồm:
- Giá mở cửa
- Giá cao nhất
- Giá thấp nhất
- Giá đóng cửa
- Khối lượng giao dịch

Dữ liệu được thu thập tự động thông qua thư viện **TVDatafeed**, đảm bảo tính đầy đủ và cập nhật theo thời gian thực.

Sử dụng mô hình **LSTM (Long Short-Term Memory)** để dự đoán xu hướng
giá ngắn hạn (5 ngày) và trực quan hóa kết quả bằng **Streamlit**.

------------------------------------------------------------------------

## Tính năng

-   Thu thập dữ liệu lịch sử cổ phiếu từ TradingView bằng **TVDatafeed**
-   Xử lý và chuẩn hóa dữ liệu bằng **Pandas, NumPy, Scikit-learn**
-   Xây dựng và huấn luyện mô hình **LSTM** bằng **Keras/TensorFlow**
-   Vẽ biểu đồ giá cổ phiếu thực tế và dự đoán kèm các đường:
    -   MA20
    -   MA50
    -   MA100
    -   MA200
-   Dự đoán giá ngắn hạn 5 ngày và phân tích xu hướng:
    -   tăng 📈
    -   giảm 📉
    -   sideway ↔️
-   Giao diện trực quan với **Streamlit** giúp dễ dàng sử dụng

------------------------------------------------------------------------

## Công nghệ sử dụng

-   Python 
-   TVDatafeed
-   Pandas
-   NumPy
-   Scikit-learn
-   Keras + TensorFlow
-   Matplotlib
-   Streamlit

------------------------------------------------------------------------

## Cài đặt

### 1. Clone repository

``` bash
git clone <link-repo>
cd <ten-thu-muc-du-an>
```

### 2. Cài đặt các thư viện cần thiết

``` bash
pip install git+https://github.com/rongardF/tvdatafeed.git
pip install numpy pandas scikit-learn matplotlib keras tensorflow streamlit
```

------------------------------------------------------------------------

## Chạy ứng dụng

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## Hướng dẫn sử dụng

1.  Nhập mã cổ phiếu thuộc sàn HOSE (ví dụ: HPG, VNM, VIC,...)

2.  Các tính năng trong giao diện:

-   Dự đoán 5 ngày tiếp theo: Mô hình LSTM dự đoán giá tương lai kèm
    biểu đồ so sánh giá thực tế và dự đoán
-   Nhận định xu hướng ngắn hạn: Xác định cổ phiếu đang tăng 📈, giảm 📉
    hay đi ngang ↔️ và hiển thị mức độ dự kiến thay đổi (%) so với giá
    hiện tại

------------------------------------------------------------------------

## Kết quả hiển thị

-   Biểu đồ giá thực tế và dự đoán
-   Bảng giá dự kiến từng ngày trong 5 phiên tiếp theo
-   Nhận định xu hướng ngắn hạn: tăng 📈 / giảm 📉 / sideway ↔️
-   Mức độ dự kiến thay đổi giá (%)

------------------------------------------------------------------------

## Minh họa

![demo](https://raw.githubusercontent.com/VgKiet/Vietnam-Stock-Price-Prediction-using-LSTM/master/image.png)



------------------------------------------------------------------------

## Lưu ý

-   Dự đoán chỉ mang tính chất tham khảo, không phải khuyến nghị đầu tư
-   Nhà đầu tư cần tự đánh giá và chịu trách nhiệm với quyết định giao
    dịch của mình
