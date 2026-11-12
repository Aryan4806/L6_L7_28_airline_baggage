"""Lab 7 - Fuzz testing airline_baggage.py with Hypothesis.

Two kinds of property are checked for each of the three functions:
  1. No crash: for ANY input (random Unicode text, None, or other types)
     the function must not raise an exception. Invalid input must be
     rejected by returning None.
  2. Correctness: for VALID generated input the function returns the
     expected value, and every result it does return is well formed.

Run:
    pytest test_airline_baggage.py        (or: python -m pytest test_airline_baggage.py)
"""
import math

from hypothesis import given, settings, strategies as st
from airline_baggage import parse_booking, total_weight, tag_label

# Random junk: any Unicode text, None, or values of the wrong type.
any_input = st.text() | st.none() | st.integers() | st.floats() | st.lists(st.text())

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"


# ============================ parse_booking ============================

@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


@settings(max_examples=300)
@given(any_input)
def test_parse_booking_no_crash_any_type(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"


@settings(max_examples=300)
@given(st.text(alphabet=LETTERS + DIGITS + "-", max_size=20))
def test_parse_booking_booking_like_strings(s):
    """Strings made only of booking characters (letters, digits, '-') hit the
    split / int / seat-letter logic much more often than random Unicode."""
    try:
        result = parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"
    if result is not None:
        airline, flight, seat = result
        assert airline.isalnum() and airline == airline.upper()
        assert isinstance(flight, int) and flight >= 0
        assert len(seat) == 1 and seat.isalpha() and seat == seat.upper()


@given(
    airline=st.text(alphabet=LETTERS, min_size=2, max_size=3),
    flight=st.integers(min_value=1, max_value=9999),
    row=st.integers(min_value=1, max_value=60),
    seat=st.sampled_from("ABCDEFabcdef"),
)
def test_parse_booking_valid_codes(airline, flight, row, seat):
    code = f"{airline}-{flight}-{row}{seat}"
    assert parse_booking(code) == (airline.upper(), flight, seat.upper())


# ============================ total_weight =============================

@settings(max_examples=500)
@given(st.text() | st.none())
def test_total_weight_no_crash(s):
    try:
        total_weight(s)
    except Exception as e:
        assert False, f"total_weight crashed with: {e!r}"


@settings(max_examples=300)
@given(any_input)
def test_total_weight_no_crash_any_type(s):
    try:
        total_weight(s)
    except Exception as e:
        assert False, f"total_weight crashed with: {e!r}"


@settings(max_examples=300)
@given(st.lists(st.sampled_from(["nan", "inf", "-inf", "1e400", "-5", "12.5", "7", "", " "]),
                min_size=1, max_size=6))
def test_total_weight_result_is_finite_and_non_negative(parts):
    """A total weight must be a real, non-negative number: NaN, infinity and
    negative bag weights must be rejected (None), not silently summed."""
    s = ",".join(parts)
    try:
        result = total_weight(s)
    except Exception as e:
        assert False, f"total_weight crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result) and result >= 0, f"total_weight({s!r}) returned {result}"


@given(st.lists(st.floats(min_value=0, max_value=1000, allow_nan=False), min_size=1, max_size=10))
def test_total_weight_valid_csv(weights):
    s = ",".join(repr(w) for w in weights)
    assert math.isclose(total_weight(s), sum(weights), rel_tol=1e-9, abs_tol=1e-9)


# ============================= tag_label ===============================

@settings(max_examples=500)
@given(st.text() | st.none())
def test_tag_label_no_crash(s):
    try:
        tag_label(s)
    except Exception as e:
        assert False, f"tag_label crashed with: {e!r}"


@settings(max_examples=300)
@given(any_input)
def test_tag_label_no_crash_any_type(s):
    try:
        tag_label(s)
    except Exception as e:
        assert False, f"tag_label crashed with: {e!r}"


@given(
    first=st.text(alphabet=LETTERS, min_size=1, max_size=10),
    last=st.text(alphabet=LETTERS, min_size=1, max_size=12),
)
def test_tag_label_first_and_last(first, last):
    assert tag_label(f"{first} {last}") == f"{first[0].upper()}. {last.upper()}"


@given(
    first=st.text(alphabet=LETTERS, min_size=1, max_size=10),
    middle=st.text(alphabet=LETTERS, min_size=1, max_size=10),
    last=st.text(alphabet=LETTERS, min_size=1, max_size=12),
)
def test_tag_label_uses_last_name_with_middle_name(first, middle, last):
    """'John Paul Smith' should be tagged with the LAST name: 'J. SMITH'."""
    assert tag_label(f"{first} {middle} {last}") == f"{first[0].upper()}. {last.upper()}"
