

def format_large_number(n) -> str:
    if n is None:
        return "N/A"
    if n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.2f}T"
    if n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    return f"${n:,.0f}"


def format_volume(v) -> str:
    if v is None:
        return "N/A"
    if v >= 1_000_000:
        return f"{v / 1_000_000:.2f}M"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K"
    return str(v)


def build_dataframe(data):
    rows = []
    current = data["current_price"]
    prev = data["previous_close"]
    change = current - prev if current and prev else None
    change_pct = (change / prev * 100) if change and prev else None

    rows.append({
        "Symbol":       data["symbol"],
        "Name":         data["name"],
        "Price":        current,
        "Change":       round(change, 2) if change else None,
        "Change %":     round(change_pct, 2) if change_pct else None,
        "Open":         data["open"],
        "Day High":     data["day_high"],
        "Day Low":      data["day_low"],
        "Volume":       data["volume"],
        "Market Cap":   data["market_cap"],
        "P/E Ratio":    data["pe_ratio"],
        "Sector":       data["sector"],
    })

    return pd.DataFrame(rows).set_index("Symbol")