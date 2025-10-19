# app/data.py
from typing import Dict

DEFAULT_CURVE = {
    "1-3Y": 0.015,   # 1.5%
    "3-5Y": 0.018,   # 1.8%
    "5-10Y": 0.020,  # 2.0%
    "10-15Y": 0.025, # 2.5%
    "15-30Y": 0.030, # 3.0%
}

def get_default_curve() -> Dict[str, float]:
    return DEFAULT_CURVE.copy()
