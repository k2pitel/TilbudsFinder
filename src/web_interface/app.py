"""Flask web application for TilbudsFinder."""

import os
from flask import Flask, render_template, request, jsonify
from src.database import db, Market, Offer, init_db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tilbudsfinder.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    init_db(app)
    
    return app


app = create_app()


@app.route('/')
def index():
    """Main page showing all offers."""
    return render_template('index.html')


@app.route('/api/offers')
def get_offers():
    """
    API endpoint to get offers with filtering and sorting.
    
    Query parameters:
        - search: Search term for product names
        - market: Filter by market name
        - sort: Sort by 'price_asc' or 'price_desc'
        - page: Page number (default 1)
        - per_page: Items per page (default 20)
    """
    # Get query parameters
    search_term = request.args.get('search', '').strip()
    market_filter = request.args.get('market', '')
    sort_order = request.args.get('sort', 'price_asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query
    query = Offer.query
    
    # Apply search filter
    if search_term:
        query = query.filter(Offer.product_name.ilike(f'%{search_term}%'))
    
    # Apply market filter
    if market_filter:
        market = Market.query.filter_by(name=market_filter).first()
        if market:
            query = query.filter_by(market_id=market.id)
    
    # Apply sorting
    if sort_order == 'price_desc':
        query = query.order_by(Offer.price.desc())
    else:  # Default to ascending
        query = query.order_by(Offer.price.asc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Convert to dictionary
    offers = [offer.to_dict() for offer in pagination.items]
    
    return jsonify({
        'offers': offers,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@app.route('/api/markets')
def get_markets():
    """API endpoint to get all markets."""
    markets = Market.query.all()
    return jsonify({
        'markets': [market.to_dict() for market in markets]
    })


@app.route('/api/process-pdf', methods=['POST'])
def process_pdf():
    """
    API endpoint to process a PDF file and extract offers.
    
    Expected JSON body:
        - pdf_path: Path to PDF file
        - market_name: Name of the market
    """
    data = request.get_json()
    pdf_path = data.get('pdf_path')
    market_name = data.get('market_name')
    
    if not pdf_path or not market_name:
        return jsonify({'error': 'Missing pdf_path or market_name'}), 400
    
    try:
        # Import processing modules
        from src.pdf_processor import extract_pdf_text
        from src.nlp_processor import extract_offers
        
        # Extract text from PDF
        text = extract_pdf_text(pdf_path)
        
        if not text:
            return jsonify({'error': 'Failed to extract text from PDF'}), 400
        
        # Extract offers from text
        offers_data = extract_offers(text, market_name)
        
        # Get or create market
        market = Market.query.filter_by(name=market_name).first()
        if not market:
            market = Market(name=market_name)
            db.session.add(market)
            db.session.commit()
        
        # Save offers to database
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
        
        return jsonify({
            'success': True,
            'offers_extracted': len(offers_data),
            'offers_saved': saved_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
