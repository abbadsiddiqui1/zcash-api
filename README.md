# Zcash Tracker API

A REST API for tracking the Zcash (ZEC) cryptocurrency, built with FastAPI and powered by CoinGecko.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/price` | Live ZEC price and 24h change |
| GET | `/market` | Market cap, volume, supply, and ATH |
| GET | `/history?days=7` | Historical price, volume, and market cap (1–365 days) |

## Setup

**Requirements:** Python 3.8+

```bash
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`

## Example Responses

**GET /price**
```json
{
  "symbol": "ZEC",
  "price_usd": 416.20,
  "change_24h_pct": 19.65,
  "last_updated": 1780863823
}
```

**GET /market**
```json
{
  "symbol": "ZEC",
  "price_usd": 416.20,
  "market_cap_usd": 6932739733,
  "volume_24h_usd": 1232273902,
  "circulating_supply": 16754743.9,
  "total_supply": 16755170.5,
  "max_supply": 21000000.0,
  "ath_usd": 3191.93,
  "ath_date": "2016-10-29T00:00:00.000Z",
  "high_24h_usd": 436.24,
  "low_24h_usd": 346.39
}
```

**GET /history?days=3**
```json
{
  "symbol": "ZEC",
  "days": 3,
  "data_points": 73,
  "history": [
    {
      "timestamp": 1780606834777,
      "price_usd": 519.46,
      "volume_usd": 1235869607.05,
      "market_cap_usd": 8683021112.57
    }
  ]
}
```

## Data Source

All data is fetched from the [CoinGecko API](https://www.coingecko.com/en/api) — no API key required.
