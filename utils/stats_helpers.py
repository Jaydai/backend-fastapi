from datetime import datetime


# Energy cost constants (in joules per token)
ENERGY_COST_PER_INPUT_TOKEN = 0.0003
ENERGY_COST_PER_OUTPUT_TOKEN = 0.0006
JOULES_PER_WH = 3600
CO2_PER_KWH = 0.42  # kg CO2 per kWh (global average)

# Estimated cost per token by model (USD)
MODEL_COSTS = {
    "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},
    "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
    "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
    "claude-3-opus": {"input": 0.015 / 1000, "output": 0.075 / 1000},
    "claude-3-sonnet": {"input": 0.003 / 1000, "output": 0.015 / 1000},
    "claude-3-haiku": {"input": 0.00025 / 1000, "output": 0.00125 / 1000},
    "default": {"input": 0.002 / 1000, "output": 0.004 / 1000}
}


def estimate_tokens(content: str | None) -> int:
    """Estimate token count from text content"""
    if not content:
        return 0
    return max(1, len(str(content)) // 4)


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate estimated cost for token usage"""
    costs = MODEL_COSTS.get(model, MODEL_COSTS["default"])
    return (input_tokens * costs["input"]) + (output_tokens * costs["output"])


def energy_to_equivalent(wh: float) -> str:
    """Convert energy consumption to human-readable equivalent"""
    if wh < 0.05:
        return "équivaut à allumer une LED pendant quelques secondes"
    elif wh < 0.2:
        return "équivaut à allumer une LED pendant une minute"
    elif wh < 1:
        return "équivaut à une minute de vidéo YouTube"
    else:
        return "équivaut à quelques minutes d'ordinateur portable"


def parse_datetime_safe(timestamp_str: str) -> datetime:
    """Safely parse datetime string with various formats"""
    try:
        # Handle timezone info
        timestamp = timestamp_str.replace('Z', '+00:00')

        # If it has microseconds but incomplete (e.g., .44 instead of .440000)
        if '.' in timestamp and '+' in timestamp:
            parts = timestamp.split('+')
            datetime_part = parts[0]
            timezone_part = '+' + parts[1]

            if '.' in datetime_part:
                date_part, microsecond_part = datetime_part.split('.')
                # Pad microseconds to 6 digits
                microsecond_part = microsecond_part.ljust(6, '0')[:6]
                timestamp = f"{date_part}.{microsecond_part}{timezone_part}"

        return datetime.fromisoformat(timestamp)
    except Exception:
        # Fallback: try to parse without microseconds
        try:
            # Remove microseconds entirely
            base_timestamp = timestamp_str.split('.')[0]
            if 'Z' in base_timestamp:
                base_timestamp = base_timestamp.replace('Z', '+00:00')
            elif not ('+' in base_timestamp or '-' in base_timestamp[-6:]):
                base_timestamp += '+00:00'
            return datetime.fromisoformat(base_timestamp)
        except Exception:
            # Last resort: use current time
            return datetime.now()


def fetch_all_paginated(repository_fn, batch_size: int = 1000):
    """Fetch all records using pagination"""
    offset = 0
    all_items = []

    while True:
        batch = repository_fn(offset, batch_size)
        if not batch:
            break

        all_items.extend(batch)

        if len(batch) < batch_size:
            break

        offset += batch_size

    return all_items
