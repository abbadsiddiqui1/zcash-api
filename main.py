from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="Zcash Tracker API", version="1.0.0")

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
HEADERS = {"Accept": "application/json"}


async def fetch(url: str, params: dict = None) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params, headers=HEADERS)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="CoinGecko request failed")
        return r.json()


@app.get("/price")
async def current_price():
    data = await fetch(f"{COINGECKO_BASE}/simple/price", {
        "ids": "zcash",
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_last_updated_at": "true",
    })
    zec = data["zcash"]
    return {
        "symbol": "ZEC",
        "price_usd": zec["usd"],
        "change_24h_pct": zec.get("usd_24h_change"),
        "last_updated": zec.get("last_updated_at"),
    }


@app.get("/market")
async def market_stats():
    data = await fetch(f"{COINGECKO_BASE}/coins/zcash", {
        "localization": "false",
        "tickers": "false",
        "community_data": "false",
        "developer_data": "false",
    })
    md = data["market_data"]
    return {
        "symbol": "ZEC",
        "price_usd": md["current_price"]["usd"],
        "market_cap_usd": md["market_cap"]["usd"],
        "volume_24h_usd": md["total_volume"]["usd"],
        "circulating_supply": md["circulating_supply"],
        "total_supply": md["total_supply"],
        "max_supply": md["max_supply"],
        "ath_usd": md["ath"]["usd"],
        "ath_date": md["ath_date"]["usd"],
        "high_24h_usd": md["high_24h"]["usd"],
        "low_24h_usd": md["low_24h"]["usd"],
    }


@app.get("/history")
async def price_history(
    days: int = Query(default=7, ge=1, le=365, description="Number of days of history (1–365)")
):
    data = await fetch(f"{COINGECKO_BASE}/coins/zcash/market_chart", {
        "vs_currency": "usd",
        "days": days,
    })
    prices = [{"timestamp": ts, "price_usd": price} for ts, price in data["prices"]]
    volumes = {ts: vol for ts, vol in data["total_volumes"]}
    market_caps = {ts: mc for ts, mc in data["market_caps"]}

    result = []
    for entry in prices:
        ts = entry["timestamp"]
        result.append({
            "timestamp": ts,
            "price_usd": entry["price_usd"],
            "volume_usd": volumes.get(ts),
            "market_cap_usd": market_caps.get(ts),
        })

    return {"symbol": "ZEC", "days": days, "data_points": len(result), "history": result}
