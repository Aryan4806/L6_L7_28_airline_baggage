"""Branch coverage tests for airline_baggage.py.

Goal: take both the True and the False outcome of every decision
(if / elif / else) in the module at least once.

Run:
    coverage run --branch -m pytest test_branch_coverage.py
    coverage report -m
"""
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ======================= baggage_fee =======================

# Decision 1: cabin not in FREE_ALLOWANCE
def test_b1_true_unknown_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


@pytest.mark.parametrize("cabin", ["economy", "premium", "business"])
def test_b1_false_known_cabins(cabin):
    assert baggage_fee(cabin, 0, "domestic", False) == 0


# Decision 2: weight_kg < 0
def test_b2_true_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -0.5, "domestic", False)


def test_b2_false_zero_weight_boundary():
    assert baggage_fee("economy", 0, "domestic", False) == 0


# Decision 3: is_member and cabin != "business"
def test_b3_true_member_economy():
    # 15 + 10 = 25 allowance -> 26 kg gives 1 kg excess * 20
    assert baggage_fee("economy", 26, "domestic", True) == 20


def test_b3_false_member_business_no_bonus():
    # business 40, no bonus -> 41 kg gives 1 kg excess * 20
    assert baggage_fee("business", 41, "domestic", True) == 20


def test_b3_false_non_member():
    # premium 25, no bonus -> 26 kg gives 1 kg excess * 20
    assert baggage_fee("premium", 26, "domestic", False) == 20


# Decision 4: excess <= 0
def test_b4_true_exactly_at_allowance():
    assert baggage_fee("economy", 15, "domestic", False) == 0


def test_b4_false_just_over_allowance():
    assert baggage_fee("economy", 16, "domestic", False) == 20


# Decision 5: route == "domestic"  (else -> rate 45)
def test_b5_true_domestic_rate():
    assert baggage_fee("economy", 25, "domestic", False) == 10 * 20


def test_b5_false_international_rate():
    assert baggage_fee("economy", 25, "international", False) == 10 * 45


def test_b5_false_other_route_uses_45():
    assert baggage_fee("economy", 25, "regional", False) == 10 * 45


# Decision 6: excess > 20
def test_b6_false_excess_exactly_20():
    assert baggage_fee("economy", 35, "domestic", False) == 20 * 20


def test_b6_true_domestic_large_excess_no_surcharge():
    # Decision 7 False: domestic -> rate 20*2 = 40
    assert baggage_fee("economy", 36, "domestic", False) == 21 * 40


# Decision 7: route == "international" (nested inside excess > 20)
def test_b7_true_international_surcharge():
    # rate 45*2 + 10 = 100
    assert baggage_fee("economy", 36, "international", False) == 21 * 100


def test_b7_false_other_route_no_surcharge():
    # rate 45*2 = 90, no +10 because route is not "international"
    assert baggage_fee("economy", 36, "regional", False) == 21 * 90


# ======================= carry_on_ok =======================

# Decision 8: is_infant
def test_b8_true_infant_two_items():
    assert carry_on_ok(20, 2, True) is True


def test_b8_true_infant_three_items():
    assert carry_on_ok(1, 3, True) is False


# Decision 9: weight_kg > 7
def test_b9_true_overweight():
    assert carry_on_ok(7.1, 1, False) is False


def test_b9_false_weight_boundary_one_item():
    assert carry_on_ok(7, 1, False) is True


def test_b9_false_too_many_items():
    assert carry_on_ok(5, 2, False) is False


# ======================= check_in_status =======================

# Decision 10: has_baggage   Decision 11: is_international
@pytest.mark.parametrize(
    "has_baggage, is_international, cutoff",
    [
        (True, True, 120),
        (True, False, 60),
        (False, True, 105),
        (False, False, 45),
    ],
)
def test_b10_b11_cutoff_combinations(has_baggage, is_international, cutoff):
    assert check_in_status(cutoff, has_baggage, is_international) == "open"
    assert check_in_status(cutoff - 1, has_baggage, is_international) == "late"


# Decision 12: minutes_before >= cutoff   Decision 13: >= cutoff - 15
def test_b12_true_open():
    assert check_in_status(90, True, False) == "open"


def test_b13_true_late_lower_boundary():
    assert check_in_status(45, True, False) == "late"


def test_b13_false_closed():
    assert check_in_status(44, True, False) == "closed"
