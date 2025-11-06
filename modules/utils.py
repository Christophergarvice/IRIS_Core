def letter_value_sum(text: str) -> int:
    """Convert letters A–Z to numeric values and sum them."""
    return sum(ord(c) - ord('A') + 1 for c in text.upper() if c.isalpha())