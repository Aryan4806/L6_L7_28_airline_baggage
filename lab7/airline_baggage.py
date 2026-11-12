"""Airline baggage helpers - hardened after fuzz testing (Lab 7).

Every function validates its input and returns None for anything invalid
instead of raising an exception, so no input can crash the program.
"""
import math

MAX_FLIGHT_DIGITS = 4        # flight numbers are 1-4 digits (also avoids int() digit-limit errors)
MAX_BAG_WEIGHT_KG = 1000.0   # sanity cap per bag


def parse_booking(code):
    """'AI-203-12A' -> ('AI', 203, 'A'), or None if the code is invalid."""
    if not isinstance(code, str):
        return None
    parts = code.strip().split('-')
    if len(parts) != 3:
        return None
    airline, flight, seat = (p.strip() for p in parts)
    # isascii() rejects Unicode digits/letters such as '١٢' or 'ß'
    # that isdigit()/isalpha()/int() would otherwise accept.
    if not (airline.isascii() and airline.isalnum()):
        return None
    if not (flight.isascii() and flight.isdigit() and len(flight) <= MAX_FLIGHT_DIGITS):
        return None
    if not (seat.isascii() and seat.isalnum() and seat[-1].isalpha()):
        return None
    return airline.upper(), int(flight), seat[-1].upper()


def total_weight(weights_csv):
    """'12.5,7,23' -> 42.5, or None if any weight is missing, not a number,
    negative, NaN/infinite or unrealistically large."""
    if not isinstance(weights_csv, str):
        return None
    total = 0.0
    for w in weights_csv.split(','):
        w = w.strip()
        if not w:
            return None
        try:
            value = float(w)
        except ValueError:
            return None
        if not math.isfinite(value) or value < 0 or value > MAX_BAG_WEIGHT_KG:
            return None
        total += value
    return total


def tag_label(name):
    """'Aryan Singh' -> 'A. SINGH' (first initial + last name), or None
    if the name does not have at least a first and a last name."""
    if not isinstance(name, str):
        return None
    parts = name.split()
    if len(parts) < 2:
        return None
    return parts[0][0].upper() + '. ' + parts[-1].upper()


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    result = parse_booking(user_input)
    if result is None:
        print("Invalid booking code. Expected format AIRLINE-FLIGHT-SEAT, e.g. AI-203-12A")
    else:
        print("Airline, Flight and Seat Letter:", result)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    result = total_weight(user_input)
    if result is None:
        print("Invalid weights. Enter non-negative numbers separated by commas, e.g. 12.5,7,23")
    else:
        print("Total Weight:", result)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    result = tag_label(user_input)
    if result is None:
        print("Invalid name. Enter at least a first and a last name, e.g. Aryan Singh")
    else:
        print("Tag Label:", result)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
