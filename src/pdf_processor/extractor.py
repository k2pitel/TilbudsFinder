"""PDF extraction module for processing supermarket flyers."""

import pdfplumber
import PyPDF2
from typing import Optional


class PDFExtractor:
    """Extracts text from PDF files."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = pdf_path
    
    def extract_text_pdfplumber(self) -> str:
        """
        Extract text using pdfplumber (better for complex layouts).
        
        Returns:
            Extracted text as string
        """
        text = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n'.join(text)
        except Exception as e:
            print(f"Error extracting with pdfplumber: {e}")
            return ""
    
    def extract_text_pypdf2(self) -> str:
        """
        Extract text using PyPDF2 (fallback method).
        
        Returns:
            Extracted text as string
        """
        text = []
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n'.join(text)
        except Exception as e:
            print(f"Error extracting with PyPDF2: {e}")
            return ""
    
    def extract_text(self) -> str:
        """
        Extract text from PDF using the best available method.
        
        Returns:
            Extracted text as string
        """
        # Try pdfplumber first (better results)
        text = self.extract_text_pdfplumber()
        
        # Fallback to PyPDF2 if pdfplumber fails
        if not text or len(text.strip()) < 50:
            text = self.extract_text_pypdf2()
        
        return text


def extract_pdf_text(pdf_path: str) -> str:
    """
    Convenience function to extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as string
    """
    extractor = PDFExtractor(pdf_path)
    return extractor.extract_text()
