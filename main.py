import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Nguyễn Hoàng Linh 2121050097
# Phạm Đức Long 2121050067

# Đọc dữ liệu
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")

# Tóm tắt về tập dữ liệu
st.write("### Tóm tắt về dữ liệu:")
st.write(movies_data.info())

# Loại bỏ các cột có dữ liệu bị thiếu
movies_data = movies_data.dropna()

# Tiêu đề
st.title("Dự Án Trực Quan Hóa Dữ Liệu Phim IMDb")

# Các bộ lọc lựa chọn thể loại phim (cho phép chọn nhiều thể loại)
st.sidebar.header("Lọc Dữ Liệu Phim")
selected_genres = st.sidebar.multiselect("Chọn thể loại phim", movies_data['genre'].unique())
selected_year = st.sidebar.slider("Chọn năm phát hành", int(movies_data['year'].min()), int(movies_data['year'].max()), (int(movies_data['year'].min()), int(movies_data['year'].max())))

# Lọc dữ liệu theo thể loại và năm
filtered_data = movies_data[(movies_data['genre'].isin(selected_genres)) & 
                            (movies_data['year'] >= selected_year[0]) & 
                            (movies_data['year'] <= selected_year[1])]

# Tạo biểu đồ cột trung bình ngân sách theo thể loại
avg_budget = filtered_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()

# Vẽ biểu đồ
fig = plt.figure(figsize=(10, 6))
plt.bar(avg_budget['genre'], avg_budget['budget'], color='maroon', width=0.4)  # Giảm chiều rộng cột để tránh bị tràn
plt.xlabel('Thể loại phim')
plt.ylabel('Ngân sách (tính bằng USD)')
plt.title(f'Ngân sách trung bình của các phim thuộc thể loại {", ".join(selected_genres)}')

# Biểu đồ 1: Số lượng phim theo năm
st.write("### Biểu đồ Số lượng phim theo năm:")
count_by_year = filtered_data['year'].value_counts().sort_index()
fig1 = plt.figure(figsize=(10, 5))
plt.plot(count_by_year.index, count_by_year.values, marker='o', linestyle='-', color='teal')
plt.xlabel("Năm phát hành")
plt.ylabel("Số lượng phim")
plt.title("Số lượng phim phát hành theo từng năm")
st.pyplot(fig1)

# Biểu đồ 2: Điểm IMDb trung bình theo thể loại
st.write("### Biểu đồ Điểm IMDb trung bình theo thể loại:")
avg_rating = filtered_data.groupby('genre')['score'].mean().round(2).reset_index()
fig2 = plt.figure(figsize=(10, 5))
plt.bar(avg_rating['genre'], avg_rating['score'], color='skyblue')
plt.xlabel("Thể loại phim")
plt.ylabel("Điểm IMDb trung bình")
plt.title("Điểm IMDb trung bình theo thể loại")
st.pyplot(fig2)

# Biểu đồ 3: Phân phối điểm IMDb
st.write("### Biểu đồ Phân phối điểm IMDb:")
fig3 = plt.figure(figsize=(10, 5))
plt.hist(filtered_data['score'], bins=20, color='orange', edgecolor='black')
plt.xlabel("Điểm IMDb")
plt.ylabel("Số lượng phim")
plt.title("Phân phối điểm IMDb")
st.pyplot(fig3)

# Hiển thị biểu đồ trên Streamlit
st.pyplot(fig)

# Hiển thị bảng dữ liệu đã lọc
st.write("### Bảng Dữ Liệu Phim Đã Lọc:")
st.write(filtered_data)

# Thêm một số thống kê đơn giản
st.write("### Thống kê về dữ liệu phim:")
st.write(filtered_data.describe())