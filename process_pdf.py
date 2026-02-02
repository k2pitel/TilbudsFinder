"""Script to process PDF files and extract offers into the database."""

import sys
import os
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_processor import extract_pdf_text
from nlp_processor import extract_offers
from database import db, Market, Offer, init_db
from web_interface.app import create_app


def process_pdf_file(pdf_path: str, market_name: str):
    """
    Process a PDF file and extract offers.
    
    Args:
        pdf_path: Path to the PDF file
        market_name: Name of the market (e.g., 'Bilka', 'Rema 1000')
    """
    # Create Flask app for database access
    app = create_app()
    
    with app.app_context():
        print(f"Processing PDF: {pdf_path}")
        print(f"Market: {market_name}")
        
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_pdf_text(pdf_path)
        
        if not text:
            print("Error: Could not extract text from PDF")
            return
        
        print(f"Extracted {len(text)} characters of text")
        
        # Extract offers from text
        print("Extracting offers from text...")
        offers_data = extract_offers(text, market_name)
        print(f"Found {len(offers_data)} potential offers")
        
        # Get or create market
        market = Market.query.filter_by(name=market_name).first()
        if not market:
            print(f"Creating new market: {market_name}")
            market = Market(name=market_name)
            db.session.add(market)
            db.session.commit()
        
        # Save offers to database
        print("Saving offers to database...")
        saved_count = 0
        for offer_data in offers_data:
            offer = Offer(
                market_id=market.id,
                product_name=offer_data['product_name'],
                price=offer_data['price'],
                unit=offer_data.get('unit'),
                valid_from=offer_data.get('valid_from'),
                valid_to=offer_data.get('valid_to')
            )
            db.session.add(offer)
            saved_count += 1
        
        db.session.commit()
        print(f"Successfully saved {saved_count} offers to database")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Process PDF files and extract offers')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('market_name', help='Name of the market (e.g., Bilka, Rema 1000)')
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)
    
    # Process the PDF
    try:
        process_pdf_file(args.pdf_path, args.market_name)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
