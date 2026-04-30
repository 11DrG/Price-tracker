# PriceTracker

![PriceTracker](https://github.com/MerlaSilviuAlexandru/Price-tracker/actions/workflows/price_tracker.yml/badge.svg)

A Python automation tool that monitors product prices across multiple Romanian e-commerce sites and sends a Telegram notification whenever a price drops.

## Supported sites

- [eMAG](https://www.emag.ro)
- [Altex](https://www.altex.ro)
- [Carrefour](https://www.carrefour.ro)

## How it works

1. Reads the product list from `products.json`
2. Opens each product page using Playwright (headless browser)
3. Scrapes the current price and original (strikethrough) price
4. Compares against the last known price stored in `last_price.json`
5. Sends a Telegram notification if the price dropped, including discount % and an all-time low badge when applicable
6. Logs every price change to `price_history.csv`
7. Sends a Telegram alert if scraping a product fails after all retries

Runs automatically every hour via GitHub Actions.

## Project structure

```
Price-tracker/
├── .github/workflows/
│   └── price_tracker.yml   # CI/CD: run tests then track prices hourly
├── pages/
│   ├── base_page.py        # Shared Playwright page logic
│   ├── emag_page.py        # eMAG price locators
│   ├── altex_page.py       # Altex price locators
│   ├── carrefour_page.py   # Carrefour price locators
│   └── page_factory.py     # Routes URLs to the correct page class
├── tests/
│   ├── test_scrapers.py        # Mocked browser tests for all page classes
│   ├── test_page_classes.py    # Site name and inheritance tests
│   ├── test_check_deal.py      # Notification and price logic tests
│   ├── test_price_history.py   # Load/save history tests
│   ├── test_parse_price.py     # Price parsing tests
│   └── test_telegram.py        # Telegram API call tests
├── tracker.py          # Orchestration and business logic
├── utils.py            # Price string parser
├── products.json       # List of products to track
├── Dockerfile          # Container image definition
├── docker-compose.yml  # One-command run for local/shared use
├── requirements.txt    # Python dependencies
└── .env.example        # Environment variable template
```

## Setup

### Option A — Docker (recommended for sharing)

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your Telegram credentials
3. Edit `products.json` with the products you want to track
4. Run:

```bash
docker compose up --build
```

Price history is stored in a Docker named volume and persists between runs.

### Option B — Local Python

**1. Install dependencies**

```bash
pip install -r requirements.txt
playwright install chromium
```

**2. Create a `.env` file**

```bash
cp .env.example .env
# then edit .env with your credentials
```

**3. Add products to track**

Edit `products.json` — no code changes needed:

```json
[
    {
        "name": "Product Name",
        "url": "https://www.emag.ro/..."
    }
]
```

**4. Run the tracker**

```bash
python tracker.py
```

To scrape prices without sending notifications or saving history:

```bash
python tracker.py --dry-run
```

**5. Run the tests**

```bash
pytest tests/ -v
```

## GitHub Actions setup

To run the tracker automatically every hour:

1. Fork or push this repo to GitHub
2. Go to *Settings → Secrets and variables → Actions* and add:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`

The workflow will run tests first and only track prices if they pass.

## Tech stack

- Python 3.11
- Playwright (browser automation)
- Requests (Telegram API)
- python-dotenv
- pytest
- GitHub Actions
- Docker
