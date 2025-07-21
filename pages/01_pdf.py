import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import os

# 이미지를 PDF로 변환하는 함수 (PNG, JPG 지원)
def convert_image_to_pdf(image_file):
    """
    이미지 파일 (PNG, JPG)을 PDF로 변환합니다.
    Args:
        image_file: Streamlit의 uploaded_file 객체 (PNG 또는 JPG 이미지).
    Returns:
        변환된 PDF 파일의 경로 또는 None (오류 발생 시).
    """
    try:
        # PIL을 사용하여 이미지를 열고 RGB 모드로 변환 (투명도 및 색상 모드 문제 방지)
        image = Image.open(image_file).convert("RGB")
        # 임시 PDF 파일 경로 설정
        pdf_path = "output.pdf"
        # 이미지를 PDF로 저장
        image.save(pdf_path)
        return pdf_path
    except Exception as e:
        st.error(f"이미지를 PDF로 변환하는 중 오류 발생: {e}")
        return None

# PDF 파일을 PNG 이미지로 변환하는 함수
def convert_pdf_to_png(pdf_file):
    """
    PDF 파일을 PNG 이미지로 변환합니다.
    Args:
        pdf_file: Streamlit의 uploaded_file 객체 (PDF 파일).
    Returns:
        변환된 PNG 이미지 파일들의 경로 리스트 또는 None (오류 발생 시).
    """
    try:
        # PyMuPDF를 사용하여 PDF 문서 열기
        # file.read()를 사용하여 BytesIO 객체로 전달하여 메모리에서 처리
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        png_paths = []
        # PDF의 각 페이지를 순회하며 PNG로 변환
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # 페이지를 픽셀맵으로 렌더링 (높은 해상도를 위해 scale 값 조정 가능)
            pix = page.get_pixmap()
            # 임시 PNG 파일 경로 설정
            output_png_path = f"output_page_{page_num + 1}.png"
            # 픽셀맵을 PNG로 저장
            pix.save(output_png_path)
            png_paths.append(output_png_path)
        return png_paths
    except Exception as e:
        st.error(f"PDF를 PNG로 변환하는 중 오류 발생: {e}")
        return None

# Streamlit 페이지 설정
st.set_page_config(layout="centered", page_title="이미지-PDF 변환기")

# 웹 앱의 제목
st.title("📄 이미지 ↔️ PDF 변환기")

# 앱 설명
st.markdown("""
이 앱은 **PNG/JPG 이미지를 PDF로 변환**하거나, **PDF 파일을 PNG 이미지로 변환**해줍니다.
파일을 업로드하고 원하는 변환 옵션을 선택하세요.
""")

# 변환 모드 선택 (라디오 버튼)
conversion_mode = st.radio(
    "어떤 변환을 원하시나요?",
    ("이미지 → PDF", "PDF → 이미지"), # 텍스트 변경
    index=0 # 기본 선택은 이미지 → PDF
)

# 파일 업로더
# 선택된 변환 모드에 따라 허용되는 파일 타입 변경
if conversion_mode == "이미지 → PDF":
    uploaded_file = st.file_uploader(
        "PNG 또는 JPG 파일을 업로드하세요.",
        type=["png", "jpg", "jpeg"] # JPG/JPEG 추가
    )
else: # PDF → 이미지
    uploaded_file = st.file_uploader(
        "PDF 파일을 업로드하세요.",
        type=["pdf"]
    )


# 파일이 업로드되었을 때만 변환 로직 실행
if uploaded_file is not None:
    if conversion_mode == "이미지 → PDF":
        st.subheader("이미지를 PDF로 변환")
        # 변환 버튼
        if st.button("PDF로 변환하기"):
            with st.spinner("PDF 변환 중... 잠시만 기다려 주세요."):
                output_pdf = convert_image_to_pdf(uploaded_file)
                if output_pdf:
                    st.success("이미지가 PDF로 성공적으로 변환되었습니다!")
                    # 변환된 PDF 파일을 다운로드할 수 있도록 버튼 제공
                    with open(output_pdf, "rb") as f:
                        st.download_button(
                            label="PDF 다운로드",
                            data=f.read(),
                            file_name="converted_image.pdf",
                            mime="application/pdf"
                        )
                    # 임시 파일 삭제
                    os.remove(output_pdf)
    elif conversion_mode == "PDF → 이미지":
        st.subheader("PDF를 이미지로 변환")
        # 변환 버튼
        if st.button("이미지로 변환하기"):
            with st.spinner("이미지 변환 중... 잠시만 기다려 주세요."):
                output_pngs = convert_pdf_to_png(uploaded_file)
                if output_pngs:
                    st.success("PDF가 이미지로 성공적으로 변환되었습니다!")
                    # 변환된 각 PNG 이미지를 다운로드할 수 있도록 버튼 제공
                    for i, png_path in enumerate(output_pngs):
                        with open(png_path, "rb") as f:
                            st.download_button(
                                label=f"PNG 이미지 다운로드 (페이지 {i+1})",
                                data=f.read(),
                                file_name=f"converted_page_{i+1}.png",
                                mime="image/png",
                                key=f"png_download_{i}" # 고유한 키 필요
                            )
                        # 임시 파일 삭제
                        os.remove(png_path)

# 푸터 (선택 사항)
st.markdown("---")
st.markdown("Made with ❤️ by Streamlit")
