import yfinance as yf
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

# Portfolio definition
portfolio = {
    "NVDA": {"shares": 38, "avg_price": 123.90},
    "MSFT": {"shares": 11, "avg_price": 398.20},
    "AMZN": {"shares": 20, "avg_price": 214.03},
    "GOOGL": {"shares": 26, "avg_price": 171.66}
}

# Logo paths
logos = {
    "NVDA": "logos/nvda.png",
    "MSFT": "logos/msft.png",
    "AMZN": "logos/amzn.png",
    "GOOGL": "logos/googl.png"
}

# Output paths
output_folder = Path("frames")
output_folder.mkdir(parents=True, exist_ok=True)
gif_path = Path("assets/trading.gif")
gif_path.parent.mkdir(parents=True, exist_ok=True)

# Font fallback
def get_font(size, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    except:
        return ImageFont.load_default()

# Fetch prices from Yahoo Finance
def fetch_prices():
    tickers = list(portfolio.keys())
    data = yf.download(tickers=tickers, period="1d", interval="1m", progress=False)
    prices = {ticker: data["Close"][ticker].dropna().iloc[-1] for ticker in tickers}
    return prices

# Generate a single frame
def generate_frame(prices, frame_idx):
    width, height = 1200, 800
    img = Image.new("RGB", (width, height), color=(30, 30, 40))
    draw = ImageDraw.Draw(img)

    font = get_font(36)
    title_font = get_font(48, bold=True)

    y = 40
    draw.text((40, y), "Hyun (Kenneth) Sim's Portfolio", fill="#ff4081", font=title_font)
    y += 80

    total_value, total_cost = 0, 0

    for symbol, data in portfolio.items():
        price = prices[symbol]
        shares = data["shares"]
        avg_price = data["avg_price"]
        cost = shares * avg_price
        value = shares * price
        pnl = value - cost + random.uniform(-10, 10)  # animated fluctuation
        percent = (pnl / cost) * 100
        total_value += value
        total_cost += cost

        # Logo and stock line
        logo = Image.open(logos[symbol]).resize((64, 64))
        img.paste(logo, (40, y))
        pnl_color = "#00e676" if pnl >= 0 else "#ff1744"

        draw.text((120, y + 8),
                  f"{symbol}: ${price:.2f} | PnL: {pnl:+.2f} ({percent:+.2f}%) | Value: ${value:,.0f}",
                  font=font, fill=pnl_color)
        y += 80

    # Animated totals
    animated_total_value = total_value + random.uniform(-50, 50)
    animated_total_pnl = animated_total_value - total_cost
    animated_total_percent = (animated_total_pnl / total_cost) * 100
    total_color = "#00e676" if animated_total_pnl >= 0 else "#ff1744"

    draw.text((40, y + 20),
              f"Total Portfolio: ${animated_total_value:,.0f}",
              font=font, fill="white")
    draw.text((40, y + 60),
              f"Total PnL: ${animated_total_pnl:+,.0f} ({animated_total_percent:+.2f}%)",
              font=font, fill=total_color)
    draw.text((40, y + 110),
              f"Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
              font=font, fill="gray")

    # Save frame
    img.save(output_folder / f"frame_{frame_idx}.png")

# Generate GIF
def generate_gif():
    frames = []
    for i in range(5):
        prices = fetch_prices()
        generate_frame(prices, i)
        frame = Image.open(output_folder / f"frame_{i}.png")
        frames.append(frame)

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=600,
        loop=0,
        disposal=2,
    )
    print("✅ Generated high-res trading.gif")

# Run the generator
if __name__ == "__main__":
    generate_gif()
