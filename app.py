import os
import zipfile
import shutil
import fitz
import streamlit as st

st.title("استخراج‌کننده تصاویر از فایل (PDF, Word, EPUB)")
st.write("فایل خود را آپلود کنید تا تمام تصاویر آن یکجا استخراج شوند.")

uploaded_file = st.file_uploader("انتخاب فایل", type=['pdf', 'docx', 'epub', 'zip', 'xlsx', 'pptx'])

if uploaded_file is not None:
    output_dir = "temp_extracted"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = uploaded_file.name
    ext = os.path.splitext(file_path)[1].lower()
    
    # ذخیره موقت فایل آپلود شده
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
        
        # ساخت فایل زیپ خروجی
        shutil.make_archive("extracted_images", 'zip', output_dir)

    st.success("استخراج با موفقیت انجام شد!")
    
    with open("extracted_images.zip", "rb") as fp:
        st.download_button(
            label="دانلود فایل فشرده تصاویر (ZIP)",
            data=fp,
            file_name="extracted_images.zip",
            mime="application/zip"
        )
