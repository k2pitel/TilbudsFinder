"""Unit tests for database models."""

import unittest
import os
import sys
from datetime import datetime, date

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import Market, Offer


class TestDatabaseModels(unittest.TestCase):
    """Test cases for database models."""
    
    def test_market_creation(self):
        """Test that Market model can be instantiated."""
        market = Market(name='Test Market')
        self.assertEqual(market.name, 'Test Market')
    
    def test_market_repr(self):
        """Test Market string representation."""
        market = Market(name='Test Market')
        self.assertIn('Test Market', repr(market))
    
    def test_offer_creation(self):
        """Test that Offer model can be instantiated."""
        offer = Offer(
            market_id=1,
            product_name='Test Product',
            price=10.50,
            unit='kg'
        )
        self.assertEqual(offer.product_name, 'Test Product')
        self.assertEqual(offer.price, 10.50)
        self.assertEqual(offer.unit, 'kg')
    
    def test_offer_repr(self):
        """Test Offer string representation."""
        offer = Offer(
            market_id=1,
            product_name='Test Product',
            price=10.50
        )
        self.assertIn('Test Product', repr(offer))


if __name__ == '__main__':
    unittest.main()
