import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Cấu hình trang web
st.set_page_config(page_title="Quản lý điểm sinh viên", page_icon="📚", layout="wide")
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng xem điểm, xếp loại và thống kê kết quả học tập.")

# Dữ liệu mẫu: thay bằng thông tin thật trước khi nộp bài.
du_lieu = {
    "Họ và tên": [
        "Nguyễn Minh Anh", "Trần Gia Bảo", "Lê Hoàng Nam",
        "Phạm Ngọc Hà", "Võ Tuấn Kiệt", "Đặng Thu Trang",
        "Bùi Quốc Huy", "Đỗ Khánh Linh", "Hồ Đức Thịnh",
        "Phan Mỹ Duyên"
    ],
    "Chuyên cần": [9.0, 8.0, 7.5, 9.5, 6.5, 8.5, 7.0, 10.0, 6.0, 9.0],
    "Giữa kỳ":    [8.5, 7.0, 6.5, 9.0, 5.5, 8.0, 7.5, 9.5, 6.0, 8.5],
    "Cuối kỳ":    [9.0, 7.5, 6.0, 9.5, 5.0, 8.5, 8.0, 9.0, 4.5, 9.0]
}
df = pd.DataFrame(du_lieu)

# Tính điểm tổng kết theo đúng công thức của đề.
df["Tong_ket"] = (
    df["Chuyên cần"] * 0.2
    + df["Giữa kỳ"] * 0.3
    + df["Cuối kỳ"] * 0.5
).round(2)

# Xếp loại sinh viên.
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Thống kê tổng quan.
diem_trung_binh = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sinh_vien_dat = int((df["Tong_ket"] >= 5).sum())

cot1, cot2, cot3, cot4 = st.columns(4)
cot1.metric("Điểm trung bình lớp", f"{diem_trung_binh:.2f}")
cot2.metric("Số sinh viên đạt", f"{so_sinh_vien_dat}/{len(df)}")
cot3.metric("Điểm cao nhất", f"{sv_cao_nhat['Tong_ket']:.2f}")
cot4.metric("Điểm thấp nhất", f"{sv_thap_nhat['Tong_ket']:.2f}")

st.subheader("1. Bảng điểm sinh viên")
bang_hien_thi = df.rename(columns={
    "Chuyên cần": "Chuyên cần",
    "Giữa kỳ": "Giữa kỳ",
    "Cuối kỳ": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})
st.dataframe(bang_hien_thi, use_container_width=True, hide_index=True)

st.subheader("2. Sinh viên có điểm cao nhất và thấp nhất")
trai, phai = st.columns(2)
trai.success(f"**Cao nhất:** {sv_cao_nhat['Họ và tên']} — {sv_cao_nhat['Tong_ket']:.2f} điểm")
phai.info(f"**Thấp nhất:** {sv_thap_nhat['Họ và tên']} — {sv_thap_nhat['Tong_ket']:.2f} điểm")

st.subheader("3. Tra cứu điểm theo sinh viên")
ten_duoc_chon = st.selectbox("Chọn sinh viên:", df["Họ và tên"].tolist())
sv = df[df["Họ và tên"] == ten_duoc_chon].iloc[0]
a, b, c, d, e = st.columns(5)
a.metric("Chuyên cần", f"{sv['Chuyên cần']:.1f}")
b.metric("Giữa kỳ", f"{sv['Giữa kỳ']:.1f}")
c.metric("Cuối kỳ", f"{sv['Cuối kỳ']:.1f}")
d.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
e.metric("Xếp loại", sv["Xep_loai"])

st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Họ và tên"], df["Tong_ket"])
ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)
for nhan in ax.get_xticklabels():
    nhan.set_ha("right")
ax.grid(axis="y", linestyle="--", alpha=0.35)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Điền thông tin thật của người tạo ứng dụng tại đây.
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:12px; color:gray;'>"
    "Người tạo: [HỌ VÀ TÊN CỦA BẠN] | MSSV: [MÃ SỐ SINH VIÊN]"
    "</div>",
    unsafe_allow_html=True
)
