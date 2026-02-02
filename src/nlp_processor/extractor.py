"""NLP processor for extracting offer information from text."""

import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
from dateutil import parser as date_parser


class OfferExtractor:
    """Extracts product offers from text using NLP techniques."""
    
    # Danish month names for date parsing
    DANISH_MONTHS = {
        'januar': 'january', 'jan': 'jan',
        'februar': 'february', 'feb': 'feb',
        'marts': 'march', 'mar': 'mar',
        'april': 'april', 'apr': 'apr',
        'maj': 'may', 'may': 'may',
        'juni': 'june', 'jun': 'jun',
        'juli': 'july', 'jul': 'jul',
        'august': 'august', 'aug': 'aug',
        'september': 'september', 'sep': 'sep',
        'oktober': 'october', 'okt': 'oct',
        'november': 'november', 'nov': 'nov',
        'december': 'december', 'dec': 'dec'
    }
    
    # Common Danish units
    UNITS = ['kg', 'g', 'l', 'ml', 'cl', 'dl', 'stk', 'stk.', 'pk', 'pk.', 'bk', 'ps', 'pose']
    
    def __init__(self):
        """Initialize the offer extractor."""
        pass
    
    def extract_prices(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract price patterns from text.
        
        Args:
            text: Input text to search
            
        Returns:
            List of dictionaries containing price information
        """
        prices = []
        
        # Pattern: "XX,XX kr" or "XX kr" or "XX,-"
        price_patterns = [
            r'(\d+)[,.](\d{2})\s*kr',  # 12,50 kr or 12.50 kr
            r'(\d+)\s*kr',              # 12 kr
            r'(\d+)[,.](\d{2})\s*,-',   # 12,50 ,-
            r'(\d+)\s*,-',              # 12 ,-
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    price = float(f"{match.group(1)}.{match.group(2)}")
                else:
                    price = float(match.group(1))
                
                prices.append({
                    'price': price,
                    'position': match.start(),
                    'text': match.group(0)
                })
        
        return prices
    
    def extract_units(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract unit patterns from text.
        
        Args:
            text: Input text to search
            
        Returns:
            List of dictionaries containing unit information
        """
        units = []
        
        # Create pattern from known units
        unit_pattern = r'\b(\d+[,.]?\d*)\s*(' + '|'.join(self.UNITS) + r')\b'
        
        matches = re.finditer(unit_pattern, text, re.IGNORECASE)
        for match in matches:
            units.append({
                'quantity': match.group(1),
                'unit': match.group(2).lower(),
                'position': match.start(),
                'text': match.group(0)
            })
        
        return units
    
    def extract_dates(self, text: str) -> List[datetime]:
        """
        Extract dates from text (Danish format).
        
        Args:
            text: Input text to search
            
        Returns:
            List of datetime objects
        """
        dates = []
        
        # Convert Danish month names to English for parsing
        text_normalized = text.lower()
        for danish, english in self.DANISH_MONTHS.items():
            text_normalized = text_normalized.replace(danish, english)
        
        # Common date patterns
        date_patterns = [
            r'\b(\d{1,2})[./\-](\d{1,2})[./\-](\d{2,4})\b',  # 12/06/2024 or 12-06-24
            r'\b(\d{1,2})\.\s*(\w+)\s*(\d{4})\b',            # 12. juni 2024
            r'\b(\d{1,2})\s+(\w+)\s+(\d{4})\b',              # 12 juni 2024
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text_normalized)
            for match in matches:
                try:
                    date_str = match.group(0)
                    parsed_date = date_parser.parse(date_str, dayfirst=True, fuzzy=True)
                    dates.append(parsed_date)
                except (ValueError, date_parser.ParserError):
                    # Skip dates that cannot be parsed
                    pass
        
        return dates
    
    def extract_offers_from_text(self, text: str, market_name: str) -> List[Dict[str, Any]]:
        """
        Extract complete offer information from text.
        
        Args:
            text: Input text from PDF
            market_name: Name of the market
            
        Returns:
            List of offer dictionaries
        """
        offers = []
        
        # Extract all components
        prices = self.extract_prices(text)
        units = self.extract_units(text)
        dates = self.extract_dates(text)
        
        # Split text into lines for product name extraction
        lines = text.split('\n')
        
        # Find validity period
        valid_from = dates[0] if len(dates) > 0 else None
        valid_to = dates[1] if len(dates) > 1 else None
        
        # Process each price found
        for price_info in prices:
            price_pos = price_info['position']
            
            # Find the line containing this price
            current_pos = 0
            product_line = ""
            
            for line in lines:
                line_end = current_pos + len(line)
                if current_pos <= price_pos <= line_end:
                    product_line = line
                    break
                current_pos = line_end + 1  # +1 for newline
            
            # Extract product name (text before price on the same line)
            product_name = product_line[:product_line.find(price_info['text'])].strip()
            
            # Skip if product name is too short or empty
            if len(product_name) < 3:
                continue
            
            # Find nearest unit
            unit = None
            min_distance = float('inf')
            for unit_info in units:
                distance = abs(unit_info['position'] - price_pos)
                if distance < min_distance and distance < 100:  # Within 100 chars
                    min_distance = distance
                    unit = unit_info['unit']
            
            offer = {
                'market': market_name,
                'product_name': product_name[:255],  # Limit length
                'price': price_info['price'],
                'unit': unit,
                'valid_from': valid_from,
                'valid_to': valid_to
            }
            
            offers.append(offer)
        
        return offers


def extract_offers(text: str, market_name: str) -> List[Dict[str, Any]]:
    """
    Convenience function to extract offers from text.
    
    Args:
        text: Input text from PDF
        market_name: Name of the market
        
    Returns:
        List of offer dictionaries
    """
    extractor = OfferExtractor()
    return extractor.extract_offers_from_text(text, market_name)
