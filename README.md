# 📝 AI-Based Handwritten Notes to Text Converter

Convert handwritten notes (English & Hindi) to editable text using OCR.  
Supports multiple images, PDF/Word export, and more.

## Features

- 📷 Upload multiple images (JPG, PNG)
- 🖋️ Supports English handwritten notes (for now)
- 📝 Edit extracted text before export
- 📤 Export as TXT, DOCX, or PDF
- 🕑 Keeps conversion history
- 💡 OCR tips for best results

## Getting Started

### Prerequisites

- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (with `eng` and `hin` language data)
- [wkhtmltopdf](https://wkhtmltopdf.org/) (for PDF export, optional)

### Installation

```sh
pip install streamlit pytesseract pillow opencv-python python-docx pdfkit numpy
```

### Usage

1. Start the app:
    ```sh
    streamlit run c.py
    ```
2. Open the provided local URL in your browser.
3. Upload handwritten note images and convert!

### Tesseract Setup

- Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
- Make sure `hin.traineddata` is in your `tessdata` folder for Hindi support.

### PDF Export

- Install [wkhtmltopdf](https://wkhtmltopdf.org/) and update the path in the code if needed.

## Folder Structure

```
handwritten_notes_converter/
│
├── c.py
├── README.md
├── requirements.txt
└── ...
```

## License

MIT License

---

**Made with ❤️ using Streamlit and Tesseract OCR**
