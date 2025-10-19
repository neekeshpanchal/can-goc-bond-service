# tests/test_pricing.py
from app.pricing import YieldCurve, price_zero_coupon, price_coupon_bond

def test_zero_coupon():
    yc = YieldCurve({"1-3Y": 0.02, "3-5Y":0.03, "5-10Y":0.04, "10-15Y":0.05, "15-30Y":0.06})
    r = yc.rate_at(2.0)
    p = price_zero_coupon(1000, 2.0, r)
    assert p > 0 and p < 1000

def test_coupon_bond():
    yc = YieldCurve({"1-3Y": 0.01, "3-5Y":0.015, "5-10Y":0.02, "10-15Y":0.025, "15-30Y":0.03})
    r = yc.rate_at(5.0)
    p = price_coupon_bond(1000, 0.02, 5.0, r, coupons_per_year=2)
    assert p > 0
