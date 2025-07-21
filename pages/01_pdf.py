import streamlit as st
from PIL import Image
import fitz  # PyMuPDF

def convert_png_to_pdf(image_file):
    """PNG 파일을 PDF로 변환합니다."""
    try:
        image = Image.open(image_file).convert("RGB")
        pdf_path = "output.pdf"
        image.save(pdf_path)
        return pdf_path
    except Exception as e:
        st.error(f"PNG를 PDF로 변환하는 중 오류 발생: {e}")
        return None

def convert_pdf_to_png(pdf_file):
    """PDF 파일을 PNG 이미지로 변환합니다."""
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        png_paths = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            output_png_path = f"output_page_{page_num + 1}.png"
            pix.save(output_png_path)
            png_paths.append(output_png_path)
        return png_paths
    except Exception as e:
        st.error(f"PDF를 PNG로 변환하는 중 오류 발생: {e}")
        return None

st.set_page_config(layout="centered", page_title="이미지-PDF 변환기")

st.title("📄 이미지 ↔️ PDF 변환기")

st.markdown("""
이 앱은 PNG 이미지를 PDF로 변환하거나, PDF 파일을 PNG 이미지로 변환해줍니다.
파일을 업로드하고 원하는 변환 옵션을 선택하세요.
""")

# 변환 모드 선택
conversion_mode = st.radio(
    "어떤 변환을 원하시나요?",
    ("PNG → PDF", "PDF → PNG"),
    index=0
)

uploaded_file = st.file_uploader(
    f"{conversion_mode} 변환을 위해 파일을 업로드하세요.",
    type=["png"] if conversion_mode == "PNG → PDF" else ["pdf"]
)

if uploaded_file is not None:
    if conversion_mode == "PNG → PDF":
        st.subheader("PNG를 PDF로 변환")
        if st.button("PDF로 변환하기"):
            with st.spinner("PDF 변환 중..."):
                output_pdf = convert_png_to_pdf(uploaded_file)
                if output_pdf:
                    st.success("PNG가 PDF로 성공적으로 변환되었습니다!")
                    with open(output_pdf, "rb") as f:
                        st.download_button(
                            label="PDF 다운로드",
                            data=f.read(),
                            file_name="converted_image.pdf",
                            mime="application/pdf"
                        )
    elif conversion_mode == "PDF → PNG":
        st.subheader("PDF를 PNG로 변환")
        if st.button("PNG로 변환하기"):
            with st.spinner("PNG 변환 중..."):
                output_pngs = convert_pdf_to_png(uploaded_file)
                if output_pngs:
                    st.success("PDF가 PNG로 성공적으로 변환되었습니다!")
                    for i, png_path in enumerate(output_pngs):
                        with open(png_path, "rb") as f:
                            st.download_button(
                                label=f"PNG 이미지 다운로드 (페이지 {i+1})",
                                data=f.read(),
                                file_name=f"converted_page_{i+1}.png",
                                mime="image/png",
                                key=f"png_download_{i}"
                            )
