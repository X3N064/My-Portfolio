import yfinance as yf
from datetime import datetime
from pathlib import Path

# Portfolio data
portfolio = {
    "NVDA": {"shares": 38, "avg_price": 123.90},
    "MSFT": {"shares": 11, "avg_price": 398.20},
    "AMZN": {"shares": 20, "avg_price": 214.03},
    "GOOGL": {"shares": 26, "avg_price": 171.66},
}

# Output SVG path
output_path = Path("assets/trading.svg")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Fetch live data
def fetch_data(tickers):
    return yf.download(tickers=tickers, period="1d", interval="1m")

# Generate SVG content
def create_svg(prices):
    total_value = 0
    total_cost = 0
    lines = []
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

        lines.append(f"{symbol}: ${price:.2f} | PnL: {'+' if pnl>=0 else '-'}${abs(pnl):.2f} ({percent:+.2f}%)")

    total_pnl = total_value - total_cost
    total_percent = (total_pnl / total_cost) * 100

    # SVG Template
    # (inside create_svg function, replace the SVG part with this)

    svg = f'''<svg width="400" height="230" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#1e1e2f; stop-opacity:1">
            <animate attributeName="offset" values="0;1;0" dur="20s" repeatCount="indefinite" />
          </stop>
          <stop offset="100%" style="stop-color:#2e2e4f; stop-opacity:1" />
        </linearGradient>
      </defs>

      <style>
        .title {{ fill: #ff4081; font-weight: bold; font-size: 18px; }}
        .stat {{ fill: white; font-size: 14px; }}
        .highlight {{ fill: {'#00e676' if total_pnl > 0 else '#ff1744'}; font-weight: bold; animation: pulse 2s infinite; }}
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
        svg {{ background: url(#grad); font-family: monospace; }}
      </style>

      <rect width="100%" height="100%" rx="15" fill="url(#grad)"/>

      <text x="20" y="30" class="title">Hyun(Kenneth) Sim's Trading Stats</text>
      <text x="20" y="55" class="stat">{lines[0]}</text>
      <text x="20" y="75" class="stat">{lines[1]}</text>
      <text x="20" y="95" class="stat">{lines[2]}</text>
      <text x="20" y="115" class="stat">{lines[3]}</text>

      <text x="20" y="150" class="highlight">Total PnL: ${total_pnl:+.2f} ({total_percent:+.2f}%)</text>
      <text x="20" y="190" class="timestamp">Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</text>
    </svg>'''


    return svg

# Save SVG
def save_svg(content):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    tickers = list(portfolio.keys())
    data = fetch_data(tickers)
    # Restructure to get last Close price for each ticker
    prices = {ticker: {"Close": data["Close"][ticker]} for ticker in tickers}
    svg_content = create_svg(prices)
    save_svg(svg_content)
    print(f"✅ Updated {output_path}")
