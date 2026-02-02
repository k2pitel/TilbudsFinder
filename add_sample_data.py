"""Sample script to add test data to the database."""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

# Change to the script's directory
os.chdir(parent_dir)

# Now we can import from src
from src.web_interface.app import app
from src.database import db, Market, Offer


def add_sample_data():
    """Add sample offer data to the database."""
    with app.app_context():
        print("Adding sample data to database...")
        
        # Ensure all markets exist first
        for market_name in ['Bilka', 'Rema 1000', 'Netto', 'Føtex', 'Lidl']:
            if not Market.query.filter_by(name=market_name).first():
                print(f"Creating market: {market_name}")
                market = Market(name=market_name)
                db.session.add(market)
        db.session.commit()
        
        # Sample offers for different markets
        sample_offers = [
            # Bilka offers
            {'market': 'Bilka', 'product': 'Bananer', 'price': 12.50, 'unit': 'kg'},
            {'market': 'Bilka', 'product': 'Mælk Letmælk 1,5%', 'price': 8.95, 'unit': 'l'},
            {'market': 'Bilka', 'product': 'Rugbrød', 'price': 15.00, 'unit': 'stk'},
            {'market': 'Bilka', 'product': 'Hakket Oksekød', 'price': 49.95, 'unit': 'kg'},
            {'market': 'Bilka', 'product': 'Gulerødder', 'price': 5.00, 'unit': 'kg'},
            
            # Rema 1000 offers
            {'market': 'Rema 1000', 'product': 'Bananer', 'price': 13.50, 'unit': 'kg'},
            {'market': 'Rema 1000', 'product': 'Mælk Letmælk', 'price': 7.95, 'unit': 'l'},
            {'market': 'Rema 1000', 'product': 'Franskbrød', 'price': 12.00, 'unit': 'stk'},
            {'market': 'Rema 1000', 'product': 'Kartofler', 'price': 8.95, 'unit': 'kg'},
            {'market': 'Rema 1000', 'product': 'Ost 45+', 'price': 35.00, 'unit': 'stk'},
            
            # Netto offers
            {'market': 'Netto', 'product': 'Bananer', 'price': 11.95, 'unit': 'kg'},
            {'market': 'Netto', 'product': 'Minimælk', 'price': 6.95, 'unit': 'l'},
            {'market': 'Netto', 'product': 'Toastbrød', 'price': 10.00, 'unit': 'stk'},
            {'market': 'Netto', 'product': 'Tomater', 'price': 15.00, 'unit': 'kg'},
            {'market': 'Netto', 'product': 'Agurker', 'price': 8.00, 'unit': 'stk'},
            
            # Føtex offers
            {'market': 'Føtex', 'product': 'Økologiske Bananer', 'price': 15.95, 'unit': 'kg'},
            {'market': 'Føtex', 'product': 'Sødmælk', 'price': 9.50, 'unit': 'l'},
            {'market': 'Føtex', 'product': 'Havregryn', 'price': 18.00, 'unit': 'pk'},
            {'market': 'Føtex', 'product': 'Kyllingebryst', 'price': 59.95, 'unit': 'kg'},
            {'market': 'Føtex', 'product': 'Æbler', 'price': 18.00, 'unit': 'kg'},
            
            # Lidl offers
            {'market': 'Lidl', 'product': 'Bananer', 'price': 10.95, 'unit': 'kg'},
            {'market': 'Lidl', 'product': 'Mælk', 'price': 6.49, 'unit': 'l'},
            {'market': 'Lidl', 'product': 'Rundstykker', 'price': 7.95, 'unit': 'pk'},
            {'market': 'Lidl', 'product': 'Pasta', 'price': 5.95, 'unit': 'pk'},
            {'market': 'Lidl', 'product': 'Appelsiner', 'price': 12.95, 'unit': 'kg'},
        ]
        
        # Set validity dates (this week)
        today = datetime.now().date()
        valid_from = today
        valid_to = today + timedelta(days=7)
        
        added_count = 0
        for offer_data in sample_offers:
            # Get market
            market = Market.query.filter_by(name=offer_data['market']).first()
            if not market:
                print(f"Warning: Market {offer_data['market']} not found")
                continue
            
            # Create offer
            offer = Offer(
                market_id=market.id,
                product_name=offer_data['product'],
                price=offer_data['price'],
                unit=offer_data['unit'],
                valid_from=valid_from,
                valid_to=valid_to
            )
            db.session.add(offer)
            added_count += 1
        
        db.session.commit()
        print(f"Successfully added {added_count} sample offers")


if __name__ == '__main__':
    add_sample_data()
