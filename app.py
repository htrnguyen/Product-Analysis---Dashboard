import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Đọc và chuẩn hóa dữ liệu
df = pd.read_csv('data/data.csv')

# Xử lý dữ liệu thiếu
df.fillna({'main_category': 'Unknown', 'sub_category': 'Unknown'}, inplace=True)
df['discount_percentage'] = ((df['actual_price'] - df['discount_price']) / df['actual_price']) * 100

# Khởi tạo ứng dụng Dash
app = dash.Dash(__name__)

# Layout của ứng dụng
app.layout = html.Div([
    # Header hiển thị các giá trị cơ bản
    html.Div([
        html.H2("Thông Tin Dữ Liệu Được Chọn", style={"textAlign": "center", "marginBottom": "20px"}),
        html.Div([
            html.Div([
                html.H4("Tổng Số Sản Phẩm"),
                html.P(id="total_products", style={"fontSize": "20px", "fontWeight": "bold"})
            ], className="stat-box"),

            html.Div([
                html.H4("Giá Trị Trung Bình Đánh Giá"),
                html.P(id="avg_ratings", style={"fontSize": "20px", "fontWeight": "bold"})
            ], className="stat-box"),

            html.Div([
                html.H4("Giá Giảm Trung Bình"),
                html.P(id="avg_discount_price", style={"fontSize": "20px", "fontWeight": "bold"})
            ], className="stat-box"),

            html.Div([
                html.H4("Số Lượng Đánh Giá Trung Bình"),
                html.P(id="avg_no_of_ratings", style={"fontSize": "20px", "fontWeight": "bold"})
            ], className="stat-box"),
        ], className="stats-row", style={"display": "flex", "justifyContent": "space-around", "marginBottom": "30px"})
    ], style={"padding": "20px"}),

    # Bộ lọc
    html.Div([
        html.Div([
            html.Label("Lọc theo Loại Chính"),
            dcc.Dropdown(
                id="main_category_filter",
                options=[{"label": cat, "value": cat} for cat in df["main_category"].unique()],
                value=None,
                placeholder="Chọn Loại Chính",
                style={"width": "100%"}
            )
        ], style={"width": "30%", "display": "inline-block", "paddingRight": "10px"}),

        html.Div([
            html.Label("Lọc theo Loại Con"),
            dcc.Dropdown(
                id="sub_category_filter",
                options=[{"label": subcat, "value": subcat} for subcat in df["sub_category"].unique()],
                value=None,
                placeholder="Chọn Loại Con",
                style={"width": "100%"}
            )
        ], style={"width": "30%", "display": "inline-block", "paddingRight": "10px"}),

        html.Div([
            html.Label("Chọn Biểu Đồ Hiển Thị"),
            dcc.Dropdown(
                id="chart_selector",
                options=[
                    {"label": "Phân phối đánh giá (Ratings)", "value": "ratings_distribution"},
                    {"label": "Giá giảm vs Giá thực (Scatter)", "value": "price_comparison"},
                    {"label": "Top 10 Sản phẩm có số lượng đánh giá cao nhất", "value": "top10_products"},
                    {"label": "Phân bố sản phẩm theo Loại Con (Treemap)", "value": "treemap_subcategories"},
                    {"label": "Phân tích tỷ lệ giảm giá (Box Plot)", "value": "discount_analysis"}
                ],
                value="ratings_distribution",
                placeholder="Chọn Biểu Đồ",
                style={"width": "100%"}
            )
        ], style={"width": "30%", "display": "inline-block"}),
    ], className="filters-row", style={"marginBottom": "30px"}),

    # Biểu đồ
    html.Div(
        dcc.Graph(id="dynamic_chart", style={"height": "70vh", "margin": "0 auto"}), 
        style={"maxWidth": "1200px", "margin": "0 auto"}
    ),

    # Hiển thị thông báo khi không có dữ liệu
    html.Div(
        id="no_data_message", 
        style={"textAlign": "center", "color": "red", "fontSize": "18px", "marginTop": "20px"}
    )
], style={"padding": "20px"})  # Thêm padding để tạo khoảng trống xung quanh màn hình


# Callback để cập nhật các giá trị trong dropdown "Loại Con" dựa vào "Loại Chính"
@app.callback(
    Output("sub_category_filter", "options"),
    Input("main_category_filter", "value")
)
def update_sub_category_options(selected_main_category):
    if selected_main_category:
        # Lọc các giá trị "Loại Con" phù hợp với "Loại Chính"
        filtered_sub_categories = df[df["main_category"] == selected_main_category]["sub_category"].unique()
        return [{"label": subcat, "value": subcat} for subcat in filtered_sub_categories]
    else:
        # Nếu không chọn "Loại Chính", hiển thị tất cả các giá trị "Loại Con"
        return [{"label": subcat, "value": subcat} for subcat in df["sub_category"].unique()]


# Callback để hiển thị các giá trị cơ bản trong Header
@app.callback(
    [Output("total_products", "children"),
     Output("avg_ratings", "children"),
     Output("avg_discount_price", "children"),
     Output("avg_no_of_ratings", "children")],
    [Input("main_category_filter", "value"),
     Input("sub_category_filter", "value")]
)
def update_header_values(main_category, sub_category):
    # Lọc dữ liệu theo các bộ lọc
    filtered_df = df.copy()
    if main_category:
        filtered_df = filtered_df[filtered_df["main_category"] == main_category]
    if sub_category:
        filtered_df = filtered_df[filtered_df["sub_category"] == sub_category]

    # Tính toán giá trị cơ bản
    total_products = len(filtered_df)
    avg_ratings = filtered_df["ratings"].mean() if not filtered_df.empty else 0
    avg_discount_price = filtered_df["discount_price"].mean() if not filtered_df.empty else 0
    avg_no_of_ratings = filtered_df["no_of_ratings"].mean() if not filtered_df.empty else 0

    # Trả về các giá trị
    return (
        f"{total_products:,}",
        f"{avg_ratings:.2f}",
        f"${avg_discount_price:,.2f}",
        f"{avg_no_of_ratings:,.0f}"
    )


# Callback để lọc dữ liệu và cập nhật biểu đồ
@app.callback(
    [Output("dynamic_chart", "figure"), Output("no_data_message", "children")],
    [Input("main_category_filter", "value"),
     Input("sub_category_filter", "value"),
     Input("chart_selector", "value")]
)
def update_chart(main_category, sub_category, chart_type):
    # Lọc dữ liệu theo các bộ lọc
    filtered_df = df.copy()
    if main_category:
        filtered_df = filtered_df[filtered_df["main_category"] == main_category]
    if sub_category:
        filtered_df = filtered_df[filtered_df["sub_category"] == sub_category]

    # Nếu không có dữ liệu sau khi lọc
    if filtered_df.empty:
        return {}, "Không có dữ liệu phù hợp!"

    # Biểu đồ 1: Phân phối đánh giá
    if chart_type == "ratings_distribution":
        fig = px.histogram(
            filtered_df, x='ratings', nbins=10,
            title="Phân phối Đánh Giá",
            labels={"ratings": "Đánh Giá"},
            color_discrete_sequence=["#636EFA"]
        )
    # Biểu đồ 2: Scatter Giá giảm vs Giá thực
    elif chart_type == "price_comparison":
        fig = px.scatter(
            filtered_df, x='discount_price', y='actual_price',
            title="Giá Giảm vs Giá Thực",
            labels={"discount_price": "Giá Giảm", "actual_price": "Giá Thực"},
            color_discrete_sequence=["#EF553B"]
        )
    # Biểu đồ 3: Top 10 sản phẩm
    elif chart_type == "top10_products":
        top10 = filtered_df.nlargest(10, "no_of_ratings")
        top10["short_name"] = top10["name"].apply(lambda x: x[:20] + "..." if len(x) > 20 else x)
        fig = px.bar(
            top10, x="no_of_ratings", y="short_name",
            orientation="h",
            title="Top 10 Sản phẩm có số lượng Đánh Giá cao nhất",
            labels={"short_name": "Tên Sản Phẩm", "no_of_ratings": "Số lượng Đánh Giá"},
            color="no_of_ratings",
            hover_data={"name": True},  # Hiển thị tên đầy đủ khi hover
            color_continuous_scale="Viridis"
        )
    # Biểu đồ 4: Treemap phân bố sản phẩm theo loại con
    elif chart_type == "treemap_subcategories":
        fig = px.treemap(
            filtered_df, path=["sub_category", "name"], values="no_of_ratings",
            title="Phân bố Sản Phẩm theo Loại Con",
            color="no_of_ratings",
            color_continuous_scale="RdBu"
        )
    # Biểu đồ 5: Phân tích tỷ lệ giảm giá
    elif chart_type == "discount_analysis":
        fig = px.box(
            filtered_df, x="main_category", y="discount_percentage",
            title="Phân tích Tỷ Lệ Giảm Giá theo Loại Chính",
            labels={"main_category": "Loại Chính", "discount_percentage": "Tỷ Lệ Giảm Giá (%)"},
            color="main_category"
        )
    else:
        fig = px.scatter(title="Không có dữ liệu để hiển thị!")

    # Trả về biểu đồ và thông báo trống
    return fig, ""


# Chạy ứng dụng
if __name__ == '__main__':
    app.run_server(debug=True)
