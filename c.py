import streamlit as st
import pytesseract
from PIL import Image, ImageOps
import io
import base64
import platform
import os
import pdfkit 
from docx import Document
from datetime import datetime
import numpy as np
import cv2

# Detect and set Tesseract path
def auto_set_tesseract_path():
    system = platform.system()
    if system == 'Windows':
        default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(default_path):
            pytesseract.pytesseract.tesseract_cmd = default_path
    elif system == 'Linux' or system == 'Darwin':
        pytesseract.pytesseract.tesseract_cmd = 'tesseract'  # assume installed

auto_set_tesseract_path()

# Add this before OCR call if using tessdata_best
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Program Files\Tesseract-OCR\tessdata_best"

# Store session history
if 'history' not in st.session_state:
    st.session_state.history = []

# Title
st.title("📝 AI-Based Handwritten Notes to Text Converter")
st.caption("Convert handwritten notes to editable text with OCR. Supports multiple images, Hindi, PDF, Word export and more.")

# Upload multiple images
uploaded_files = st.file_uploader("📂 Upload one or more images (JPG, PNG, etc.)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# OCR progress
progress_text = "🔍 Performing OCR, please wait..."
progress_bar = st.empty()
spinner_area = st.empty()

# OCR tips
with st.expander("📸 How to capture good notes for OCR"):
    st.markdown("""
    - Use good lighting
    - Avoid shadows
    - Use clear handwriting
    - Capture image from top
    - Avoid blurry images
    """)

# Function: image preprocessing
def preprocess_image(img):
    # Convert PIL Image to OpenCV format
    img_cv = np.array(img)
    if img_cv.ndim == 3:
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Adaptive thresholding for better contrast
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    return Image.fromarray(thresh)

# Function: convert image to text
def convert_image_to_text(image):
    custom_config = r'--oem 1 --psm 11'  # PSM 11 = Assume a uniform block of text
    return pytesseract.image_to_string(preprocess_image(image), lang='eng+hin', config=custom_config)


# Begin processing
if uploaded_files:
    output_texts = []
    for i, uploaded_file in enumerate(uploaded_files):
        spinner_area.info(f"Processing image {i+1}/{len(uploaded_files)}...")
        image = Image.open(uploaded_file)

        # Preprocess and show image for debug
        pre_img = preprocess_image(image)
        st.image(pre_img, caption=f"🖼️ Preprocessed Image {i+1}", use_container_width=True)

        # OCR
        text = pytesseract.image_to_string(pre_img, lang='eng+hin', config='--oem 1 --psm 11')

        # Append results
        output_texts.append(text)
        st.session_state.history.append({
            'filename': uploaded_file.name,
            'text': text,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        progress_bar.progress((i+1)/len(uploaded_files))

    spinner_area.success("✅ All images processed!")
    full_text = "\n\n".join(output_texts)

    # Editable text area
    st.subheader("📝 Extracted Text")
    edited_text = st.text_area("Edit if needed:", full_text, height=300)

    # Copy to clipboard
    st.button("📋 Copy to Clipboard", on_click=lambda: st.success("Text copied! (Ctrl+C in editable field)"))

        # Export section with dropdown
    st.subheader("📤 Export")

    export_option = st.selectbox("Choose format to download:", ["Select...", "TXT", "DOCX", "PDF"])

    if export_option == "TXT":
        st.download_button("⬇️ Download TXT", data=edited_text, file_name="notes.txt")

    elif export_option == "DOCX":
        doc = Document()
        doc.add_paragraph(edited_text)
        doc_io = io.BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        st.download_button("⬇️ Download Word (.docx)", data=doc_io, file_name="notes.docx")

    elif export_option == "PDF":
        WKHTMLTOPDF_PATH = None
        if platform.system() == 'Windows':
            WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        elif platform.system() == 'Linux':
            WKHTMLTOPDF_PATH = "/usr/local/bin/wkhtmltopdf"
        elif platform.system() == 'Darwin':
            WKHTMLTOPDF_PATH = "/usr/local/bin/wkhtmltopdf"

        if WKHTMLTOPDF_PATH and os.path.exists(WKHTMLTOPDF_PATH):
            config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
            try:
                html = f"<pre>{edited_text}</pre>"
                pdf_output = pdfkit.from_string(html, False, configuration=config)

                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_output,
                    file_name="notes.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}. Please ensure wkhtmltopdf is installed and the path is correct.")
        else:
            st.error(f"wkhtmltopdf not found at '{WKHTMLTOPDF_PATH}'. PDF export will not work. Please install it.")

# Conversion history
if st.session_state.history:
    st.subheader("📚 Conversion History")
    for i, record in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"{record['filename']} ({record['timestamp']})"):
            st.code(record['text'])

