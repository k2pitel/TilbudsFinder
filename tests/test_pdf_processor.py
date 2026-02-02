"""Unit tests for PDF extraction functionality."""

import unittest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_processor import PDFExtractor


class TestPDFExtractor(unittest.TestCase):
    """Test cases for PDF extraction."""
    
    def test_extractor_initialization(self):
        """Test that PDFExtractor can be initialized."""
        extractor = PDFExtractor('dummy_path.pdf')
        self.assertEqual(extractor.pdf_path, 'dummy_path.pdf')
    
    def test_extract_text_method_exists(self):
        """Test that extract_text method exists."""
        extractor = PDFExtractor('dummy_path.pdf')
        self.assertTrue(hasattr(extractor, 'extract_text'))
        self.assertTrue(callable(extractor.extract_text))


if __name__ == '__main__':
    unittest.main()
