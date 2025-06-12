import os
from PIL import Image
import pytesseract
from pypdf import PdfReader
from pdf2image import convert_from_path
from typing import List, Dict, Any

# --- Configuration ---
# You might need to install Tesseract OCR on your system
# and Poppler for pdf2image to work.
#
# For Windows:
# 1. Install Tesseract: https://github.com/tesseract-ocr/tesseract
# 2. Install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/
#    - Add the 'bin' folder from the Poppler installation to your system's PATH.
#
# For macOS (using Homebrew):
# brew install tesseract
# brew install poppler
#
# For Linux (using apt):
# sudo apt-get install tesseract-ocr
# sudo apt-get install poppler-utils

def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 100) -> List[str]:
    """Splits text into smaller chunks."""
    if not text:
        return []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

def extract_text_from_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text from a PDF, using OCR for scanned pages, and returns it in chunks.
    Each chunk includes metadata for citations.
    """
    document_chunks = []
    reader = PdfReader(file_path)
    
    for page_num, page in enumerate(reader.pages):
        page_content = ""
        # First, try to extract text directly
        extracted_text = page.extract_text()
        
        # If direct extraction yields little or no text, assume it's a scanned image
        if not extracted_text or len(extracted_text.strip()) < 100:
            try:
                # Convert the PDF page to an image
                images = convert_from_path(file_path, first_page=page_num + 1, last_page=page_num + 1)
                if images:
                    # Perform OCR on the image
                    page_content = pytesseract.image_to_string(images[0])
            except Exception as e:
                print(f"OCR failed on page {page_num + 1} of {os.path.basename(file_path)}: {e}")
                page_content = "" # Continue if OCR fails on one page
        else:
            page_content = extracted_text
            
        # Split the page content into smaller chunks
        text_chunks = chunk_text(page_content)
        
        for i, chunk in enumerate(text_chunks):
            document_chunks.append({
                "content": chunk,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": page_num + 1,
                    "chunk": i
                }
            })
            
    return document_chunks

def extract_text_from_image(file_path: str) -> List[Dict[str, Any]]:
    """Extracts text from an image and returns it in chunks."""
    text = pytesseract.image_to_string(Image.open(file_path))
    text_chunks = chunk_text(text)
    
    return [{
        "content": chunk,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1,
            "chunk": i
        }
    } for i, chunk in enumerate(text_chunks)]

def extract_text_from_txt(file_path: str) -> List[Dict[str, Any]]:
    """Extracts text from a .txt file and returns it in chunks."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    text_chunks = chunk_text(text)
    
    return [{
        "content": chunk,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1,
            "chunk": i
        }
    } for i, chunk in enumerate(text_chunks)]

def extract_chunks_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    A wrapper function that calls the appropriate extractor based on file extension.
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['.png', '.jpg', '.jpeg', '.jjpg', '.tiff', '.bmp']:
        return extract_text_from_image(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    else:
        print(f"Unsupported file type: {file_extension}")
        return []