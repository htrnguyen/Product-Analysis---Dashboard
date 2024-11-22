### README: **Product Analysis - Dashboard**

---

#### **Giới Thiệu**

Ứng dụng Dashboard giúp trực quan hóa dữ liệu sản phẩm dựa trên các chỉ số cơ bản như đánh giá, giá giảm, số lượng đánh giá, v.v. Ứng dụng này sử dụng **Dash** để xây dựng giao diện tương tác và **Plotly** để hiển thị biểu đồ.

Bạn có thể dễ dàng lọc dữ liệu, xem các biểu đồ trực quan, và hiểu rõ hơn về sản phẩm trong dữ liệu của mình.

---

#### **Tính Năng Chính**

1. **Header Thông Tin Tổng Quan**:

    - Hiển thị:
        - Tổng số sản phẩm.
        - Giá trị trung bình đánh giá.
        - Giá giảm trung bình.
        - Số lượng đánh giá trung bình.

2. **Bộ Lọc Linh Hoạt**:

    - Lọc theo **Loại Chính** và **Loại Con** để thu hẹp phạm vi dữ liệu.

3. **Các Loại Biểu Đồ**:

    - **Phân phối đánh giá (Ratings)**: Hiển thị phân phối các mức đánh giá từ 1 đến 5.
    - **Giá giảm vs Giá thực (Scatter Plot)**: So sánh mối quan hệ giữa giá giảm và giá thực.
    - **Top-N sản phẩm có số lượng đánh giá cao nhất**:
        - Hiển thị Top 10 (hoặc số lượng tùy chọn) sản phẩm phổ biến nhất.
        - Tên sản phẩm dài được rút gọn, hiển thị đầy đủ khi hover.
    - **Phân bố sản phẩm theo Loại Con (Treemap)**: Trực quan hóa tỷ lệ sản phẩm trong từng loại con.
    - **Phân tích tỷ lệ giảm giá (Box Plot)**: Hiển thị sự phân bố tỷ lệ giảm giá theo từng loại sản phẩm.

4. **Tính Năng Hover**:
    - Hiển thị thông tin chi tiết (như tên đầy đủ sản phẩm) khi người dùng di chuột vào biểu đồ.

---

#### **Hướng Dẫn Sử Dụng**

1. **Yêu Cầu Cài Đặt**:

    - Python 3.7 trở lên.
    - Các thư viện:
        - `dash`
        - `pandas`
        - `plotly`

2. **Cài Đặt Thư Viện**:
   Chạy lệnh sau để cài đặt các thư viện cần thiết:

    ```bash
    pip install -r requirements.txt
    ```

3. **Cấu Trúc Dữ Liệu**
   Dữ liệu mẫu phải được lưu trong file `sample_data.csv` (hoặc file bạn chọn) với cấu trúc như sau:

    - **name**: Tên sản phẩm.
    - **main_category**: Loại chính của sản phẩm.
    - **sub_category**: Loại con của sản phẩm.
    - **ratings**: Điểm đánh giá của sản phẩm.
    - **no_of_ratings**: Số lượng đánh giá.
    - **discount_price**: Giá sau giảm.
    - **actual_price**: Giá gốc (trước khi giảm).

4. **Chạy Ứng Dụng**:
    - Lưu file `app.py` trong cùng thư mục với file dữ liệu.
    - Chạy lệnh sau:
        ```bash
        python app.py
        ```
    - Mở trình duyệt và truy cập: [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

---

#### **Hướng Dẫn Sử Dụng Giao Diện**

1. **Header**:

    - Hiển thị các thông tin cơ bản dựa trên dữ liệu hiện tại.
    - Thông tin sẽ cập nhật khi áp dụng các bộ lọc.

2. **Bộ Lọc**:

    - **Loại Chính**: Lọc dữ liệu theo danh mục chính.
    - **Loại Con**: Tự động thay đổi dựa trên Loại Chính được chọn.
    - **Loại Biểu Đồ**: Chọn một trong các biểu đồ để hiển thị dữ liệu.

3. **Biểu Đồ**:
    - Tất cả biểu đồ tương tác, người dùng có thể di chuột hoặc phóng to để xem chi tiết.

---

#### **Mô Tả Biểu Đồ**

| Loại Biểu Đồ                       | Mô Tả                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------- |
| **Phân phối đánh giá**             | Histogram hiển thị số lượng đánh giá theo từng mức đánh giá từ 1 đến 5.               |
| **Giá giảm vs Giá thực**           | Scatter plot thể hiện mối quan hệ giữa giá giảm và giá gốc của sản phẩm.              |
| **Top-N sản phẩm**                 | Biểu đồ thanh ngang hiển thị các sản phẩm phổ biến nhất dựa trên số lượng đánh giá.   |
| **Phân bố sản phẩm theo Loại Con** | Treemap hiển thị tỷ lệ sản phẩm trong từng danh mục con.                              |
| **Phân tích tỷ lệ giảm giá**       | Box plot phân tích tỷ lệ giảm giá giữa các loại sản phẩm để đánh giá tính cạnh tranh. |
