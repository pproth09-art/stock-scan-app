import streamlit as st
import pandas as pd

st.set_page_config(page_title="StockScan Pro", layout="centered")

st.title("📦 StockScan Auto-Fill")
uploaded_file = st.file_uploader("📸 อัปโหลดรูปใบเสร็จ", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # ข้อมูลจำลอง (ในอนาคตเชื่อมต่อ OCR ได้ที่นี่)
    data = [
        {"รายการ": "แสงโสมกลม", "ขนาด": "0.75 ลิตร", "จำนวน": 1, "หน่วย": "ลัง"},
        {"รายการ": "โซดาร็อค", "ขนาด": "325 ml.", "จำนวน": 2, "หน่วย": "ถาด"}
    ]
    df = pd.DataFrame(data)
    
    search_term = st.text_input("🔍 ค้นหาสินค้า:")
    if search_term:
        res = df[df['รายการ'].str.contains(search_term, case=False)]
        for i, row in res.iterrows():
            st.info(f"{row['รายการ']} | {row['ขนาด']} | จำนวน: {row['จำนวน']} {row['หน่วย']}")
            if st.button(f"คัดลอกเลข {row['จำนวน']}", key=i):
                st.write(f"คัดลอกเลข {row['จำนวน']} แล้ว!") # จำลองการก๊อปปี้
