# app/api.py
from flask import Flask, request, jsonify
from pricing import YieldCurve, price_zero_coupon, price_coupon_bond
from data import get_default_curve
import os

app = Flask(__name__)
APP_VERSION = os.environ.get("APP_VERSION", "dev")

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok", version=APP_VERSION)

@app.route("/curve", methods=["GET"])
def curve():
    curve = get_default_curve()
    return jsonify(curve=curve)

@app.route("/price", methods=["POST"])
def price():
    """
    expected JSON:
    {
      "type": "zero" | "coupon",
      "maturity_years": 5,
      "face": 1000,
      "coupon_rate": 0.02,        # required for coupon
      "coupons_per_year": 2,     # optional, default 1
      "curve": {optional custom curve dict}
    }
    """
    data = request.get_json(force=True)
    if not data:
        return jsonify(error="invalid json"), 400
    typ = data.get("type", "zero")
    maturity = float(data.get("maturity_years", 0))
    face = float(data.get("face", 1000.0))
    coupons_per_year = int(data.get("coupons_per_year", 1))
    curve_dict = data.get("curve", None)
    if curve_dict is None:
        curve_dict = get_default_curve()
    yc = YieldCurve(curve_dict)
    # get spot rate at maturity
    rate = yc.rate_at(maturity)
    if typ == "zero":
        p = price_zero_coupon(face=face, maturity_years=maturity, annual_rate=rate)
    elif typ == "coupon":
        coupon_rate = float(data.get("coupon_rate", 0.0))
        p = price_coupon_bond(face=face, coupon_rate=coupon_rate, maturity_years=maturity, annual_rate=rate, coupons_per_year=coupons_per_year)
    else:
        return jsonify(error="unknown type"), 400
    return jsonify({
        "price": round(p, 6),
        "maturity_years": maturity,
        "rate_used": rate,
        "type": typ,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
