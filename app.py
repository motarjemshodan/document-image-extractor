import os
import zipfile
import shutil
import fitz
import streamlit as st

# تنظیمات صفحه و راست‌چین کردن (RTL) به همراه فونت Vazirmatn
st.set_page_config(page_title="استخراج‌کننده تصاویر", page_icon="🖼️", layout="centered")

st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', Tahoma, sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* اصلاح جهت تراز عناصر در استریم‌لیت */
    .stApp {
        direction: rtl;
    }
    
    /* تنظیمات اختصاصی برای بهبود رندر عناوین */
    h1, h2, h3 {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
    }
    
    /* راست‌چین کردن دکمه‌ها و عناصر آپلودر */
    .uploadedFile {
        text-align: right;
    }
    
    /* استایل‌های بخش فوتر */
    .footer-container {
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #e0e0e0;
        background-color: #f9f9f9;
        border-radius: 10px;
        font-size: 14px;
        color: #333;
    }
    .footer-content {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .footer-logo {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
    }
    .footer-links {
        margin-top: 8px;
        font-size: 13px;
    }
    .footer-links a {
        color: #0066cc;
        text-decoration: none;
        margin-left: 10px;
        margin-right: 10px;
    }
    .footer-links a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🖼️ استخراج‌کننده تصاویر از فایل")
st.write("فایل خود (PDF، Word، EPUB و...) را آپلود کنید تا تمام تصاویر آن یکجا استخراج شوند.")

uploaded_file = st.file_uploader("انتخاب فایل", type=['pdf', 'docx', 'epub', 'zip', 'xlsx', 'pptx'])

if uploaded_file is not None:
    output_dir = "temp_extracted"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = uploaded_file.name
    ext = os.path.splitext(file_path)[1].lower()
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    with st.spinner('در حال استخراج تصاویر...'):
        if ext in ['.docx', '.epub', '.zip', '.xlsx', '.pptx']:
            with zipfile.ZipFile(file_path, 'r') as z:
                for filename in z.namelist():
                    if any(filename.lower().endswith(img_ext) for img_ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif']):
                        z.extract(filename, output_dir)
                        
        elif ext == '.pdf':
            doc = fitz.open(file_path)
            for page_index in range(len(doc)):
                for img_index, img in enumerate(doc.get_page_images(page_index)):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n >= 5:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    pix.save(os.path.join(output_dir, f"page_{page_index+1}_img_{img_index+1}.png"))
        
        shutil.make_archive("extracted_images", 'zip', output_dir)

    st.success("استخراج با موفقیت انجام شد!")
    
    with open("extracted_images.zip", "rb") as fp:
        st.download_button(
            label="دانلود فایل فشرده تصاویر (ZIP)",
            data=fp,
            file_name="extracted_images.zip",
            mime="application/zip"
        )

# اضافه شدن بخش فوتر در انتهای صفحه
st.markdown("""
<hr style="margin-top: 40px; margin-bottom: 20px;">
<div style="text-align: right; font-family: 'Vazirmatn', sans-serif; color: #555; padding: 10px;">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        <img src="https://motarjemshodan.ir/wp-content/uploads/2021/10/cropped-cropped-photo_2021-09-11_13-53-35-50x50.jpg" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">
        <strong>مترجم‌شدن</strong> | نگاهی دور و نزدیک به ترجمه و حرفه‌ی مترجمی.
    </div>
    <div style="margin-top: 10px; font-size: 13px;">
        <strong>ارتباط و آموزش‌ها:</strong> 
        <a href="https://motarjemshodan.ir" target="_blank" style="text-decoration: none; color: #007acc; margin: 0 5px;">وبگاه</a> | 
        <a href="https://t.me/motarjemshodan" target="_blank" style="text-decoration: none; color: #007acc; margin: 0 5px;">کانال تلگرام</a> | 
        <a href="https://t.me/motarjemshodanG" target="_blank" style="text-decoration: none; color: #007acc; margin: 0 5px;">گروه تلگرام</a> | 
        <a href="http://instagram.com/motarjemshodan" target="_blank" style="text-decoration: none; color: #007acc; margin: 0 5px;">اینستاگرام</a> | 
        <a href="https://yaademy.com/topics/4/%D8%AA%D8%B1%D8%AC%D9%85%D9%87" target="_blank" style="text-decoration: none; color: #007acc; margin: 0 5px;">آموزش‌ها</a>
    </div>
</div>
""", unsafe_allow_html=True)
