// TilbudsFinder JavaScript Application

let currentPage = 1;
let currentSearch = '';
let currentMarket = '';
let currentSort = 'price_asc';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadMarkets();
    loadOffers();
    
    // Event listeners
    document.getElementById('searchBtn').addEventListener('click', handleSearch);
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    document.getElementById('marketFilter').addEventListener('change', handleMarketFilter);
    document.getElementById('sortOrder').addEventListener('change', handleSortChange);
});

// Load available markets
async function loadMarkets() {
    try {
        const response = await fetch('/api/markets');
        const data = await response.json();
        
        const marketFilter = document.getElementById('marketFilter');
        data.markets.forEach(market => {
            const option = document.createElement('option');
            option.value = market.name;
            option.textContent = market.name;
            marketFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading markets:', error);
    }
}

// Load offers with current filters
async function loadOffers() {
    showLoading(true);
    
    const params = new URLSearchParams({
        page: currentPage,
        per_page: 20
    });
    
    if (currentSearch) {
        params.append('search', currentSearch);
    }
    if (currentMarket) {
        params.append('market', currentMarket);
    }
    if (currentSort) {
        params.append('sort', currentSort);
    }
    
    try {
        const response = await fetch(`/api/offers?${params}`);
        const data = await response.json();
        
        displayOffers(data.offers);
        updateResultsInfo(data.total, data.page, data.per_page);
        displayPagination(data.page, data.pages);
    } catch (error) {
        console.error('Error loading offers:', error);
        displayError('Kunne ikke indlæse tilbud. Prøv venligst igen.');
    } finally {
        showLoading(false);
    }
}

// Display offers in the grid
function displayOffers(offers) {
    const container = document.getElementById('offersContainer');
    
    if (offers.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h2>Ingen tilbud fundet</h2>
                <p>Prøv at justere dine søgekriterier</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = offers.map(offer => createOfferCard(offer)).join('');
}

// Create HTML for a single offer card
function createOfferCard(offer) {
    const unit = offer.unit ? ` / ${offer.unit}` : '';
    const validityText = offer.valid_from && offer.valid_to 
        ? `Gyldig: ${formatDate(offer.valid_from)} - ${formatDate(offer.valid_to)}`
        : '';
    
    return `
        <div class="offer-card">
            <span class="offer-market">${escapeHtml(offer.market)}</span>
            <div class="offer-product">${escapeHtml(offer.product_name)}</div>
            <div class="offer-price">${offer.price.toFixed(2)} kr${unit}</div>
            ${validityText ? `<div class="offer-validity">${validityText}</div>` : ''}
        </div>
    `;
}

// Update results info text
function updateResultsInfo(total, page, perPage) {
    const info = document.getElementById('resultsInfo');
    const start = (page - 1) * perPage + 1;
    const end = Math.min(page * perPage, total);
    
    if (total > 0) {
        info.textContent = `Viser ${start}-${end} af ${total} tilbud`;
    } else {
        info.textContent = '';
    }
}

// Display pagination controls
function displayPagination(currentPage, totalPages) {
    const container = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let html = '';
    
    // Previous button
    html += `<button ${currentPage === 1 ? 'disabled' : ''} onclick="goToPage(${currentPage - 1})">« Forrige</button>`;
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            html += `<button class="${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += '<span>...</span>';
        }
    }
    
    // Next button
    html += `<button ${currentPage === totalPages ? 'disabled' : ''} onclick="goToPage(${currentPage + 1})">Næste »</button>`;
    
    container.innerHTML = html;
}

// Handle search
function handleSearch() {
    currentSearch = document.getElementById('searchInput').value;
    currentPage = 1;
    loadOffers();
}

// Handle market filter
function handleMarketFilter() {
    currentMarket = document.getElementById('marketFilter').value;
    currentPage = 1;
    loadOffers();
}

// Handle sort change
function handleSortChange() {
    currentSort = document.getElementById('sortOrder').value;
    currentPage = 1;
    loadOffers();
}

// Go to specific page
function goToPage(page) {
    currentPage = page;
    loadOffers();
}

// Show/hide loading indicator
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('offersContainer').style.display = show ? 'none' : 'grid';
}

// Display error message
function displayError(message) {
    const container = document.getElementById('offersContainer');
    container.innerHTML = `
        <div class="empty-state">
            <h2>Fejl</h2>
            <p>${message}</p>
        </div>
    `;
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('da-DK', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
