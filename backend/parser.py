import re

def clean_text(text):
    return text.replace("|", "").replace("=", "").strip()


def find_total(lines):
    total_patterns = [
        r"total[^0-9]*([\d]+\.\d{2})",
        r"amount[^0-9]*([\d]+\.\d{2})",
        r"balance[^0-9]*([\d]+\.\d{2})"
    ]

    for line in lines[::-1]:  # search from bottom
        lower = line.lower()
        for pattern in total_patterns:
            match = re.search(pattern, lower)
            if match:
                return match.group(1)

        # fallback: last large price on receipt
        prices = re.findall(r"\d+\.\d{2}", line)
        if prices:
            return prices[-1]

    return "N/A"


def find_date(lines):
    date_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{2,4}\b"
    for line in lines:
        match = re.search(date_pattern, line)
        if match:
            return match.group()
    return "N/A"


def find_store(lines):
    # assume store name is near top and mostly letters
    for line in lines[:5]:
        clean = clean_text(line)
        if len(clean) > 5 and not any(char.isdigit() for char in clean):
            return clean
    return "Unknown Store"


def find_items(lines):
    items = []

    for line in lines:
        match = re.search(r"(.+?)\s+(\d+\.\d{2})", line)
        if match:
            name = clean_text(match.group(1))
            price = match.group(2)

            # ignore totals or payment lines
            if "total" in name.lower():
                continue
            if len(name) < 3:
                continue

            items.append(f"{name} — ${price}")

    return items


def parse_receipt(lines):
    return {
        "store": find_store(lines),
        "date": find_date(lines),
        "total": find_total(lines),
        "items": find_items(lines)
    }