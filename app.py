import streamlit as st
import pandas as pd
import os

# Cấu hình tiêu đề trang web
st.set_page_config(page_title="Review Phim Chuẩn", layout="wide")
st.title("🎬 Sàn Đánh Giá Phim (Dành cho người chuẩn bị xem)")

# Tên file lưu trữ dữ liệu đánh giá (tự động tạo ra trong máy)
DATA_FILE = "reviews.csv"

# Tạo dữ liệu mẫu nếu chưa có file
if not os.path.exists(DATA_FILE):
    sample_data = pd.DataFrame([
        {"Phim": "Oppenheimer", "Đạo diễn": "Christopher Nolan", "Người xem": "Minh Anh", "Điểm (1-10)": 9, "Nhận xét": "Phim xuất sắc, âm thanh và diễn xuất đỉnh cao, nên xem bản IMAX."},
        {"Phim": "Oppenheimer", "Đạo diễn": "Christopher Nolan", "Người xem": "Hoàng Nam", "Điểm (1-10)": 8, "Nhận xét": "Hơi nhiều thoại nhưng rất cuốn, cần tập trung khi xem."},
        {"Phim": "Mai", "Đạo diễn": "Trấn Thành", "Người xem": "Thu Hà", "Điểm (1-10)": 8, "Nhận xét": "Cảm động, góc quay đẹp, diễn viên nhập vai tốt."},
        {"Phim": "Avatar 2", "Đạo diễn": "James Cameron", "Người xem": "Tuấn Kiệt", "Điểm (1-10)": 9, "Nhận xét": "Kỹ xảo mãn nhãn, đáng tiền ra rạp."}
    ])
    sample_data.to_csv(DATA_FILE, index=False)

# Đọc dữ liệu từ file
df = pd.read_csv(DATA_FILE)

# --- PHẦN 1: TRA CỨU PHIM ---
st.header("1. Tham khảo đánh giá trước khi xem")
danh_sach_phim = df["Phim"].unique().tolist()
phim_chon = st.selectbox("Chọn bộ phim bạn định xem:", danh_sach_phim)

# Lọc dữ liệu theo phim đã chọn
du_lieu_phim = df[df["Phim"] == phim_chon]
diem_tb = round(du_lieu_phim["Điểm (1-10)"].mean(), 1)
dao_dien = du_lieu_phim["Đạo diễn"].iloc[0]

# Hiển thị chỉ số nhanh
col1, col2, col3 = st.columns(3)
col1.metric("Đạo diễn", dao_dien)
col2.metric("Điểm trung bình", f"{diem_tb} / 10")
col3.metric("Số lượt đánh giá", f"{len(du_lieu_phim)} người")

# Hiển thị danh sách bình luận của người xem trước
st.subheader(f"Đánh giá từ những người đã xem '{phim_chon}':")
for index, row in du_lieu_phim.iterrows():
    with st.chat_message("user"):
        st.write(f"**{row['Người xem']}** — Chấm **{row['Điểm (1-10)']}/10**")
        st.write(row["Nhận xét"])

st.divider()

# --- PHẦN 2: THÊM ĐÁNH GIÁ MỚI ---
st.header("2. Bạn đã xem phim? Hãy để lại đánh giá")
with st.form("review_form", clear_on_submit=True):
    ten_phim_moi = st.text_input("Tên phim (gõ tên phim có sẵn hoặc phim mới):")
    dao_dien_moi = st.text_input("Tên đạo diễn:")
    nguoi_xem = st.text_input("Tên của bạn:")
    diem = st.slider("Chấm điểm:", 1, 10, 8)
    nhan_xet = st.text_area("Cảm nhận của bạn (có đáng xem không?):")
    
    submit = st.form_submit_button("Gửi đánh giá")
    
    if submit:
        if ten_phim_moi and nguoi_xem and nhan_xet:
            new_row = pd.DataFrame([{
                "Phim": ten_phim_moi.strip(),
                "Đạo diễn": dao_dien_moi.strip() if dao_dien_moi else "Chưa rõ",
                "Người xem": nguoi_xem.strip(),
                "Điểm (1-10)": diem,
                "Nhận xét": nhan_xet.strip()
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Đã lưu đánh giá thành công! Hãy tải lại trang để xem.")
            st.rerun()
        else:
            st.error("Vui lòng nhập đầy đủ Tên phim, Tên của bạn và Nhận xét.")
