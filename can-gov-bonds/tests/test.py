import requests

url = "http://can-gov-bonds.local/price"
payload = {
    "type": "coupon",
    "maturity_years": 10,
    "face": 1000,
    "coupon_rate": 0.02,
    "coupons_per_year": 2
}

resp = requests.post(url, json=payload)
print(resp.status_code)
print(resp.text)  # <-- see what the server actually returned
