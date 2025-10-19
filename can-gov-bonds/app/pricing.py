# app/pricing.py
from __future__ import annotations
from typing import Dict, List, Tuple
import math

# Tenor keys we will use (years)
TENOR_BUCKETS = ["1-3Y", "3-5Y", "5-10Y", "10-15Y", "15-30Y"]

class YieldCurve:
    """
    Simple yield curve backed by fixed bucket mid-point rates (annual, decimal).
    Example storage: {"1-3Y": 0.02, "3-5Y": 0.025, ...}
    Rates are annual spot yields (continuous compounding assumed for ZCB price calculation).
    """
    def __init__(self, bucket_rates: Dict[str, float]):
        missing = [b for b in TENOR_BUCKETS if b not in bucket_rates]
        if missing:
            raise ValueError(f"Missing rates for buckets: {missing}")
        self.bucket_rates = bucket_rates
        # convert bucket to midpoint in years for interpolation
        self.bucket_points = {
            "1-3Y": 2.0,
            "3-5Y": 4.0,
            "5-10Y": 7.5,
            "10-15Y": 12.5,
            "15-30Y": 22.5,
        }

    def rate_at(self, maturity_years: float) -> float:
        """
        Returns interpolated spot rate (annual, decimal) for a given maturity in years.
        Uses linear interpolation between bucket midpoints.
        """
        pts = sorted((self.bucket_points[b], self.bucket_rates[b]) for b in self.bucket_points)
        years = maturity_years
        if years <= pts[0][0]:
            return pts[0][1]
        if years >= pts[-1][0]:
            return pts[-1][1]
        # find interval
        for i in range(len(pts) - 1):
            x0, r0 = pts[i]
            x1, r1 = pts[i+1]
            if x0 <= years <= x1:
                t = (years - x0) / (x1 - x0)
                return r0 + t * (r1 - r0)
        # fallback
        return pts[-1][1]

def price_zero_coupon(face: float, maturity_years: float, annual_rate: float) -> float:
    """
    Price of a zero-coupon bond assuming continuous compounding:
    P = F * exp(-r * T)
    """
    return face * math.exp(-annual_rate * maturity_years)

def price_coupon_bond(face: float, coupon_rate: float, maturity_years: float, annual_rate: float, coupons_per_year: int = 1) -> float:
    """
    Price a fixed-coupon bond paying coupon_rate (annual decimal) with coupons_per_year payments.
    Discounting using continuous compounding with annual_rate (spot).
    """
    # number of coupon payments
    n = int(round(maturity_years * coupons_per_year))
    coupon = face * coupon_rate / coupons_per_year
    pv = 0.0
    for k in range(1, n + 1):
        t = k / coupons_per_year
        pv += coupon * math.exp(-annual_rate * t)
    # final principal
    pv += face * math.exp(-annual_rate * maturity_years)
    return pv
