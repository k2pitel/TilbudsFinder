"""Unit tests for NLP extraction functionality."""

import unittest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nlp_processor import OfferExtractor


class TestOfferExtractor(unittest.TestCase):
    """Test cases for offer extraction."""
    
    def setUp(self):
        """Set up test cases."""
        self.extractor = OfferExtractor()
    
    def test_extractor_initialization(self):
        """Test that OfferExtractor can be initialized."""
        self.assertIsNotNone(self.extractor)
    
    def test_extract_prices_simple(self):
        """Test price extraction with simple format."""
        text = "Mælk 12,50 kr"
        prices = self.extractor.extract_prices(text)
        self.assertGreater(len(prices), 0)
        self.assertEqual(prices[0]['price'], 12.50)
    
    def test_extract_prices_no_decimals(self):
        """Test price extraction without decimals."""
        text = "Brød 25 kr"
        prices = self.extractor.extract_prices(text)
        self.assertGreater(len(prices), 0)
        self.assertEqual(prices[0]['price'], 25.0)
    
    def test_extract_units_kg(self):
        """Test unit extraction for kg."""
        text = "Kartofler 2 kg"
        units = self.extractor.extract_units(text)
        self.assertGreater(len(units), 0)
        self.assertEqual(units[0]['unit'], 'kg')
    
    def test_extract_units_stk(self):
        """Test unit extraction for stk."""
        text = "Æbler 6 stk"
        units = self.extractor.extract_units(text)
        self.assertGreater(len(units), 0)
        self.assertEqual(units[0]['unit'], 'stk')
    
    def test_extract_offers_complete(self):
        """Test complete offer extraction."""
        text = """
        Bilka Tilbudsavis
        Gyldig fra 1. november 2024 til 7. november 2024
        
        Banan 1 kg 12,50 kr
        Mælk 1 l 8 kr
        Brød 1 stk 15,00 kr
        """
        offers = self.extractor.extract_offers_from_text(text, "Bilka")
        self.assertGreater(len(offers), 0)
        
        # Check that offers have required fields
        for offer in offers:
            self.assertIn('product_name', offer)
            self.assertIn('price', offer)
            self.assertIn('market', offer)


if __name__ == '__main__':
    unittest.main()
