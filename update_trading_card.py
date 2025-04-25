import yfinance as yf
from datetime import datetime
from pathlib import Path

# Portfolio data
portfolio = {
    "NVDA": {"shares": 38, "avg_price": 123.90},
    "MSFT": {"shares": 11, "avg_price": 398.20},
    "AMZN": {"shares": 20, "avg_price": 214.03},
    "GOOGL": {"shares": 26, "avg_price": 171.66}
}

# Base64-encoded SVG logos (minified SVGs encoded as base64)
logos = {
    "NVDA": "data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMDAwMDAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHJlY3Qgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiBmaWxsPSIjOTlkZjAwIiByeD0iMyIvPjwvc3ZnPg==",
    "MSFT": "data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMDAwMDAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHJlY3Qgd2lkdGg9IjgiIGhlaWdodD0iOCIgeD0iMCIgeT0iMCIgZmlsbD0iI2ZmMzMwMCIvPjxyZWN0IHdpZHRoPSI4IiBoZWlnaHQ9IjgiIHg9IjgiIHk9IjAiIGZpbGw9IiMwMDk5ZmYiLz48cmVjdCB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB4PSIwIiB5PSI4IiBmaWxsPSIjZmY5OTAwIi8+PHJlY3Qgd2lkdGg9IjgiIGhlaWdodD0iOCIgeD0iOCIgeT0iOCIgcmlnaHQ9IiMwMGZmMDAiLz48L3N2Zz4=",
    "AMZN": "data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMDAwMDAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHJlY3Qgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiBmaWxsPSIjZmZ5NTIwIiByeD0iMyIvPjwvc3ZnPg==",
    "GOOGL": "data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjMDAwMDAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PGNpcmNsZSBjeD0iOCIgY3k9IjgiIHI9IjgiIGZpbGw9IiMwMDk5ZmYiIC8+PC9zdmc+"
}

output_path = Path("assets/trading.svg")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Fetch stock data
def fetch_data(tickers):
    return yf.download(tickers=tickers, period="1d", interval="1m")

# Generate SVG
def create_svg(prices):
    total_value = 0
    total_cost = 0
    lines = []
    y = 55
    content = ""

    for symbol, data in portfolio.items():
        shares = data["shares"]
        avg_price = data["avg_price"]
        price = prices[symbol]["Close"][-1]
        cost = shares * avg_price
        value = shares * price
        pnl = value - cost
        percent = (pnl / cost) * 100
        total_cost += cost
        total_value += value

        content += f'''
        <image href="{logos[symbol]}" x="20" y="{y-18}" height="20" width="20"/>
        <text x="50" y="{y}" class="stat">{symbol} - ${price:.2f} | PnL: {'+' if pnl>=0 else '-'}${abs(pnl):.2f} ({percent:+.2f}%) | Value: ${value:,.0f}</text>
        '''
        y += 25

    total_pnl = total_value - total_cost
    total_percent = (total_pnl / total_cost) * 100

    svg = f'''<svg width="500" height="{y+80}" xmlns="http://www.w3.org/2000/svg">
    <style>
      .title {{ fill: #ff4081; font-weight: bold; font-size: 20px; }}
      .stat {{ fill: white; font-size: 14px; }}
      .highlight {{ fill: {'#00e676' if total_pnl > 0 else '#ff1744'}; font-weight: bold; font-size: 16px; animation: pulse 2s infinite; }}
      .timestamp {{ fill: gray; font-size: 12px; animation: fadeGlow 5s infinite alternate; }}
      @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
        100% {{ transform: scale(1); }}
      }}
      @keyframes fadeGlow {{
        from {{ opacity: 0.5; }}
        to {{ opacity: 1; }}
      }}
      svg {{ background: #1e1e2f; font-family: monospace; }}
    </style>

    <rect width="100%" height="100%" rx="15" fill="#1e1e2f"/>

    <text x="20" y="30" class="title">Hyun (Kenneth) Sim's Trading Stats</text>

    {content}

    <text x="20" y="{y+20}" class="highlight">Total Portfolio: ${total_value:,.0f}</text>
    <text x="20" y="{y+45}" class="highlight">Total PnL: ${total_pnl:+,.0f} ({total_percent:+.2f}%)</text>

    <text x="20" y="{y+70}" class="timestamp">Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</text>
  </svg>'''

    return svg

def save_svg(content):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    tickers = list(portfolio.keys())
    data = fetch_data(tickers)
    prices = {ticker: {"Close": data["Close"][ticker]} for ticker in tickers}
    svg_content = create_svg(prices)
    save_svg(svg_content)
    print(f"✅ Updated {output_path}")