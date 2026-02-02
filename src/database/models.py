"""Database models for TilbudsFinder."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Market(db.Model):
    """Represents a supermarket chain."""
    __tablename__ = 'markets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    offers = db.relationship('Offer', backref='market', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Market {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }


class Offer(db.Model):
    """Represents a product offer from a market."""
    __tablename__ = 'offers'
    
    id = db.Column(db.Integer, primary_key=True)
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))  # kg, stk, L, etc.
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)
    extracted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Offer {self.product_name} - {self.price}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'market': self.market.name,
            'product_name': self.product_name,
            'price': self.price,
            'unit': self.unit,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_to': self.valid_to.isoformat() if self.valid_to else None,
            'extracted_at': self.extracted_at.isoformat()
        }


def init_db(app):
    """Initialize the database."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Add default markets if they don't exist
        default_markets = ['Bilka', 'Rema 1000', 'Netto', 'Føtex', 'Lidl']
        for market_name in default_markets:
            if not Market.query.filter_by(name=market_name).first():
                market = Market(name=market_name)
                db.session.add(market)
        db.session.commit()
