# TilbudsFinder 🛒

An automated system for extracting and comparing Danish supermarket offers from weekly tilbudsaviser (promotional flyers). This bachelor project processes PDF flyers from selected markets using text extraction and NLP to identify products, prices, units, and validity periods.

## Features

- **PDF Processing**: Extract text from supermarket PDF flyers using advanced text extraction
- **NLP Analysis**: Automatically identify products, prices, units (kg, stk, L), and validity periods
- **Database Storage**: Store structured offer data in SQLite database
- **Web Interface**: 
  - Search for products
  - Filter by supermarket
  - Sort by price (ascending/descending)
  - Clean, responsive design with Danish language support

## Supported Supermarkets

- Bilka
- Rema 1000
- Netto
- Føtex
- Lidl

## Project Structure

```
TilbudsFinder/
├── src/
│   ├── database/           # Database models and initialization
│   ├── pdf_processor/      # PDF text extraction
│   ├── nlp_processor/      # NLP offer extraction
│   └── web_interface/      # Flask web application
│       ├── static/         # CSS and JavaScript
│       └── templates/      # HTML templates
├── pdfs/                   # Place PDF files here
├── tests/                  # Unit tests
├── run.py                  # Main application entry point
├── process_pdf.py          # Script to process PDF files
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/k2pitel/TilbudsFinder.git
cd TilbudsFinder
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure environment variables:
```bash
# Create a .env file for production settings
echo "SECRET_KEY=your-secure-random-key-here" > .env
echo "FLASK_DEBUG=0" >> .env
echo "DATABASE_URL=sqlite:///tilbudsfinder.db" >> .env
```

## Usage

### 1. Processing PDF Files

Place your supermarket PDF flyers in the `pdfs/` directory, then process them:

```bash
python process_pdf.py pdfs/bilka_uge45.pdf "Bilka"
python process_pdf.py pdfs/rema1000_uge45.pdf "Rema 1000"
```

The script will:
- Extract text from the PDF
- Identify products, prices, units, and validity periods
- Save the offers to the database

### 2. Running the Web Application

Start the web server:

```bash
python run.py
```

For development with debug mode enabled:
```bash
FLASK_DEBUG=1 python run.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### 3. Using the Web Interface

- **Search**: Enter product names in the search box
- **Filter**: Select a specific supermarket from the dropdown
- **Sort**: Choose to sort by price (low to high or high to low)
- **Browse**: View all available offers with pagination

## API Endpoints

The application provides REST API endpoints:

### Get Offers
```
GET /api/offers
```
Query parameters:
- `search` - Search term for product names
- `market` - Filter by market name
- `sort` - Sort order: `price_asc` or `price_desc`
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20)

### Get Markets
```
GET /api/markets
```
Returns list of all available markets.

### Process PDF
```
POST /api/process-pdf
Content-Type: application/json

{
  "pdf_path": "path/to/pdf",
  "market_name": "Bilka"
}
```
Processes a PDF file and extracts offers.

## Database Schema

### Markets Table
- `id` - Primary key
- `name` - Market name (unique)
- `created_at` - Timestamp

### Offers Table
- `id` - Primary key
- `market_id` - Foreign key to markets
- `product_name` - Name of the product
- `price` - Price in DKK
- `unit` - Unit (kg, stk, L, etc.)
- `valid_from` - Offer start date
- `valid_to` - Offer end date
- `extracted_at` - Extraction timestamp

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Processing**: PyPDF2, pdfplumber
- **NLP**: Regular expressions, python-dateutil
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with responsive design

## Development

### Environment Variables

The application supports the following environment variables:

- `SECRET_KEY` - Secret key for Flask sessions (required in production)
- `FLASK_DEBUG` - Set to `1` to enable debug mode (default: `0`)
- `DATABASE_URL` - Database connection string (default: `sqlite:///tilbudsfinder.db`)

### Running Tests

```bash
python -m pytest tests/
```

### Code Structure

- `src/database/models.py` - Database models and initialization
- `src/pdf_processor/extractor.py` - PDF text extraction logic
- `src/nlp_processor/extractor.py` - NLP offer extraction logic
- `src/web_interface/app.py` - Flask application and API routes
- `src/web_interface/templates/index.html` - Main page template
- `src/web_interface/static/css/style.css` - Application styles
- `src/web_interface/static/js/app.js` - Frontend JavaScript

## Danish Language Support

The NLP processor includes:
- Danish month name recognition (januar, februar, marts, etc.)
- Common Danish units (kg, stk, pk, etc.)
- Danish price formats (XX,XX kr, XX,-)
- Danish date formats

## Limitations and Future Improvements

- PDF quality affects extraction accuracy
- Complex layouts may require manual tuning
- Currently uses rule-based NLP (could be enhanced with ML models)
- No image recognition (text-only extraction)

## License

This is a bachelor project for educational purposes.

## Authors

Bachelor Project - 2024

## Contributing

This is an academic project. For questions or suggestions, please open an issue.

---

**Note**: This system is designed for educational purposes as part of a bachelor thesis on automated extraction of supermarket offers from PDF flyers.